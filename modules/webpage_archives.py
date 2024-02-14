import requests 


class wayback:
    async def query(self,domain):
        url = "https://web.archive.org/web/timemap/json?url={}".format(domain)

        response = requests.get(url)
        if response.status_code == 200:
            return response.json()


""" response = get_wayback("dr.dk")
print(len(response))
first = response[1][1]
print(first)
for i in response:
    print(i) """