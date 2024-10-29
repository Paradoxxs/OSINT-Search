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
from streamlit_flow import streamlit_flow
from streamlit_flow.elements import StreamlitFlowNode, StreamlitFlowEdge
from streamlit_flow.state import StreamlitFlowState
from streamlit_flow.layouts import TreeLayout

from uuid import uuid4



st.set_page_config(page_title="OSINT-search", page_icon=":dog:",layout="wide",initial_sidebar_state="expanded",menu_items={'About': "This is in WIP"})
st.markdown("# OSINT Search")
st.write("Hello, OSINT practicer!")


username_search = Username()
ip_search = IPaddress()
domain_search = Domain()
email_search = Email()



USER_AGENT = UserAgent().user_agent
requests.utils.default_user_agent = lambda: USER_AGENT
Methods = ["email","username","IP","Domain","phone"]


def present_data(k, v):
    st.write(k)
    if k in ["subdomains", "usernames", "emails", "Email_registration", "tls_certs", "leak"]:
        st.dataframe(v)
    elif k in ["google_analytic_id", "TLS_jarm","Google_analytic_shared"]:
        st.write(v)
    elif k in ["WHOIS", "hostIO", "google", "nmap", "hist_dns", "wayback", "Email_reputation","shodan_ip","ip_Whois"]:
        st.json(v, expanded=False)


def present_data_in_columns(search_output, present_func):
    num_results = len(search_output)
    num_columns = 2  # You can adjust this number based on your preference

    # Calculate the number of items to be displayed in each column
    items_per_column = num_results // num_columns
    remainder = num_results % num_columns

    columns = st.columns(num_columns)

    item_index = 0
    for col_index in range(num_columns):
        num_items = items_per_column + 1 if col_index < remainder else items_per_column
        with columns[col_index]:
            for _ in range(num_items):
                if item_index < num_results:
                    k, v = search_output[item_index]
                    present_func(k, v)
                    item_index += 1




def graphview(data,output):

    if 'curr_state' not in st.session_state:
        nodes = []
        edges = []
        st.session_state.curr_state = StreamlitFlowState(nodes,edges)

    head_node = StreamlitFlowNode("1",(0,0),{"content": data}, 'default', 'right', 'left')    
    st.session_state.curr_state.nodes.append(head_node)

    
    for k, v in output:
        create_node_edge(head_node,v)

    
    st.session_state.curr_state = streamlit_flow('flow', 
                    st.session_state.curr_state, 
                    layout=TreeLayout(direction='right'), 
                    fit_view=True, 
                    height=500, 
                    enable_node_menu=True,
                    enable_edge_menu=True,
                    enable_pane_menu=True,
                    show_minimap=True, 
                    hide_watermark=True, 
                    allow_new_edges=True,
                    min_zoom=0.1)
    st.rerun()

def create_node_edge(parent, point):
    new_node = StreamlitFlowNode(str(uuid4()),(0,0),{"content": point}, 'default', 'right', 'left')
    st.session_state.curr_state.nodes.append(new_node)
    new_edge = StreamlitFlowEdge(f"{parent.id}-{new_node.id}", parent.id, new_node.id, animated=True)
    st.session_state.curr_state.edges.append(new_edge)

type = st.selectbox("Select data type",options=Methods)
data = st.text_input("Enter you search query")




if st.button("Search"):
        search_output = []

        if type == "email":
            # Split email
            username,domain = splitEmail(data)

            # Lookup email
            output = asyncio.run(email_search.search(data))
            for k,v in output.items():
                search_output.append((k, v))

            # Lookup username
            usernames = asyncio.run(username_search.search(username))
            for k,v in usernames.items():
                search_output.append((k, v))

            # Lookup domain
            if not any(domain.split(".")[0] == email for email in public_emails()):
                domain_output = asyncio.run(domain_search.search(domain))
                for k,v in domain_output.items():
                    search_output.append((k, v))

        elif type == "username":
            output = asyncio.run(username_search.search(data))
            for k,v in output.items():
                search_output.append((k, v))

        elif type == "IP":
            output = asyncio.run(ip_search.search(data))
            for k,v in output.items():
                search_output.append((k, v))

        elif type == "Domain":

            output = asyncio.run(domain_search.search(data))
            for k,v in output.items():
                search_output.append((k, v))

        elif type == "phone":
            output = Phone.search(data)
            if output:
                st.write(output)

        #graphview(data, search_output)

        present_data_in_columns(search_output, present_data)