import requests
from utils.helpers import get_env_var
import utils.regexes as regexes
import re

class hunterio:
    watched_events = ["DNS_NAME"]
    produced_events = ["EMAIL_ADDRESS", "DNS_NAME", "URL_UNVERIFIED"]
    flags = ["passive", "email-enum", "subdomain-enum", "safe"]
    meta = {"description": "Query hunter.io for emails", "auth_required": True}
    options = {"api_key": ""}
    options_desc = {"api_key": "Hunter.IO API key"}

    base_url = "https://api.hunter.io/v2"
    limit = 25
    api_key = get_env_var("hunterio_api")
    



    async def query(self, domain):
        emails = []
        url = (
            f"{self.base_url}/domain-search?domain={domain}&api_key={self.api_key}"
            + "&limit={page_size}&offset={offset}"
        )
        agen = self.helpers.api_page_iter(url, page_size=self.limit)
        try:
            async for j in agen:
                new_emails = j.get("data", {}).get("emails", [])
                if not new_emails:
                    break
                emails += new_emails
        finally:
            agen.aclose()
        return emails
    




class skymem:
    flags = ["passive", "email-enum", "safe"]
    meta = {"description": "Query skymem.info for email addresses"}

    base_url = "https://www.skymem.info"

    async def query(self, domain):
        emails = []
        # get first page
        url = f"{self.base_url}/srch?q={domain}"
        r = requests.get(url)
        if not r:
            return emails
        for email in regexes.extract_emails(r.text):
            emails.append(email)

        # iterate through other pages
        domain_ids = re.findall(r'<a href="/domain/([a-z0-9]+)\?p=', r.text, re.I)
        if not domain_ids:
            return emails
        domain_id = domain_ids[0]
        for page in range(2, 22):
            r2 = requests.get(f"{self.base_url}/domain/{domain_id}?p={page}")
            if not r2:
                continue
            for email in regexes.extract_emails(r2.text):
                emails.append(email)
            pages = re.findall(r"/domain/" + domain_id + r"\?p=(\d+)", r2.text)
            if not pages:
                break
            last_page = max([int(p) for p in pages])
            if page >= last_page:
                break
        
        return emails
    

class FindEmail:
    
    async def query(self, domain):
        emails = []
        emails.extend(await skymem().query(domain))
        #emails.extend(await hunterio().query(domain))
        #remove duplicates
        emails = list(set(emails))
        #remove emails that does not contain domain
        emails = [email for email in emails if domain in email]
        return emails
    
    