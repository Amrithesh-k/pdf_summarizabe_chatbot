import streamlit as st
import os 
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import Chroma
from streamlit_chat import message
import time


from dotenv import load_dotenv

load_dotenv()

#load groaq

groq_api_key=os.environ['GROQ_API_KEY']
cohere_api_key=os.environ['COHERE_API_KEY']

if "vector" not in st.session_state:
    st.session_state.embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key)
    st.session_state.loader = PyPDFLoader("files/result.pdf")
    st.session_state.docs=st.session_state.loader.load()

    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
    st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)


st.title("RAG CHATBOT 🤖")

llm=ChatGroq(groq_api_key=groq_api_key,
             model_name="Llama3-8b-8192")

prompt= ChatPromptTemplate.from_template(
"""
Answer the following question based  only on the provided context.
Think step by step before providing  a detailed answer.
Please provide the most accurate reponce based on the provided question.
<context>
{context}
</context>
Question: {input}
""")



document_chain =create_stuff_documents_chain(llm,prompt)
retriever= st.session_state.vectors.as_retriever()
retrival_chain = create_retrieval_chain(retriever,document_chain)

prompt = st.text_input("Enter your question here!")

if 'user_input' not in st.session_state:
    st.session_state['user_input'] = []
 
if 'response' not in st.session_state:
    st.session_state['response'] = []

if prompt:
    start = time.process_time()
    response = retrival_chain.invoke({"input":prompt})
    print("Response time :",time.process_time()-start)
    output=response['answer']
    st.session_state.response.append(prompt)
    st.session_state.user_input.append(output)  

    with st.expander("Document Similarity Search"):
        for i,doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("-------------------------------------------------")



message_history = st.empty()
 
if st.session_state['user_input']:
    for i in range(len(st.session_state['user_input']) - 1, -1, -1):
        
        # This function displays user input
        
        message(st.session_state["user_input"][i],
                key=str(i), avatar_style="icons")
        
        # This function displays response
        
        message(st.session_state['response'][i],
                avatar_style="miniavs", is_user=True
                , key=str(i) + 'data_by_user')