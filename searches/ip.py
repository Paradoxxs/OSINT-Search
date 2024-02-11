from modules.ip2geo import IP2Location
import requests
from modules.shodan_search import shodan

class IPaddress():


    async def search(ipAddress):
        geo_data = IP2Location.query(ipAddress)
        ipinfo_r = requests.request("GET", f"https://ipinfo.io/{ipAddress}/json")
        shodan_data = shodan.IP_services(ipAddress)
        return geo_data,ipinfo_r,shodan_data