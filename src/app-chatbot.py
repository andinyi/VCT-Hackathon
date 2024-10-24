import boto3
import json
import os
from botocore.config import Config
import datetime
import time
import base64
import invokeAgent

import streamlit as st

config = Config(read_timeout=5000)

appY = boto3.client('bedrock-agent-runtime', region_name='us-east-1', config=config)
agentId = 'K71TUFEQVD'
agentAliasId = '7DJEPLGFQ1'

appZ = boto3.client('bedrock-runtime', region_name='us-east-1')

st.title("JettReviveMe Chatbot 🤖")

sessionId = str(datetime.datetime.now()).replace(' ', '')

if 'sessionId' not in st.session_state:
    st.session_state.sessionId = sessionId

if 'agentCalled' not in st.session_state:
    st.session_state.agentCalled = False

#st.subheader(f'Current SessionId is :orange[{st.session_state.sessionId}]') 

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])

if temp := st.chat_input("Type your input here"):
    #if(temp[0] == '!'):
    #    sessionId = temp[1:]
    #    st.session_state.sessionId = sessionId
    #    st.subheader(f'Switching SessionId Into : :orange[{st.session_state.sessionId}]') 
    #else:
        st.chat_message("user").markdown(temp)
        st.session_state.messages.append({"role" : "user", "content" : temp})

        if('build' not in temp.lower() and st.session_state.agentCalled == False):
            handle = appZ.invoke_model(modelId = "anthropic.claude-3-haiku-20240307-v1:0", body = 
                json.dumps(
                    {
                        "anthropic_version" : "bedrock-2023-05-31",
                        "max_tokens" : 1000,
                        "temperature" : 0.2,
                        "system" : "You are a nice and helpful chatbot that will answer queries outside of the functional agent calls. Feel free to answer and have conversations with the user.",
                        "messages" : [
                            {
                                "role" : "user",
                                "content" : [{"type" : "text", "text" : temp}]
                            }
                        ]
                    }))
            text = json.loads(handle["body"].read())['content'][0]["text"]
            st.chat_message('assistant').markdown(text)
            st.session_state.messages.append({"role" : "assistant", "content" : f'{text}'})
        else:
            st.session_state.agentCalled = True
            text = invokeAgent.invokeAgent(agentId, agentAliasId, str(st.session_state.sessionId).replace(' ',''), temp + " Create the best/strongest team possible. Ensure you 5 players in your final response. Explain strategies that this team can/will execute well and some weaknesses they may struggle with.")
            st.session_state.status.update(label='Thoughts and prayers completed, streaming final response 💡', state='complete')
            st.chat_message('assistant').write_stream(invokeAgent.streamFormat(text))
            st.session_state.messages.append({"role" : "assistant", "content" : f'{text}'})


