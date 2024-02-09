import requests
from pprint import pprint
from datetime import datetime
import json
import whois
from shodan import Shodan
import mmh3
import requests
import codecs
import os
from utils.helpers import get_env_var
import pandas as pd

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
api = Shodan(get_env_var("shodan_key"))


def get_mnemonic(domain):
    url = f"https://api.mnemonic.no/pdns/v3/{domain}"

    
    response = requests.get(url, headers={"User-Agent": useragent})
    if response.status_code == 200:
        results = response.json()
        for result in results["data"]:
            result["createdTimestamp_utc"] = datetime.utcfromtimestamp(result["createdTimestamp"] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
            result["lastSeenTimestamp_utc"] = datetime.utcfromtimestamp(result["lastSeenTimestamp"] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
        return results["data"]


def get_wayback(domain):
    url = "https://web.archive.org/web/timemap/json?url={}".format(domain)

    response = requests.get(url,headers={"User-Agent": useragent})
    if response.status_code == 200:
        return response.json()


""" response = get_wayback("dr.dk")
print(len(response))
first = response[1][1]
print(first)
for i in response:
    print(i) """




def get_whois(domain):
    result = whois.whois(domain)
    return result


# https://help.shodan.io/developer-fundamentals/looking-up-ip-info




def get_shodan_favicon_search(domain):
    try:
        response = requests.get("http://www.{}/favicon.ico".format(domain),verify=False)
        favicon = codecs.encode(response.content, 'base64')
        hash = mmh3.hash(favicon)
        results = api.search_cursor("http.favicon.hash:{}".format(hash))   
        
        return results
    except Exception as e:
        print(e)
        return False


""" results = get_shodan_favicon_search("dr.dk")
print(results)
for result in results:
    print(result["hostnames"])
    print(result["ip_str"])
    print("Break\n") """


def get_shodan_IP_services(IP):
    try:
        results = api.host(IP)
        return results
    except Exception as e:
        print(e)
        return False



""" res = get_shodan_IP_services("8.8.8.8")
print(type(res))
print(res["ports"])
print(res["hostnames"])
print(type(res["data"]))
print(res.get("hash", "n/a")) """


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