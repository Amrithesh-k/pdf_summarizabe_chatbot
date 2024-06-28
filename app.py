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
import time


from dotenv import load_dotenv

load_dotenv()

#load groaq

groq_api_key=os.environ['GROQ_API_KEY']
cohere_api_key=os.environ['COHERE_API_KEY']

if "vector" not in st.session_state:
    st.session_state.embeddings = CohereEmbeddings(cohere_api_key=cohere_api_key)
    st.session_state.loader = PyPDFLoader("files/goog-10-k-2023 (1).pdf")
    st.session_state.docs=st.session_state.loader.load()

    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)

    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:50])
    st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)


st.title("CHATBOT TEST")

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

prompt = st.text_input("Enter your prompt here!")


if prompt:
    start = time.process_time()
    response = retrival_chain.invoke({"input":prompt})
    print("Response time :",time.process_time()-start)
    st.write(response['answer'])

    with st.expander("Document Similarity Search"):
        for i,doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("-------------------------------------------------")

