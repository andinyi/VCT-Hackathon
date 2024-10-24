import streamlit as st

st.logo("https://public-bucket-andy.s3.us-east-1.amazonaws.com/pumpkinLong.PNG", size='large', link="http://jettreviveme.com/", icon_image="https://public-bucket-andy.s3.us-east-1.amazonaws.com/pumpkin.png")

About_page = st.Page("About.py", title='About', icon=':material/dashboard:')
Source_page = st.Page("sources.py", title='Sources', icon=':material/view_timeline:')
App_page = st.Page("app-chatbot.py", title='App', icon=':material/chat:')

pg = st.navigation({
    "Information and About" : [About_page, Source_page],
    "WebApp" : [App_page]
})

pg.run()