import requests
from datetime import datetime


class mnemonic:
    base_url = "https://api.mnemonic.no"
    async def query(self,domain):
        
        try:
            url = f"{self.base_url}/pdns/v3/{domain}"
            response = requests.get(url)
            if response.status_code == 200:
                results = response.json()
                for result in results["data"]:
                    result["createdTimestamp_utc"] = datetime.utcfromtimestamp(result["createdTimestamp"] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
                    result["lastSeenTimestamp_utc"] = datetime.utcfromtimestamp(result["lastSeenTimestamp"] / 1000.0).strftime("%Y-%m-%d %H:%M:%S")
                return results["data"]
        except:
            return