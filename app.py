import dataclasses
from flask import Flask, render_template, request
import json
import os
from pprint import pprint
import requests
from datetime import datetime
import asyncio
from utils.get_emails import get_holehe, get_poastal, get_ghunt
from utils.get_usernames import get_sherlock, get_Wmn
from utils.get_infastructure import get_mnemonic ,get_whois, get_shodan_favicon_search, get_shodan_IP_services, get_wayback_count
from utils.helpers import get_env_var, UserAgent


USER_AGENT = UserAgent().user_agent
requests.utils.default_user_agent = lambda: USER_AGENT
Methods = ["email","username","IP","Domain"]



# Flask consts
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 8080
FLASK_DEBUG = True


def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj


# Supported platforms are declared here
SUPPORTED_PLATFORMS = [
    { "label": "Ghunt", "description": "tjek email mod Google","type": "email", "dev": "github.com/mxrch"},
    { "label": "Holehe", "description": "tjek email mod platforme","type": "email", "dev": "github.com/megadose"},
    {"label": "Poastal", "description": "tjek email mod platforme","type": "email", "dev": "github.com/jakecreps"},
    { "label": "Sherlock", "description": "tjek brugernavn mod platforme","type": "username", "dev": "github.com/sherlock-project"},
    { "label": "WhatsMyName", "description": "tjek brugernavn mod platforme","type": "username", "dev": "github.com/WebBreacher"},
    { "label": "Shodan", "description": "Internet Search engine", "type":"Domain & IP","dev":"shodan.io"},
    { "label": "Host.io", "description": "DNS-lookup", "type":"Domain","dev":"host.io"},
    { "label": "Mnemonic History", "description": "DNS-lookup", "type":"Domain","dev":"passivedns.mnemonic.no"},
    { "label": "Whois Lookup", "description": "DNS-lookup", "type":"Domain","dev":"github.com/richardpenman/whois"},
    { "label": "ipinfo", "description": "IP lookup", "type":"IP","dev":"ipinfo.io"},
    { "label": "Wayback macine", "description": "Webpage archive", "type":"Domain","dev":"archive.org"},
]
SUPPORTED_PLATFORMS.sort(key=lambda x: x["type"].lower())


# create app
app = Flask(__name__)


@app.route("/")
def main():
    """The main route of the app - this is what will be shown when visiting localhost:5000 in the browser"""
    return render_template('index.html', platforms=json.dumps(SUPPORTED_PLATFORMS),datatype=Methods)


@app.route("/api")
def api():
    """
    Called when user performs a search. The request has `tool` and either `email` or `username` as request param.

    The given `username` or `email` is sent to the given `tool`. The response from the tool is returned in a rendered HTML page.

    Parameters
    ----------

    data : str
        The data the user wants to query

    type : str
        The type of data it is

    Returns
    -------
    html_template : str or None
        The HTML string that fits the particular tool.

    """

    # fetch email/username and tool from the API request
    data = request.args.get("data")
    type = request.args.get("type")

    #
    if data:
        if type == "email":

            holehe_data = get_holehe(data)
            # append source to holehe hits
            for hit in holehe_data:
                hit["source"] = "holehe"
            
            poastal_data = get_poastal(data)
            poastal_hits = []
            for domain, exists in poastal_data.items():
                # exists is a str ("true" or "false")
                # so we use json.loads to convert it to a bool
                try:
                    exists = json.loads(exists)
                except:
                    # Poastal returns "unknown" for Facebook - probably from Duolingo - for some reason
                    exists = False
                poastal_hits.append({"source": "poastal", "domain": domain, "exists": exists})



            # combine holehe and poastal hits
            hits = holehe_data + poastal_hits

            if data.endswith("@gmail.com"):
                gdata = asyncio.run(get_ghunt(data))
                if gdata is not False:
                    dict_hits = {item["domain"]: item for item in hits}
                    result = {**dict_hits, **gdata}
                    json_result = json.dumps(result, default=convert_datetime)
                    return render_template("gmail_results.html", hits=dict(google=gdata, json_str=json_result,accounts=hits))
                else:
                    return render_template("email_results.html", hits=dict(results=hits, json_str=json.dumps(hits)))
        


            return render_template("email_results.html", hits=dict(results=hits, json_str=json.dumps(hits)))
        
        elif type == "username":
            sherlock_data = get_sherlock(data)
            sherlock_data.sort(key=lambda x: x["domain"].lower(), reverse=False)
            #append source to sherlock hits
            for hit in sherlock_data:
                hit["source"] = "sherlock"
                #change key url_user til url
                hit["url"] = hit["url_user"]
        
            whm_data = get_Wmn(data)
            whm_data = [dataclasses.asdict(r) for r in whm_data if r.exists]
            whm_data.sort(key=lambda x: x["platform"].lower(), reverse=False)
            # append source to whm_data
            for hit in whm_data:
                hit["source"] = "whm"
                hit["domain"] = hit["platform"]

            # combine sherlock and whm hits
            hits = sherlock_data + whm_data

        
            return render_template("username_results.html", hits=dict(results=hits, json_str=json.dumps(hits)))

        elif type == "IP":
            responses = requests.request("GET", f"https://ipinfo.io/{data}/json")
            shodan_data = get_shodan_IP_services(data)
            return render_template("ip_results.html", hits=dict(results=responses.json(), json_str=json.dumps(responses.json()),shodan=shodan_data))
        
        elif type == "Domain":
            WHOIS_hits = get_whois(data)

            #host.io
            hostIO = requests.request("GET", f"https://host.io/api/full/{data}?token={get_env_var('hostIO_api')}")
            print(hostIO.json())
            result = {**hostIO.json(), **WHOIS_hits}
            # Serialize the result dictionary with the custom encoder
            json_result = json.dumps(result, default=convert_datetime)
            shodan_data = get_shodan_favicon_search(data)
            hist_dns_data = get_mnemonic(data)
            wayback_data = get_wayback_count(data)
            
            return render_template("domain_results.html", hits=dict(results=result, json_str=json_result,shodan=shodan_data,dns_hists=hist_dns_data, wayback=wayback_data))





if __name__ == '__main__':
    # run the app
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)

