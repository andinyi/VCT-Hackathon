import streamlit as st

About_page = st.Page("About.py", title='About', icon=':material/dashboard:')
App_page = st.Page("app-chatbot.py", title='App', icon=':material/chat:')

pg = st.navigation([About_page, App_page])

pg.run()