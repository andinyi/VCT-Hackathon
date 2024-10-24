import streamlit as st

st.logo("pumpkinLong.png", size='large', link="http://jettreviveme.com/", icon_image="pumpkin.png")

About_page = st.Page("About.py", title='About', icon=':material/dashboard:')
Source_page = st.Page("sources.py", title='Sources', icon=':material/view_timeline:')
App_page = st.Page("app-chatbot.py", title='App', icon=':material/chat:')

pg = st.navigation({
    "Information and About" : [About_page, Source_page],
    "WebApp" : [App_page]
})

pg.run()