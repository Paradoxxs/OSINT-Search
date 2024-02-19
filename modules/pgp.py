
class pgp():
    meta = {"description": "Query common PGP servers for email addresses"}
    options = {
        "search_urls": [
            "https://keyserver.ubuntu.com/pks/lookup?fingerprint=on&op=vindex&search=<query>",
            "http://the.earth.li:11371/pks/lookup?fingerprint=on&op=vindex&search=<query>",
        ]
    }
    options_desc = {"search_urls": "PGP key servers to search"}


    async def query(self, email):
        results = set()
        for url in self.config.get("search_urls", []):
            url = url.replace("<query>", self.helpers.quote(email))
            response = await self.helpers.request(url)
            if response is not None:
                for email in self.helpers.extract_emails(response.text):
                    email = email.lower()
                    if email.endswith(email):
                        results.add(email)
        return results