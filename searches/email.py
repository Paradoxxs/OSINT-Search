import asyncio
from modules.Email_registration_lookup import holehe, get_poastal, ghunt
import json
from utils.helpers import convert_datetime, public_emails
from searches.domain import Domain
from searches.username import Username
class Email():

    
    def splitEmail(self,email):
        email_split = email.split("@")
        username = email_split[0]
        domain = email_split[1]
        return username,domain
    #TODO split email up in username and domain and perform search on each, maybe check the domain of the mail no need to analysis gmail and similar emails
    async def search(self,email):
        username,domain = self.splitEmail(email)
        holehe_data = asyncio.run(holehe.query(email))
        # append source to holehe hits
        for hit in holehe_data:
            hit["source"] = "holehe"
        
        poastal_data = get_poastal(email)
        poastal_hits = []
        for domain, exists in poastal_data.items():
            # exists is a str ("true" or "false")
            # so we use json.loads to convert it to a bool
            try:
                exists = json.loads(exists)
            except:
                # Poastal returns "unknown" for Facebook - probably from Duolingo - for some reason
                exists = False
            poastal_hits.append({"source": "poastal", "domain": domain, "exists": exists})



        # combine holehe and poastal hits
        hits = holehe_data + poastal_hits
        
        if email.endswith("@gmail.com"):
            gdata = asyncio.run(ghunt.query(email))
            if gdata is not False:
                dict_hits = {item["domain"]: item for item in hits}
                result = {**dict_hits, **gdata}
            
        json_result = json.dumps(result, default=convert_datetime)

        if domain not in public_emails():
            domain_data = asyncio.run(Domain.search(domain))

        username_lookup = asyncio.run(Username.search(username))

        data = {
            "hits":hits,
            "Jresults": json_result,
            "Username":username_lookup,
            "domain":domain_data,
            "gdata":gdata
        }

        #TODO compromised email
        return data 