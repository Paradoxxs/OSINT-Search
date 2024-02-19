from shodan import Shodan
import mmh3
from utils.helpers import get_env_var
import requests
import codecs

class shodan: 

    api_key = get_env_var("shodan_key")
    shodan_api = Shodan(api_key)
    async def favicon_search(self,domain):
        try:
            response = requests.get("http://www.{}/favicon.ico".format(domain),verify=False)
            if response.status_code != 200:
                favicon = codecs.encode(response.content, 'base64')
                hash = mmh3.hash(favicon)
                results = self.shodan_api.search_cursor("http.favicon.hash:{}".format(hash))   
                return results
        except Exception as e:
            print(e)
            return False
        
    async def IP_services(self,ipAddress):
        try:
            return self.shodan_api.host(ipAddress)
             
        except Exception as e:
            print(e)
            return {}
        
    