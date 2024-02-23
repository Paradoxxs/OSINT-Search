import streamlit as st 
import requests
import asyncio
from utils.helpers import UserAgent
from searches.ip import IPaddress
from searches.username import Username
from searches.email import Email
from searches.domain import Domain
from utils.helpers import splitEmail,public_emails
from searches.phone import Phone

##TODO present data in a nice way, e.g. 2-3 columns
st.set_page_config(page_title="OSINT-search", page_icon=":dog:",layout="wide",initial_sidebar_state="expanded",menu_items={'About': "This is in WIP"})
st.markdown("# Main page")
st.write("Hello, OSINT!")


username_search = Username()
ip_search = IPaddress()
domain_search = Domain()
email_search = Email()



USER_AGENT = UserAgent().user_agent
requests.utils.default_user_agent = lambda: USER_AGENT
Methods = ["email","username","IP","Domain","phone"]


##TODO present data in 2-3 coloumns to save space.
def present_data(k,v):
    st.write(k)
    if k == "subdomains":
        st.dataframe(v)
    elif k == "shodan_ip":
        st.write(v)
    elif k == "usernames":
        st.dataframe(v)
    elif k == "emails":
        st.dataframe(v)
    elif k == "Email_registration":
        st.dataframe(v)
    elif k == "ip_Whois":
        st.write(v)
    elif k == "WHOIS":
        st.json(v,expanded=False)
    elif k == "hostIO":
        st.json(v,expanded=False)
    elif k == "google":
        st.json(v)
    elif k == "nmap":
        st.json(v)
    elif k == "google_analytic_id":
        st.write(v)
    elif k == "hist_dns":
        st.json(v,expanded=False)
    elif k == "wayback":
        st.json(v,expanded=False)
    elif k == "tls_certs":
        st.dataframe(v)
    elif k == "TLS_jarm":
        st.write(v)


type = st.selectbox("Select data type",options=Methods)
data = st.text_input("Enter you search query")


if st.button("Search"):
        if type == "email":
            # Split email
            username,domain = splitEmail(data)

            # Lookup email
            output = asyncio.run(email_search.search(data))
            for k,v in output.items():
                present_data(k,v)

            # Lookup username
            usernames = asyncio.run(username_search.search(username))
            for k,v in output.items():
                present_data(k,v)

            # Lookup domain
            if not any(domain.split(".")[0] == email for email in public_emails()):
                domain_output = asyncio.run(domain_search.search(domain))
                for k,v in domain_output.items():
                    present_data(k,v)

        elif type == "username":
            output = asyncio.run(username_search.search(data))
            for k,v in output.items():
                present_data(k,v)

        elif type == "IP":
            output = asyncio.run(ip_search.search(data))
            for k,v in output.items():
                present_data(k,v)

        elif type == "Domain":

            output = asyncio.run(domain_search.search(data))
            for k,v in output.items():
                present_data(k,v)

        elif type == "phone":
            output = Phone.search(data)
            if output:
                st.write(output)
                

