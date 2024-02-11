from flask import Flask, render_template, request
import json
import requests
import asyncio
from utils.helpers import UserAgent
from searches.ip import IPaddress
from searches.username import Username
from searches.email import Email
from searches.domain import Domain
USER_AGENT = UserAgent().user_agent
requests.utils.default_user_agent = lambda: USER_AGENT
Methods = ["email","username","IP","Domain"]



# Flask consts
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 8080
FLASK_DEBUG = True



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

            data = Email.search(data)
            return render_template("gmail_results.html", hits=dict(google=data["gdata"], json_str=data["Jresults"],accounts=data["hits"]))
    
        
        elif type == "username":
            hits = Username.search(data)
            return render_template("username_results.html", hits=dict(results=hits, json_str=json.dumps(hits)))

        elif type == "IP":
            geo2ip,ipinfo,shodan_data = IPaddress.search(data)
            return render_template("ip_results.html", hits=dict(results=ipinfo.json(), json_str=json.dumps(ipinfo.json()),shodan=shodan_data))
        
        elif type == "Domain":

            Domain_data =  Domain.search(data)
            return render_template("domain_results.html", hits=dict(results=Domain_data["result"], json_str=Domain_data["JSON"],shodan=Domain_data["Shodan"],dns_hists=Domain_data["HistoricalDNS"],wayback=Domain_data["Wayback"]))





if __name__ == '__main__':
    # run the app
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)

