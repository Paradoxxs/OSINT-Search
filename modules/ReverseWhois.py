import re
import requests
import asyncio

class viewdns:
    """
    Todo: Also retrieve registrar?
    """

    flags = ["affiliates", "passive", "safe"]
    meta = {
        "description": "Query viewdns.info's reverse whois for related domains based on email or name",
    }
    base_url = "https://viewdns.info"

    async def setup(self):
        self.date_regex = re.compile(r"\d{4}-\d{2}-\d{2}")
        return True


    async def query(self, query):
        results = set()
        url = f"{self.base_url}/reversewhois/?q={query}"
        response = requests.get(url)
        if response.status_code is not 200:
            self.verbose(f"Error retrieving reverse whois results (status code: {response.status_code})")

        content = response.content
        from bs4 import BeautifulSoup

        html = BeautifulSoup(content, "html.parser")
        found = set()
        for table_row in html.findAll("tr"):
            table_cells = table_row.findAll("td")
            # make double-sure we're in the right table by checking the date field
            try:
                if self.date_regex.match(table_cells[1].text.strip()):
                    # domain == first cell
                    domain = table_cells[0].text.strip().lower()
                    # registrar == last cell
                    registrar = table_cells[-1].text.strip()
                    if domain and not domain == query:
                        result = (domain, registrar)
                        result_hash = hash(result)
                        if result_hash not in found:
                            found.add(result_hash)
                            results.add(result)
            except IndexError:
                self.debug(f"Invalid row {str(table_row)[:40]}...")
                continue
        return results