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
from searches.subdomain import Subdomain
from utils.helpers import splitEmail,public_emails

username_search = Username()
ip_search = IPaddress()
domain_search = Domain()
email_search = Email()

USER_AGENT = UserAgent().user_agent
requests.utils.default_user_agent = lambda: USER_AGENT
Methods = ["email","username","IP","Domain"]

st.write("Hello, OSINT!")
type = st.selectbox("Select data type",options=Methods)
data = st.text_input("Enter you search query")


if st.button("Search"):
        if type == "email":

            output = asyncio.run(email_search.search(data))

            st.dataframe(output["hits"])

            for k,v in output.items():
                st.write(k)
                st.dataframe(v)
            username,domain = splitEmail(data)
            if domain != public_emails():
                domain_data = asyncio.run(Domain().search(domain))
                if domain_data != None:
                    data["domain"] = domain_data
            
            #return render_template("gmail_results.html", hits=dict(google=data["gdata"], json_str=data["Jresults"],accounts=data["hits"]))
    
        
        elif type == "username":
            output = asyncio.run(username_search.search(data))
            st.dataframe(output)

        elif type == "IP":
            output = asyncio.run(ip_search.search(data))
            for k,v in output.items():
                st.write(k)
                st.dataframe(v)
            

        elif type == "Domain":

            output = asyncio.run(domain_search.search(data))
            subdomain = asyncio.run(Subdomain().search(data))
            emails = asyncio.run(domain_search.find_emails(data))
            for k,v in output.items():
                st.write(k)
                if k == "shodan":
                    try:
                        for d in v:
                            try:
                                st.datframe(d)
                            except:
                                st.json(d)
                                pass
                    except:
                        pass
                else:
                    try:
                        st.dataframe(v)
                    except Exception  as e:
                        st.json(v)
                        print(e)
                        pass
            st.write("Subdomains")
            st.dataframe(subdomain)
            st.write("Emails")
            st.dataframe(emails)