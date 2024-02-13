import requests
import re
from bs4 import BeautifulSoup
from utils.helpers import get_env_var

class rapiddns():
    meta = {"description": "Query rapiddns.io for subdomains"}

    base_url = "https://rapiddns.io"

    def parse_results(self, r, domain):
        results = set()
        text = getattr(r, "text", "")
        for match in self.helpers.regexes.dns_name_regex.findall(text):
            match = match.lower()
            if match.endswith(domain):
                results.add(match)
        return results

    async def request_url(self, domain):
        url = f"{self.base_url}/subdomain/{domain}?full=1#result"
        response = requests.get(url)
        return response

    async def query(self,domain):
        res = self.request_url(domain)
        if res.status_code is not 200:
            self.verbose(f"Error retrieving reverse whois results (status code: {res.status_code})")
        else:
            results = self.parse_results(res,domain)
            return results






class shodan_dns():
    meta = {"description": "Query Shodan for subdomains", "auth_required": True}
    base_url = "https://api.shodan.io"
    api_key = get_env_var("shodan_key")
    #limited 

    async def request_url(self, query):
        url = f"{self.base_url}/dns/domain/{self.helpers.quote(query)}?key={self.api_key}"
        response = await self.request_with_fail_count(url)
        return response

    def parse_results(self, r, query):
        json = r.json()
        if json:
            for hostname in json.get("subdomains", []):
                yield f"{hostname}.{query}"

    async def query(self,domain):
        results = []
        res = self.request_url(domain)
        if res.status_code is not 200:
            self.verbose(f"Error retrieving reverse whois results (status code: {res.status_code})")
            return results
        else:
            for subdomain in self.parse_results(res,domain):
                results.append(subdomain)
            return results

class dnsdumpster():
    meta = {"description": "Query dnsdumpster for subdomains"}
    base_url = "https://dnsdumpster.com"

    async def query(self, domain):
        ret = []
        # first, get the CSRF tokens
        res1 = await requests.get(self.base_url)
        status_code = res1.status_code
        if status_code in 429:
            self.verbose(f'Too many requests "{status_code}"')
            return ret
        elif status_code is not 200:
            self.verbose(f'Bad response code "{status_code}" from DNSDumpster')
            return ret
        else:
            self.debug(f'Valid response code "{status_code}" from DNSDumpster')
        html = BeautifulSoup(res1.content, "html.parser")
        csrftoken = None
        csrfmiddlewaretoken = None
        try:
            for cookie in res1.headers.get("set-cookie", "").split(";"):
                try:
                    k, v = cookie.split("=", 1)
                except ValueError:
                    self.verbose("Error retrieving cookie")
                    return ret
                if k == "csrftoken":
                    csrftoken = str(v)
            csrfmiddlewaretoken = html.find("input", {"name": "csrfmiddlewaretoken"}).attrs.get("value", None)
        except AttributeError:
            pass

        # Abort if we didn't get the tokens
        if not csrftoken or not csrfmiddlewaretoken:
            self.verbose("Error obtaining CSRF tokens")
            self.errorState = True
            return ret
        else:
            self.debug("Successfully obtained CSRF tokens")

        if self.scan.stopping:
            return

        # Otherwise, do the needful
        subdomains = set()
        res2 = requests.post(f"{self.base_url}/",
            cookies={"csrftoken": csrftoken},
            data={
                "csrfmiddlewaretoken": csrfmiddlewaretoken,
                "targetip": str(domain).lower(),
                "user": "free",
            },
            headers={
                "origin": "https://dnsdumpster.com",
                "referer": "https://dnsdumpster.com/",
            },
        )
        status_code = res2.status_code
        if status_code is not 200:
            self.verbose(f'Bad response code "{status_code}" from DNSDumpster')
            return ret

        html = BeautifulSoup(res2.content, "html.parser")
        escaped_domain = re.escape(domain)
        match_pattern = re.compile(r"^[\w\.-]+\." + escaped_domain + r"$")
        for subdomain in html.findAll(text=match_pattern):
            subdomains.add(str(subdomain).strip().lower())

        return list(subdomains)
    

class binaryedge():

    meta = {"description": "Query the BinaryEdge API", "auth_required": True}
    base_url = "https://api.binaryedge.io/v2"
    headers = {"X-Key": get_env_var("binaryEdge_api")}

    async def request_left(self):
        url = f"{self.base_url}/user/subscription"
        j = (await requests.get(url, headers=self.headers)).json()
        assert j.get("requests_left", 0) > 0

    async def request_url(self, domain):
        # todo: host query (certs + services)
        url = f"{self.base_url}/query/domains/subdomain/{domain}"
        return await requests.get(url, headers=self.headers)

    def parse_results(self, r, query):
        j = r.json()
        return j.get("events", [])
    
    async def query(self,domain):
        req_left = self.request_left()
        if req_left > 0:
            response = self.request_url(domain)
            if response.status_code is 200:
                result = self.parse_results(response,domain)
                return result
            


class certspotter():
    meta = {"description": "Query Certspotter's API for subdomains"}
    base_url = "https://api.certspotter.com/v1"

    def request_url(self, query):
        url = f"{self.base_url}/issuances?domain={query}&include_subdomains=true&expand=dns_names"
        return requests(url)

    def parse_results(self, r, query):
        json = r.json()
        if json:
            for r in json:
                for dns_name in r.get("dns_names", []):
                    yield dns_name.lstrip(".*").rstrip(".")

    async def query(self,domain):
        response = self.request_url(domain)
        if response.status_code is 200:
            result = self.parse_results(response,domain)
            return result
        


class chaos():

    meta = {"description": "Query ProjectDiscovery's Chaos API for subdomains", "auth_required": True}

    options_desc = {"api_key": get_env_var("projectdiscovery_api")}

    base_url = "https://dns.projectdiscovery.io/dns"


    async def request_url(self, domain):
        url = f"{self.base_url}/{domain}/subdomains"
        return await requests.get(url, headers={"Authorization": self.api_key})

    def parse_results(self, r, query):
        j = r.json()
        subdomains_set = set()
        if isinstance(j, dict):
            domain = j.get("domain", "")
            if domain:
                subdomains = j.get("subdomains", [])
                for s in subdomains:
                    s = s.lower().strip(".*")
                    subdomains_set.add(s)
                for s in subdomains_set:
                    full_subdomain = f"{s}.{domain}"
                    if full_subdomain and full_subdomain.endswith(f".{query}"):
                        yield full_subdomain

    async def query(self,domain):
        response = self.request_url(domain)
        if response.status_code is 200:
            result = self.parse_results(response,domain)
            return result
        


        