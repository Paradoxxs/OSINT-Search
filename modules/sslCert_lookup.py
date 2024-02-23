import asyncio
import aiohttp
from jarm.scanner.scanner import Scanner

class crt:
    meta = {"description": "Query crt.sh (certificate transparency) for subdomains"}

    base_url = "https://crt.sh"
    reject_wildcards = False


    async def request_url(self, domain):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/?q={domain}&output=json") as response:
                return await response.json()

    def parse_results(self, data, query):
        cert_ids = set()
        for cert_info in data:
            if not isinstance(cert_info, dict):
                continue
            cert_id = cert_info.get("id")
            if cert_id:
                if hash(cert_id) not in cert_ids:
                    cert_ids.add(hash(cert_id))
                    domain = cert_info.get("name_value")
                    if domain:
                        for d in domain.splitlines():
                            yield d.lower()

    async def query(self, domain):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/?q={domain}&output=json") as response:
                return await response.json()

class tlsjarm:

    async def search(self, domain):
        data = await Scanner.scan_async(domain, 443)
        return data[0]
