import boto3
from botocore.client import Config
import os
import streamlit as st
import langchain
from langchain.llms.bedrock import Bedrock
from langchain.retrievers import AmazonKnowledgeBasesRetriever
from langchain.chains import RetrievalQA
from langchain_community.chat_models import BedrockChat
from langchain.memory import ConversationBufferWindowMemory
from getdata import getdata
import time
from datetime import *



def transfertoTS(time):
  timestamp1 = int(f.timestamp())
  return timestamp1
  
  

def get_memory(): #create memory for this chat session
    
    memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True) #Maintains a history of previous messages
    
    return memory

def analysis_chat():
    #st.title("這是title") 
    #st.write("Hi 有什麼可以幫助你的嗎?")
    
    with st.chat_message("assistant"):
        st.write("Hi! 我是機器人，有什麼可以幫助你的嗎?")
    
    REGION = "us-west-2"

    # Setup bedrock
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name=REGION,
    )
    
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id="AKP5CBSIE6",
        retrieval_config={
            "vectorSearchConfiguration": {"numberOfResults": 4}},
    )
    model_kwargs_claude = {
        # "prompt":"請輸入想要查詢的設備用電量", 
        "temperature": 0, "top_k": 10, 
        #"max_tokens_to_sample": 3000
        
    }

    
    
    llm = BedrockChat(
        client=bedrock_runtime, 
        region_name='us-west-2',
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs=model_kwargs_claude
    )
    
    ### Complete this section by filling out the TODO values
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        

    if prompt := st.chat_input("Ask me a question"):
        with st.chat_message("human"):
            st.markdown(prompt)
            
        st.session_state.messages.append({"role": "human", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner('Processing...'):
                message_placeholder = st.empty()
                full_response = ""
                # answer = qa(prompt)
                answer = qa(prompt + "Just tell me its nodeID. Don't give me another words")
                start_time = qa(prompt + "Find the start time of the question I want to ask from what I said. Then back to 8 hours. And convert to 'yyyy MM dd HH'. And answer is list type. Must don't give me words except time")
                # start_time = qa(prompt + "Just tell me the start time I ask you and convert to timestamp and 'yyyy-hh-dd hh:mm' ,Don't give me another words.")
                end_time = qa(prompt + "Find the end time of the question I want to ask from what I said. Then back to 8 hours. And convert to 'yyyy MM dd HH'.Must don't give me words except time")
                # end_time = qa(prompt + "Just tell me the end time I ask you and convert to timestamp 'yyyy-hh-dd hh:mm' ,Don't give me another words.")
                full_response = answer['result'] + start_time['result'] + end_time['result']
                # full_response = answer['result']
                message_placeholder.markdown(full_response)
                
                
                
                res = getdata(answer)
                tsfrom = transfertoTS(start_time)
                tsto = transfertoTS(end_time)
                
                
                
                
                
                
                
                
                
                
                
                
                
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# def query_data():
#     #發出request
#   request_body = {
#   "timeoffset": "00:00:00",
#   "timezone": "Asia/Hong_Kong",
#   "range": { "from": rfrom , "to": rto },
#   "language": "zh",
#   "targets": [
#   {
#       "target": "energy",
#       "queryType": "bems_multi",
#       "apmOrgId": 1,
#       "resourceId": answer,
#       "subitemCode": "01000",
#       "formulaType": 183,
#       "formulaUnit": scale
#   }
#   ]
#   }
    
    
    
    # if 'memory' not in st.session_state: 
    #     st.session_state.memory = solve_chat_bot.solve_chat_bot_memory() #

    # # add
    # if 'chat_history' not in st.session_state: 
    #     st.session_state.chat_history = [] 

    # if 'vector_index' not in st.session_state: 
    #     with st.spinner("Indexing document..."): 
    #         st.session_state.vector_index = glib.get_index() 

    # for message in st.session_state.chat_history: 
    #     with st.chat_message(message["role"]): 
    #         st.markdown(message["text"]) 

    # input_text = st.chat_input("請輸入您的問題，例如：今天的總用電量是多少?") 
    # if input_text: 
    
    #     with st.chat_message("user"): 
    #         st.markdown(input_text) 
    #     st.session_state.chat_history.append({"role":"user", "text":input_text}) 
    
    #     chat_response = solve_chat_bot.solve_chat_bot_converation(input_text=input_text, memory=st.session_state.memory)
    
    #     with st.chat_message("assistant"): 
    #         st.markdown(chat_response) 
    
    #     st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) 



    


