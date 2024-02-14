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

        data = {}
        username,domain = self.splitEmail(email)
        holehe_data = await holehe().query(email)
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
            gdata = await ghunt().query(email)

 
        if domain != public_emails():
            domain_data = await Domain().search(domain)

        username_lookup = await Username().search(username)

        #check value is empty if not add to dict
        if hits != None:
            data["hits"] = hits
        if gdata != None:
            data["gdata"] = gdata
        if username_lookup != None:
            data["Username"] = username_lookup
        if domain_data != None:
            data["domain"] = domain_data
        

        #TODO compromised email
        return data 