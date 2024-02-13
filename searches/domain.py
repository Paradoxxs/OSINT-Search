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

class Domain():

    async def find_emails(self,domain):
        emails = []
        emails.extend(skymem.query(domain))
    async def find_subdomain(self,domain):
        print(domain)
        subdomain = []
        subdomain.extend(dnsdumpster.query(domain))
        subdomain.extend(rapiddns.query(domain))
        subdomain.extend(certspotter.query(domain))
        # remove duplicates
        subdomain = list(set(subdomain))
        return subdomain
    async def webpage_analsis(self,domain):
        webtech = wappalyzer.wappalyze(self,domain)
        socials = social.query(domain)


    async def search(self,domain):
        WHOIS_hits = get_whois(domain)

        #host.io
        hostIO = requests.request("GET", f"https://host.io/api/full/{domain}?token={get_env_var('hostIO_api')}")
        print(hostIO.json())
        result = {**hostIO.json(), **WHOIS_hits}
        # Serialize the result dictionary with the custom encoder
        json_result = json.dumps(result, default=convert_datetime)
        shodan_data = shodan.favicon_search(domain)
        hist_dns_data = mnemonic.query(domain)
        wayback_data = wayback.query(domain)
        subdomains = await self.find_subdomain(domain)

        if domain not in public_emails():
            #TODO find emails and analysis domain
            print(domain)

        if 80 in shodan_data or 443 in shodan_data.ports:
            webpage_data = self.webpage_analsis(domain)
            

        data = {
            "WhoIs": WHOIS_hits,
            "Shodan": shodan_data,
            "HistoricalDNS": hist_dns_data,
            "Wayback": wayback_data,
            "JSON": json_result,
            "result": result,
            "technology":webpage_data,
            "subdomain":subdomains
        }

        
        return data 