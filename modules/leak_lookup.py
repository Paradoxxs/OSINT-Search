import requests 
from utils.helpers import get_env_var
class breachdirectory:
    
    #https://rapidapi.com/rohan-patra/api/breachdirectory
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



class leaklookup:

    #https://leak-lookup.com/api
    api_key = get_env_var("leaklookup_api")
    base_url = "https://leak-lookup.com/api/search"
    def query(self,email):

        payload = { 'key': self.api_key,
                    'type': 'email_address',
                    'query': {email}
                    }

        response = requests.post(self.base_url, data=payload)

        return response.json()  # or any other desired processing of the response


