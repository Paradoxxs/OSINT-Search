from utils.helpers import get_env_var, convert_datetime, public_emails
from modules.historical_dns import mnemonic
from modules.webpage_archives import wayback
from modules.shodan_search import shodan
from modules.get_infastructure import get_whois
from modules.webpage_technology import wappalyzer
from modules.ip_lookup import IPLookup
from modules.find_emails import FindEmail
from modules.port_scan import PortScan
import requests
import aiodns
import asyncio
from modules.scan_webpage import ScanWebpage, Find_Google_analytic_id
from modules.subdomain import Subdomain as module_subdomain
import socket

class Domain():

    async def domain_to_ip(self, domain):
        resolver = aiodns.DNSResolver()
        try:
            result = await resolver.query(domain, 'A')
            if result:
                return result[0].host
            else:
                return None
        except aiodns.error.DNSError:
            return None
        
    async def test_connection(self,domain, timeout=2):
    
        try:
            # Create a socket object
            response = requests.get(f"https://{domain}",verify=True,timeout=timeout)
            # Connection successful
            print(f"Connected to {domain} successfully")
            return True,response
        except socket.error as e:
            # Connection failed
            print(f"Failed to connect to {domain}: {e}")
            return False,None
    

    async def find_emails(self,domain):
        if domain not in public_emails():
            emails = await FindEmail().query(domain)
            return emails
        return None

        

    async def webpage_analysis(self,response):
        tech = await wappalyzer().query(response)
        social_data,Google_analytic_id = await ScanWebpage().query(response)
        return tech,social_data,Google_analytic_id


    async def analysis(self,domain):
        
        ##TODO Should I analyze all the subdomain to the level I do? it can quickly take a lot of time.
        data = {"domain":domain}
        ip = await self.domain_to_ip(domain)
        hist_dns_data = await mnemonic().query(domain)
        wayback_data = await wayback().query(domain)

        if ip != None:
            nmap = await PortScan().query(ip)
            ipwhois = await IPLookup().query(ip)
            if ipwhois != None:
                data["ip_whois"] = ipwhois
            if nmap is not None:
                data["nmap"] = nmap
            available,res = await self.test_connection(domain)
            if available:
                tech,social_data,Google_analytic_id = await self.webpage_analysis(res)
                if Google_analytic_id is not None:
                    data["Google_analytic_id"] = Google_analytic_id
                if tech is not None:
                    data["Technology"] = tech
                if social_data is not None:
                    data["Social"] = social_data

        if wayback_data is not None:
            data["Wayback"] = wayback_data
        if hist_dns_data is not None:
            data["HistoricalDNS"] = hist_dns_data
        return data
        
    
    async def search(self,domain):
        data = {}

        WHOIS_data = get_whois(domain)
        emails = await self.find_emails(domain)

        subdomains = await module_subdomain().search(domain)
        if subdomains is not None:
            #TODO optimize so we do not lookup the same IP multiple times
            tasks = [asyncio.create_task(self.analysis(subdomain))  for subdomain in subdomains]
            subdomains = await asyncio.gather(*tasks)
             

        
        hostIO = requests.request("GET", f"https://host.io/api/full/{domain}?token={get_env_var('hostIO_api')}")



        if emails != None:
            data["emails"] = emails
        if hostIO is not None:
            data["hostIO"] = hostIO.json()
        if WHOIS_data is not None:
            data["WHOIS"] = WHOIS_data
        if subdomains is not None:
            data["subdomains"] = subdomains
     
        return data 
    