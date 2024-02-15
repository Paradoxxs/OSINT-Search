from utils.helpers import get_env_var, convert_datetime, public_emails
from modules.historical_dns import mnemonic
from modules.webpage_archives import wayback
from modules.shodan_search import shodan
from modules.get_infastructure import get_whois
from modules.webpage_technology import wappalyzer
from modules.scan_webpage import social
from modules.subdomain import dnsdumpster, rapiddns, certspotter
from modules.Find_email import skymem
import requests
import json
import pandas as pd

class Domain():

    async def find_emails(self,domain):
        emails = []
        emails.extend(skymem().query(domain))

    async def find_subdomain(self,domain):
        print(domain)
        subdomain = []
        subdomain.extend(await dnsdumpster().query(domain))
        subdomain.extend(await rapiddns().query(domain))
        subdomain.extend(await certspotter().query(domain))
        # remove duplicates
        subdomain = list(set(subdomain))
        return subdomain
    
    async def webpage_analsis(self,domain):
        webtech = await wappalyzer().query(domain)
        #socials = await social().query(domain)
        return webtech


    async def search(self,domain):
        data = {}
        WHOIS_hits = get_whois(domain)
        wayback_data = None
        webpage_data = None
        hostIO = requests.request("GET", f"https://host.io/api/full/{domain}?token={get_env_var('hostIO_api')}")


        shodan_data = await shodan().favicon_search(domain)
        hist_dns_data = await mnemonic().query(domain)
        wayback_data = await wayback().query(domain)
        subdomains = await self.find_subdomain(domain)

        if domain not in public_emails():
            #TODO find emails and analysis domain
            print(domain)

        if subdomains is not None:
            # test if domain response to url requests
            subdomains_df = pd.DataFrame(subdomains, columns=["subdomain"])
            #subdomains_df["technology"]= subdomains_df["subdomain"].apply(self.webpage_analsis)
            subdomains_df["technology"]= [await self.webpage_analsis(r) for r in subdomains_df["subdomain"]]

        if shodan_data is not None:
            data["shodan"] = shodan_data
        if hist_dns_data is not None:
            data["HistoricalDNS"] = hist_dns_data
        if wayback_data is not None:
            data["Wayback"] = wayback_data
        if webpage_data is not None:
            data["technology"] = webpage_data
        if subdomains_df is not None:
            data["subdomain"] = subdomains_df
        if hostIO is not None:
            data["hostIO"] = hostIO.json()
        if WHOIS_hits is not None:
            data["WHOIS"] = WHOIS_hits

        
        return data 