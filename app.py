import boto3
import json
import os
from botocore.config import Config
import datetime
import time

import invokeAgent

import streamlit as st

config = Config(read_timeout=5000)

appY = boto3.client('bedrock-agent-runtime', region_name='us-east-1', config=config)
agentId = 'K71TUFEQVD'
agentAliasId = '7DJEPLGFQ1'

appZ = boto3.client('bedrock-runtime', region_name='us-east-1')

st.title("Valorant VCT Manager")

sessionId = str(datetime.datetime.now()).replace(' ', '')

if 'sessionId' not in st.session_state:
    st.session_state.sessionId = sessionId

st.sidebar.write(f'[sessionStateId = :orange[{st.session_state.sessionId}]]')

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])

if temp := st.chat_input("Type your input here"):
    if(temp[0] == '!'):
        sessionId = temp[1:]
        st.session_state.sessionId = sessionId
        st.sidebar.write(f'[sessionStateId = :orange[{st.session_state.sessionId}]]')
    else:
        st.chat_message("user").markdown(temp)
        st.session_state.messages.append({"role" : "user", "content" : temp})
        text = invokeAgent.invokeAgent(agentId, agentAliasId, str(st.session_state.sessionId).replace(' ',''), temp, appZ)
        st.chat_message('ai').markdown(f'{text}')
        st.session_state.messages.append({"role" : "ai", "content" : f'{text}'})
