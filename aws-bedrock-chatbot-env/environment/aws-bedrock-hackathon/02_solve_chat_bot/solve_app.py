import boto3
from botocore.client import Config
import os
import streamlit as st
import langchain
from langchain.llms.bedrock import Bedrock
from langchain.retrievers import AmazonKnowledgeBasesRetriever
from langchain.chains import RetrievalQA
from langchain_community.chat_models import BedrockChat
from langchain import LLMChain
from langchain.memory import ConversationBufferWindowMemory

def get_memory(): #create memory for this chat session
    
    memory = ConversationBufferWindowMemory(memory_key="messages", return_messages=True) #Maintains a history of previous messages
    
    return memory


def solve_chat():
    
    with st.chat_message("assistant"):
        st.write("Hi! 我是系統說明機器人，有什麼可以幫助你的嗎?")
    
    REGION = "us-west-2"

    # Setup bedrock
    bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name=REGION,
    )
    
    retriever = AmazonKnowledgeBasesRetriever(
        knowledge_base_id="IS2PZCVTJ9",
        retrieval_config={
            "vectorSearchConfiguration": {"numberOfResults": 4}},
    )
    # model_kwargs_claude = {
    #     "message": "\n\nHuman: You are 研寶, an ADVANTECH AI assistant.\
    #         Your goal is to provide informative and substantive responses with both Tradionnal Chinese and English \
    #         to queries \n\nAssistant:",
    #     "system": 
    #         "You are 研寶, an ADVANTECH AI assistant.\
    #         Your goal is to provide informative and substantive responses with both Tradionnal Chinese and English \
    #         to queries", 
    #     "temperature": 0,
    #     "top_p": 1,
    #     "top_k": 250,
    #     "max_tokens_to_sample": 2000,
    # }

    model_kwargs_claude = {
        "max_tokens": 1024, 
        "system": 
            "You are 研寶, an ADVANTECH AI assistant.\
            Your goal is to provide informative and substantive responses with both Tradionnal Chinese and English \
            to queries", 
        "messages": [{"role": "user", "content": "Hello, 研寶"}], 
        "anthropic_version": "bedrock-2023-05-31",
        "temperature": 0,
        "top_p": 1,
        "top_k": 250,
    }
    
    
    llm = BedrockChat(
        client=bedrock_runtime, 
        region_name='us-west-2',
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs=model_kwargs_claude
    )
    # 檢索型問答
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    
    if 'memory' not in st.session_state: 
        st.session_state.memory = get_memory()

    # add
    if 'chat_history' not in st.session_state: 
        st.session_state.chat_history = [] 
    
    # if "messages" not in st.session_state:
    #     st.session_state.messages = []
    
    for message in st.session_state.chat_history: 
        with st.chat_message(message["role"]): 
            st.markdown(message["text"])
    
    prompt = st.chat_input("Ask me a question")

    if prompt:
        
        with st.chat_message("Human"):
            st.markdown(prompt)
            
        st.session_state.chat_history.append({"role": "Human", "text": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner('Processing...'):
                message_placeholder = st.empty()
                full_response = ""
                answer = qa(prompt)
                full_response = answer['result']
                message_placeholder.markdown(full_response)
                
        st.session_state.chat_history.append({"role": "assistant", "text": full_response})


    
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



    


