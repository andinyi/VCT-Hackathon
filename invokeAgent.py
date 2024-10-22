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
def invokeAgent(agent_id, agent_alias_id, session_id, prompt, rationaleParser):

    try:
        response = appY.invoke_agent(
            agentId = agent_id,
            agentAliasId = agent_alias_id,
            sessionId = session_id,
            inputText = prompt,
            enableTrace = True
        )

        completion = ""
        
        with st.sidebar.status(":blue[Thinking...]", expanded=True) as status:
            st.write("Don't Rush Me... Please?")
            time.sleep(1)

        for event in response.get("completion"):
            try:
                chunk = event['chunk']
                completion += chunk['bytes'].decode()
            except KeyError:
                try:
                    status.update(label=":blue[Back to thinking...]", state = 'running', expanded = False)
                    rationaleParsed = rationaleParser.invoke_model(modelId = "anthropic.claude-3-haiku-20240307-v1:0", body = 
                        json.dumps(
                        {
                            "anthropic_version" : "bedrock-2023-05-31",
                            "max_tokens" : 1000,
                            "temperature" : 0.1,
                            "system" : "You are a helpful formatting tool that formats the text as if you're explaining it to a judge, please make your explanations brief, short, and concise. Return your response in natural language. DONT: include any introductions or lead-ins, return example SQL Queries, and NEVER Repeat yourself. Return only the formatted text.",
                            "messages" : [
                                {
                                    "role" : "user",
                                    "content" : [{"type" : "text", "text" : event['trace']['trace']['orchestrationTrace']['rationale']['text']}]
                                }
                            ]
                        }))
                    rationale = json.loads(rationaleParsed["body"].read())['content'][0]["text"]
                    status.update(label="Done!", state = 'complete', expanded = False)
                    st.chat_message('ai').write_stream(streamFormat(rationale))
                    st.session_state.messages.append({"role" : "ai", "content" : rationale})
                except KeyError:
                    pass
    
    except botocore.exceptions.ClientError as e:
            st.write(f"Couldn't invoke agent. {e}")
            raise

    return completion
