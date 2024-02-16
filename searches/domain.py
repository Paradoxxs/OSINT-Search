from utils.helpers import get_env_var, convert_datetime, public_emails
from modules.historical_dns import mnemonic
from modules.webpage_archives import wayback
from modules.shodan_search import shodan
from modules.get_infastructure import get_whois
from modules.webpage_technology import wappalyzer
from modules.scan_webpage import social
from modules.subdomain import dnsdumpster, rapiddns, certspotter
from modules.find_emails import FindEmail
import requests
import json
import pandas as pd
import aiodns
from searches.analysisMail import Analysis_email
import asyncio
class Domain():

    async def domain_to_ip_async(self,domain):
        resolver = aiodns.DNSResolver()
        try:
            result = await resolver.query(domain, 'A')
            return result[0].host
        except aiodns.error.DNSError:
            return None
    

    async def find_emails(self,domain):
        if domain not in public_emails():
            emails = await FindEmail().query(domain)
            if emails != None:
                emails = list(set(emails))
                tasks = [asyncio.create_task(Analysis_email().analysisEmail(mail)) for mail in emails]
                results = await asyncio.gather(*tasks)
                df = pd.DataFrame(emails)
                df = df.join(pd.DataFrame.from_dict(results))
                return df
        return None

    async def find_subdomain(self,domain):
        print(domain)
        subdomain = []
        subdomain.extend(await dnsdumpster().query(domain))
        subdomain.extend(await rapiddns().query(domain))
        subdomain.extend(await certspotter().query(domain))
        # remove duplicates
        subdomain = list(set(subdomain))
        return subdomain
    
    async def subdomain_analsis(self,domain):
        tech = await wappalyzer().query(domain)
        #TODO need to change the way social_data is stored it gets represented wrong in streamlit
        social_data = await social().query(domain)
        ip = await self.domain_to_ip_async(domain)
        #TODO enrich ip data
        return {"ip": ip,"technology": tech, "social": social_data}


    async def search(self,domain):
        data = {}
        WHOIS_hits = get_whois(domain)
        wayback_data = None
        webpage_data = None
        hostIO = requests.request("GET", f"https://host.io/api/full/{domain}?token={get_env_var('hostIO_api')}")


        shodan_data = await shodan().favicon_search(domain)
        hist_dns_data = await mnemonic().query(domain)
        wayback_data = await wayback().query(domain)
        #subdomains = await self.find_subdomain(domain)




        

        if shodan_data is not None:
            data["shodan"] = shodan_data
        if hist_dns_data is not None:
            data["HistoricalDNS"] = hist_dns_data
        if wayback_data is not None:
            data["Wayback"] = wayback_data
        if webpage_data is not None:
            data["technology"] = webpage_data

        if hostIO is not None:
            data["hostIO"] = hostIO.json()
        if WHOIS_hits is not None:
            data["WHOIS"] = WHOIS_hits


        
        return data 
    
"""         if subdomains_df is not None:
            data["subdomain"] = subdomains_df """
"""         if subdomains is not None:
            # test if domain response to url requests
            subdomains_df = pd.DataFrame(subdomains, columns=["subdomain"])
            #subdomains_df["technology"]= subdomains_df["subdomain"].apply(self.webpage_analsis)
            #subdomains_df["technology"] = [await self.webpage_analsis(r) for r in subdomains_df["subdomain"]]
            results = [await self.subdomain_analsis(r) for r in subdomains_df["subdomain"]]
            subdomains_df = subdomains_df.join(pd.DataFrame.from_dict(results))   
 """
