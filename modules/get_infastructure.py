import requests
from pprint import pprint
from datetime import datetime
import whois
import requests
import pandas as pd

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"






def get_whois(domain):
    result = whois.whois(domain)
    return result








""" results = get_shodan_favicon_search("dr.dk")
print(results)
for result in results:
    print(result["hostnames"])
    print(result["ip_str"])
    print("Break\n") """








def get_wayback_count(domain):
    url = "https://web.archive.org/web/timemap/json?url={}".format(domain)

    response = requests.get(url,headers={"User-Agent": useragent})
    if response.status_code == 200:
        data =response.json()
        df = pd.DataFrame(data[1:])
        df.columns = data[0]
        df.drop_duplicates()
        df =df.drop(["urlkey"],axis=1)
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M%S')

        data = {
            "First": df["timestamp"].min().strftime("%Y-%m-%d %H:%M:%S"),
            "Last": df["timestamp"].max().strftime("%Y-%m-%d %H:%M:%S"),
            "Total": len(df),
            "Domain": domain
        }

        return data