from modules.ip2geo import IP2Location
import requests
from modules.shodan_search import shodan

class IPaddress():


    async def search(self,ipAddress):
        data = {}
        geo_data = IP2Location().query(ipAddress)
        ipinfo_r = requests.request("GET", f"https://ipinfo.io/{ipAddress}/json")
        shodan_data = shodan().IP_services(ipAddress)
        if geo_data != None:
            data["geo"] = geo_data
        if ipinfo_r != None:
            data["ipinfo"] = ipinfo_r.json()
        if shodan_data != None:
            data["shodan"] = shodan_data
        return data