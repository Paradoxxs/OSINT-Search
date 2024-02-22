
import requests
from utils.helpers import get_env_var
import aiohttp

class Ipstack:
    """
    Ipstack GeoIP
    Leverages the ipstack.com API to geolocate a host by IP address.
    """

    meta = {"description": "Query IPStack's GeoIP API", "auth_required": True}
    api_key= (get_env_var("ipstack_api"))
    base_url = "http://api.ipstack.com"


    async def query(self, domain):
        try:
            url = f"{self.base_url}/{domain}?access_key={self.api_key}"
            result = requests(url)
            if result:
                geo_data = result.json()
                if not geo_data:
                    print(f"No JSON response from {url}")
            else:
                print(f"No response from {url}")
        except Exception:
            print(f"Error retrieving results for {domain}", trace=True)
            return
        geo_data = {k: v for k, v in geo_data.items() if v is not None}
        if "error" in geo_data:
            error_msg = geo_data.get("error").get("info", "")
            if error_msg:
                self.warning(error_msg)
        elif geo_data:
            return geo_data
        




class IP2Location:
    """
    IP2Location.io Geolocation API.
    30K monthly limit
    """

    meta = {"description": "Query IP2location.io's API for geolocation information. ", "auth_required": True}
    options = {"api_key": "", "lang": ""}
    options_desc = {
        "api_key": "IP2location.io API Key",
        "lang": "Translation information(ISO639-1). The translation is only applicable for continent, country, region and city name.",
    }
    api_key = get_env_var("ip2location_api")
    base_url = "http://api.ip2location.io"

    async def query(self, IP):
        url = f"{self.base_url}/?ip={IP}&key={self.api_key}&format=json"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        geo_data = await response.json()
                        if not geo_data:
                            print(f"No JSON response from {url}")
                    else:
                        print(f"No response from {url}")
                        response.raise_for_status()
            except aiohttp.ClientError as e:
                print(f"Error retrieving results for {IP}: {e}")
                raise Exception

        geo_data = {k: v for k, v in geo_data.items() if v is not None}
        if geo_data:
            return geo_data
        else:
            raise Exception("No geolocation data found")

class IPInfo:
    async def query(self, ipAddress):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://ipinfo.io/{ipAddress}/json") as response:
                    return await response.json()
        except:
            return None

class IPLookup:
    def __init__(self):
        self.ip2location = IP2Location()
        self.ipinfo = IPInfo()

    async def query(self, ipAddress):
        ##TODO clean up the way data is returned, so that it consistence no matter what API is used.
        try:
            data = await self.ip2location.query(ipAddress)
        except Exception as e:
            print(f"Error querying IP2Location API: {e}")
            data = await self.ipinfo.query(ipAddress)
        return data

    
