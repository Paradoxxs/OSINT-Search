
from modules.webpage_technology import wappalyzer
from modules.scan_webpage import social
from modules.subdomain import Subdomain as module_subdomain
from utils.helpers import public_emails

import pandas as pd
import aiodns
import asyncio
import socket
class Subdomain():

    async def domain_to_ip_async(self,domain):
        resolver = aiodns.DNSResolver()
        try:
            result = await resolver.query(domain, 'A')
            return result[0].host
        except aiodns.error.DNSError:
            return None
        
    async def test_connection(self,domain, timeout=2):
    
        try:
            # Create a socket object
            sock = socket.create_connection((domain, 80), timeout=timeout)
            # Connection successful
            print(f"Connected to {domain} successfully")
            sock.close()
            return True
        except socket.error as e:
            # Connection failed
            print(f"Failed to connect to {domain}: {e}")
            return False


    
    async def analsis(self,domain):
        ip = await self.domain_to_ip_async(domain)
        if ip != None:
            available = await self.test_connection(domain)
            if available:
                tech = await wappalyzer().query(domain)
                #TODO need to change the way social_data is stored it gets represented wrong in streamlit
                social_data = await social().query(domain)
                return {"ip": ip,"technology": tech, "social": social_data}
        return {"ip": ip,"technology": None, "social": None}
        #TODO enrich ip data
        


    async def search(self,domain):
        subdomains = await module_subdomain().search(domain)


        if subdomains is not None:
            # test if domain response to url requests
            subdomains_df = pd.DataFrame(subdomains, columns=["subdomain"])
            #subdomains_df["technology"]= subdomains_df["subdomain"].apply(self.webpage_analsis)
            #subdomains_df["technology"] = [await self.webpage_analsis(r) for r in subdomains_df["subdomain"]]
            tasks = [asyncio.create_task(self.analsis(r))  for r in subdomains_df["subdomain"]]
            results = await asyncio.gather(*tasks)
            subdomains_df = subdomains_df.join(pd.DataFrame.from_dict(results))   


