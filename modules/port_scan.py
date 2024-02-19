import nmap3


class nmap():
    
    nmap = nmap3.Nmap()

    async def query(self, ipAddress):  # Define as asynchronous method
        # scan top 10 ports defined by nmap
        data = self.nmap.scan_top_ports(ipAddress)
        return data 

class PortScan():

    scan = nmap()

    async def query(self, ipAddress):
        return await self.scan.query(ipAddress)  # Await the result
