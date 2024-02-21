import requests 


class wayback:
    async def query(self,domain):
        try:
            url = "http://archive.org/wayback/available?url={}".format(domain)

            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        except:
            return 

