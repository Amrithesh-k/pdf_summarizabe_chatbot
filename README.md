# Content Engine Chatbot Documentation

Welcome to the documentation for the Content Engine Chatbot. This chatbot analyzes and compares multiple PDF documents using Retrieval Augmented Generation (RAG) techniques. It utilizes various technologies and frameworks to enhance document analysis and insight generation.

## Overview

The Content Engine Chatbot is designed to:

- Analyze multiple PDF documents.
- Identify and highlight differences between documents.
- Utilize Retrieval Augmented Generation (RAG) techniques for document insights.

## Technologies Used

### Backend Framework

The backend of the Content Engine Chatbot is built using **LangChain**, a framework known for its natural language processing capabilities and integration with various AI models.

### Frontend Framework

For the user interface, **Streamlit** is used to create an interactive frontend that allows users to interact with the chatbot and view document comparisons.

### Vector Store

**Faais** serves as the vector store, providing efficient storage and retrieval of document embeddings and representations.

### Embedding

**Cohere** embeddings are used to encode and compare document content, enabling the chatbot to identify similarities and differences between PDF documents.

### Language Models

The chatbot leverages both **LLama3 Local** and **Groq_api (LLama3)** as LLMS (Large Language Models) for generating insights and responses based on document analysis.

## Features

### 1. Document Comparison

The chatbot compares multiple PDF documents and highlights their differences using advanced RAG techniques.

### 2. Insight Generation

It generates insights from analyzed documents, providing summaries, key points, and similarities.

### 3. Interactive Interface

Streamlit frontend provides an intuitive interface for users to upload documents, view comparisons, and interact with generated insights.

## Getting Started

To run the Content Engine Chatbot locally or deploy it, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/content-engine-chatbot.git
   cd content-engine-chatbot


2. **Installation:**
   ```bash
   pip install -r requirements.txt

3. **Run the Chatbot:**
    ```bash
    streamlit run app.py