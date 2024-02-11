from utils.helpers import get_env_var, convert_datetime
from modules.historical_dns import mnemonic
from modules.webpage_archives import wayback
from modules.shodan_search import shodan
from modules.get_infastructure import get_whois, public_emails
import requests
import json

class Domain():
    async def search(domain):
        WHOIS_hits = get_whois(domain)

        #host.io
        hostIO = requests.request("GET", f"https://host.io/api/full/{domain}?token={get_env_var('hostIO_api')}")
        print(hostIO.json())
        result = {**hostIO.json(), **WHOIS_hits}
        # Serialize the result dictionary with the custom encoder
        json_result = json.dumps(result, default=convert_datetime)
        shodan_data = shodan.favicon_search(domain)
        hist_dns_data = mnemonic.query(domain)
        wayback_data = wayback.query(domain)
        
        data = {
            "WhoIs": WHOIS_hits,
            "Shodan": shodan_data,
            "HistoricalDNS": hist_dns_data,
            "Wayback": wayback_data,
            "JSON": json_result,
            "result": result
        }

        if domain not in public_emails():
            #TODO find emails
            print(domain)

        
        return data 