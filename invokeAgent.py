import boto3
import boto3.exceptions
import botocore.exceptions
import time
from botocore.config import Config
import json

import streamlit as st

config = Config(read_timeout = 5000)

appY = boto3.client('bedrock-agent-runtime', region_name='us-east-1', config=config)

agentId = 'K71TUFEQVD'

agentAliasId = '7DJEPLGFQ1'

sessionId = 'andy'

def streamFormat(input, color=None):
    if color:
        yield f":{color}["
    for word in input.split(" "):
        yield word + " "
        time.sleep(0.05)
    if color:
        yield "]"
def invokeAgent(agent_id, agent_alias_id, session_id, prompt):
    try:
        response = appY.invoke_agent(
            agentId = agent_id,
            agentAliasId = agent_alias_id,
            sessionId = session_id,
            inputText = prompt,
            enableTrace = True
        )

        completion = ""
        
        if 'debug' not in st.session_state:
            st.session_state.debug = []

        for event in response.get("completion"):
            try:
                chunk = event['chunk']
                completion += chunk['bytes'].decode()
            except KeyError:
                try:
                    try:
                        debugText = event['trace']['trace']['orchestrationTrace']['invocationInput']
                        if debugText: 
                            st.session_state.debug.append(debugText)
                    except KeyError:
                        pass

                    if 'status' not in st.session_state:
                        st.session_state.status = st.status('Thinking... 🤔', state='running')

                    st.session_state.status.update(label='Thinking... 🤔', state='running')
                    rationale = event['trace']['trace']['orchestrationTrace']['rationale']['text']
                    st.session_state.status.update(label='Completed thought, streaming current step / response 📝', state='complete')
                    st.chat_message('assistant').write_stream(streamFormat(rationale))
                    st.session_state.pop('status', None)
                    st.session_state.messages.append({"role" : "assistant", "content" : rationale})
                    if len(st.session_state.debug) > 0:
                        with st.expander("debug & trace"):
                            st.markdown(st.session_state.debug[-1])
                        st.session_state.debug = []

                except KeyError:
                    pass
    
    except botocore.exceptions.ClientError as e:
            st.write(f"Couldn't invoke agent. {e}")
            raise

    return completion