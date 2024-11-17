import streamlit as st
from streamlit_chat import message
#from langchain.chat_models import ChatOpenAi
from langchain_openai import ChatOpenAI
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

import os

os.environ["OPEN_API_KEY"] = st.secrets["OPEN_API_KEY"]

#Initialize session state variables
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

if "messages" not in st.session_state.keys(): #Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistannt", "content": "How can I help you today"}
    ]

# Initialialize ChatOpenAI and ConversationChain
# llm = ChatOpenAI(modelname = "gpt-4o-mini")
# llm = ChatGoogleGenerativeAI(model = "gemini-pro")
llm = ChatOpenAI(model = "meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
                 openai_api_key = st.secrets["e1d9f69e64ad1c04046de519eb7c6ed1fb12c14d0ca6e7691cf94b52d5af30c2"],
                 openai_api_base = "https://api.together.xyz/v1"       
)

conversation = ConversationChain(memory = st.session_state.buffer_memory, llm = llm)

#Create User Interface

st.title("Conversation Chatbot")
st.subheader("Simple Chat Interface for LLMs by GK")

if prompt := st.chat_input("Your Question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for messages in st.session_state.messages: # Display prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assitant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking"):
            response = conversation.predict(imput = prompt)
            st.write(response)
            message = {"role": "assitant", "content": response}
            st.session_state.messages.append(message) # Add response to message history
