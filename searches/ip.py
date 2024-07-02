from modules.ip_lookup import IPLookup
import requests
from modules.shodan_search import shodan
from modules.port_scan import PortScan

class IPaddress():


    async def search(self,ipAddress):
        data = {}
        ip_lookup = await IPLookup().query(ipAddress)
        shodan_data = await shodan().IP_services(ipAddress)
        nmap = await PortScan().query(ipAddress)


        if ip_lookup != None:
            data["ip_Whois"] = ip_lookup
        if shodan_data != None:
            data["shodan_ip"] = shodan_data
        if nmap != None:
            data["nmap"] = nmap

        return data
