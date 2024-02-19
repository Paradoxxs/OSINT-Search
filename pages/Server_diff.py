import streamlit as st
from modules.shodan_search import shodan
import asyncio

st.set_page_config(page_title="OSINT-Search", page_icon=":dog:",layout="wide",initial_sidebar_state="expanded",menu_items={'About': "This is in WIP"})

st.write("Comparing of two servers")


ip1 = st.text_input("Server ip")
ip2 = st.text_input("server ip")


if st.button("Search"):
    try:
        server1 = asyncio.run(shodan().IP_services(ip1))
        
        server2 = asyncio.run(shodan().IP_services(ip2))

        st.markdown("Shodan results:")
        col1, col2 = st.columns(2)
        with col1:
          st.write(ip1)
          st.write(server1)
        with col2:
          st.write(ip2)
          st.write(server2)

    except Exception as e:
        st.write(e)
        st.error("Server not found or problem with API")

    