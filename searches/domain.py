import asyncio
import requests
from utils.helpers import get_env_var, convert_datetime, public_emails
from modules.historical_dns import mnemonic
from modules.webpage_archives import wayback
from modules.shodan_search import shodan_search
from modules.get_infastructure import get_whois
from modules.webpage_technology import wappalyzer, spyonweb
from modules.ip_lookup import IPLookup
from modules.find_emails import FindEmail
from modules.port_scan import PortScan
from modules.scan_webpage import ScanWebpage
from modules.subdomain import Subdomain as module_subdomain
from modules.sslCert_lookup import tlsjarm, crt
import aiodns
import aiohttp
import socket

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
            response = requests.get(f"https://{domain}", verify=True, timeout=timeout)
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
                data["ip_org"] = ipwhois.get("org") if ipwhois.get("org") else ipwhois.get("asn") + " " + ipwhois.get("as")
                data["IP_country"] = ipwhois.get("country") if ipwhois.get("country") else ipwhois.get("country_name")   
                data["ip_whois"] = ipwhois
            available, res = await self.test_connection(domain)
            if available:
                tech, social_data, Google_analytic_id = await self.webpage_analysis(res)
                if Google_analytic_id:
                    data["Google_analytic_id"] = Google_analytic_id

                    google_analytic_shared = spyonweb().query(Google_analytic_id)
                    if google_analytic_shared:
                        data["Google_analytic_shared"] = google_analytic_shared
                if tech:
                    data["Technology"] = tech
                if social_data:
                    data["Social"] = social_data
        return data

    async def search(self, domain):
        data = {}
        ip = await self.domain_to_ip(domain)
        shodan_ip = await shodan_search().IP_services(ip)
        WHOIS_data = get_whois(domain)
        TLS_jarm = await tlsjarm().search(domain)
        ssl_certs = await crt().query(domain)
        emails = await self.find_emails(domain)
        hist_dns_data = await mnemonic().query(domain)
        wayback_data = await wayback().query(domain)
        subdomains = await module_subdomain().search(domain)
        if subdomains:
            tasks = [asyncio.create_task(self.subdomain_analysis(subdomain)) for subdomain in subdomains]
            subdomains = await asyncio.gather(*tasks)
        hostIO = requests.get(f"https://host.io/api/full/{domain}?token={get_env_var('hostIO_api')}").json()
        if hostIO:
            data["hostIO"] = hostIO
        if WHOIS_data:
            data["WHOIS"] = WHOIS_data
        if TLS_jarm:
            data["TLS_jarm"] = TLS_jarm
        if ssl_certs:
            data["tls_certs"] = ssl_certs
        if shodan_ip:
            data["shodan_ip"] = shodan_ip
        if emails:
            data["emails"] = emails

        data["wayback"] = wayback_data if wayback_data else {}
        data["hist_dns"] = hist_dns_data if hist_dns_data else {}
        if subdomains:
            data["subdomains"] = subdomains
        return data
