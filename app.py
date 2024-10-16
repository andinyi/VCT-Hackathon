import boto3
import json
import os

from langchain.chains import LLMChain
from langchain_aws import ChatBedrock
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.globals import set_verbose, set_debug

import streamlit as st

appY = boto3.client('bedrock-runtime', region_name='us-east-1')

modelId = "amazon.titan-text-express-v1"

llm = ChatBedrock(
    model_id=modelId,
    client=appY,
    verbose=True,
    model_kwargs={"maxTokenCount":8192,"stopSequences":[],"temperature":0.3}
)

memory = ChatMessageHistory()

#Streamlit Initialization

st.title("Valorant VCT Manager")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]): 
        st.markdown(message["content"])

if "memory" not in st.session_state:
    st.session_state.memory = memory
#start chain

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a helpful assistant. Please assist the user with their question to the best of your ability.
            A summarized history is provided below. Please use this to maintain a memory what has been discussed already. 

            {chat_history}

            Please do your best! I believe in you!
            """,
        ),
        ("user", "{text}"),
    ]
)   

chain = (
    prompt
    | llm
    | StrOutputParser()
)

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: st.session_state.memory,
    input_messages_key="text",
    history_messages_key="chat_history",
)

tmpDebug = ""

def summarize_messages(chain_input):

    stored = memory.messages

    if len(stored) == 0:
        return False
    
    summarize_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            (
                "system",
                """Distill the above chat messages into a summary. Include as many specific details as you can.""",
            ),
        ]
    )

    summarization_chain = summarize_prompt | llm 

    summary_response = summarization_chain.invoke({"chat_history":stored})

    tmpDebug = summary_response

    return True

chain_with_summarization = (
    RunnablePassthrough.assign(messages_summarized=summarize_messages)
    | chain_with_history
)

if temp := st.chat_input("How can I help?"):
    st.chat_message("user").markdown(temp)
    st.session_state.messages.append({"role":"user","content":temp})

    response = chain_with_summarization.invoke({"text":temp}, {"configurable" : {"session_id" : "unused"}})
    st.sidebar.write(st.session_state.memory.messages)

    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    st.session_state.memory.add_user_message(temp)
    st.session_state.memory.add_ai_message(response)
