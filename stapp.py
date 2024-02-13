import streamlit as st 
import json
import requests
import asyncio
from utils.helpers import UserAgent
from searches.ip import IPaddress
from searches.username import Username
from searches.email import Email
from searches.domain import Domain
import pandas as pd
import numpy as np


USER_AGENT = UserAgent().user_agent
requests.utils.default_user_agent = lambda: USER_AGENT
Methods = ["email","username","IP","Domain"]

st.write("Hello, Streamlit!")
type = st.selectbox("Select data type",options=Methods)
data = st.text_input("Enter you search query")


if st.button("Search"):
        if type == "email":

            output = Email().search(data)

            st.dataframe(output)
            
            #return render_template("gmail_results.html", hits=dict(google=data["gdata"], json_str=data["Jresults"],accounts=data["hits"]))
    
        
        elif type == "username":
            output = Username().search(data)
            st.dataframe(output)
            #return render_template("username_results.html", hits=dict(results=hits, json_str=json.dumps(hits)))

        elif type == "IP":
            geo2ip,ipinfo,shodan_data = IPaddress().search(data)
            st.json(geo2ip)
            st.json(ipinfo.json())
            st.json(shodan_data)
            #return render_template("ip_results.html", hits=dict(results=ipinfo.json(), json_str=json.dumps(ipinfo.json()),shodan=shodan_data))
        
        elif type == "Domain":

            output =  Domain().search(data)
            for v in output:
                 st.json(v)
            #return render_template("domain_results.html", hits=dict(results=Domain_data["result"], json_str=Domain_data["JSON"],shodan=Domain_data["Shodan"],dns_hists=Domain_data["HistoricalDNS"],wayback=Domain_data["Wayback"]))

