import asyncio
from modules.Email_registration_lookup import holehe, get_poastal, ghunt
import json
from searches.username import Username
from utils.helpers import splitEmail
class Analysis_email:
    
    async def analysis(self,email):
        data = {}
        username,domain = splitEmail(email)
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
        gdata = await ghunt().query(email)

        username_lookup = await Username().search(username)

        #check value is empty if not add to dict
        if hits != None:
            data["hits"] = hits
        if gdata != None:
            data["gdata"] = gdata
        if username_lookup != None:
            data["Username"] = username_lookup

        

        #TODO compromised email
        return data 