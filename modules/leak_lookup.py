import requests 
from utils.helpers import get_env_var
import aiohttp
import asyncio


class breachdirectory:
    
    #https://rapidapi.com/rohan-patra/api/breachdirectory
    #Free version hard limit 10/month
    base_url = "https://breachdirectory.p.rapidapi.com/"
    api_key = get_env_var("breachdirectory_api")

    def query(self,email):
        querystring = {"func":"auto","term":{email}}

        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "breachdirectory.p.rapidapi.com"
        }

        response = requests.get(self.base_url, headers=headers, params=querystring)

        return response.json()





class LeakLookup:
    # https://leak-lookup.com/api
    api_key = get_env_var("leaklookup_api")
    base_url = "https://leak-lookup.com/api/search"

    async def search(self, email):
        payload = {'key': self.api_key,
                   'type': 'email_address',
                   'query': {email}
                   }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.base_url, data=payload) as response:
                data = await response.json()
                return list(data['message'].keys())



