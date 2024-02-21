import nmap3
import json

class nmap():
    
    nmap = nmap3.Nmap()

    async def query(self, ipAddress):  # Define as asynchronous method
        # scan top 10 ports defined by nmap
        data = self.nmap.scan_top_ports(ipAddress)
        return data 

class PortScan():

    scan = nmap()

    async def query(self, ipAddress):
        data =  await self.scan.query(ipAddress)  # Await the result
        # convert to data to json
        return json.dumps(data)
        
