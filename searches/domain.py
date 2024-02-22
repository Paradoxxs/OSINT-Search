import asyncio
import requests
from utils.helpers import get_env_var, convert_datetime, public_emails
from modules.historical_dns import mnemonic
from modules.webpage_archives import wayback
from modules.shodan_search import shodan
from modules.get_infastructure import get_whois
from modules.webpage_technology import wappalyzer
from modules.ip_lookup import IPLookup
from modules.find_emails import FindEmail
from modules.port_scan import PortScan
from modules.scan_webpage import ScanWebpage, Find_Google_analytic_id
from modules.subdomain import Subdomain as module_subdomain
import socket
import aiodns

class Domain:

    async def domain_to_ip(self, domain):
        resolver = aiodns.DNSResolver()
        try:
            result = await resolver.query(domain, 'A')
            return result[0].host if result else None
        except aiodns.error.DNSError:
            return None

    async def test_connection(self, domain, timeout=2):
        try:
            response = await asyncio.wait_for(requests.get(f"https://{domain}", verify=True), timeout=timeout)
            print(f"Connected to {domain} successfully")
            return True, response
        except (socket.error, asyncio.TimeoutError) as e:
            print(f"Failed to connect to {domain}: {e}")
            return False, None

    async def find_emails(self, domain):
        if domain not in public_emails():
            return await FindEmail().query(domain)
        return None

    async def webpage_analysis(self, response):
        tech = await wappalyzer().query(response)
        social_data, Google_analytic_id = await ScanWebpage().query(response)
        return tech, social_data, Google_analytic_id

    async def subdomain_analysis(self, domain):
        data = {"domain": domain}
        ip = await self.domain_to_ip(domain)
        if ip:
            data["IP"] = ip
            ipwhois = await IPLookup().query(ip)
            if ipwhois:
                data["ip_org"] = ipwhois.get("org", "N/A")
                data["IP_country"] = ipwhois.get("country", "N/A")
                data["ip_whois"] = ipwhois
            available, res = await self.test_connection(domain)
            if available:
                tech, social_data, Google_analytic_id = await self.webpage_analysis(res)
                if Google_analytic_id:
                    data["Google_analytic_id"] = Google_analytic_id
                if tech:
                    data["Technology"] = tech
                if social_data:
                    data["Social"] = social_data
        return data

    async def search(self, domain):
        data = {}
        WHOIS_data = get_whois(domain)
        emails = await self.find_emails(domain)
        hist_dns_data = await mnemonic().query(domain)
        wayback_data = await wayback().query(domain)
        subdomains = await module_subdomain().search(domain)
        if subdomains:
            tasks = [asyncio.create_task(self.subdomain_analysis(subdomain)) for subdomain in subdomains]
            subdomains = await asyncio.gather(*tasks)
        hostIO = requests.get(f"https://host.io/api/full/{domain}?token={get_env_var('hostIO_api')}").json()
        if emails:
            data["emails"] = emails
        if hostIO:
            data["hostIO"] = hostIO
        if WHOIS_data:
            data["WHOIS"] = WHOIS_data
        data["wayback"] = wayback_data if wayback_data else {}
        data["hist_dns"] = hist_dns_data if hist_dns_data else {}
        if subdomains:
            data["subdomains"] = subdomains
        return data
