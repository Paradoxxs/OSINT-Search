import requests

class crt:
    meta = {"description": "Query crt.sh (certificate transparency) for subdomains"}

    base_url = "https://crt.sh"
    reject_wildcards = False

    async def setup(self):
        self.cert_ids = set()
        return await super().setup()

    async def request_url(self, domain):
        url = f"{self.base_url}/?q={domain}&output=json"
        return requests.get(url)

    def parse_results(self, r, query):
        j = r.json()
        for cert_info in j:
            if not type(cert_info) == dict:
                continue
            cert_id = cert_info.get("id")
            if cert_id:
                if hash(cert_id) not in self.cert_ids:
                    self.cert_ids.add(hash(cert_id))
                    domain = cert_info.get("name_value")
                    if domain:
                        for d in domain.splitlines():
                            yield d.lower()

    async def query(self,domain):
        response = self.request_url(domain)
        if response.status_code is 200:
            result = self.parse_results(response,domain)
            return result