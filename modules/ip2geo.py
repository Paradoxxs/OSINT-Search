
import requests
from utils.helpers import get_env_var
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
                    self.verbose(f"No JSON response from {url}")
            else:
                self.verbose(f"No response from {url}")
        except Exception:
            self.verbose(f"Error retrieving results for {domain}", trace=True)
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
        url = f"{self.base_url}/?key={self.api_key}&ip={IP}&format=json&source=bbot"
        try:
            result = requests(url)
            if result:
                geo_data = result.json()
                if not geo_data:
                    self.verbose(f"No JSON response from {url}")
            else:
                self.verbose(f"No response from {url}")
        except Exception:
            self.verbose(f"Error retrieving results for {IP}", trace=True)
            return

        geo_data = {k: v for k, v in geo_data.items() if v is not None}
        if "error" in geo_data:
            error_msg = geo_data.get("error").get("error_message", "")
            if error_msg:
                self.warning(error_msg)
        elif geo_data:
            print(geo_data)
            return geo_data
        

