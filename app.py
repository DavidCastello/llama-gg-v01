from flask import Flask, request, jsonify, render_template
import json
from threading import Thread

import os
import sys
import pinecone
from langchain.llms import Replicate
from langchain.vectorstores import Pinecone
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain

pinecone_initialized = False  # Global variable to track initialization

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return app.send_static_file('index.html')

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.json
        user_input = data.get('user_input')
        
        # Call your existing Python code to get the chatbot's response
        result = qa_chain({'question': user_input, 'chat_history': chat_history})
        
        # Add the query and the chatbot's answer to the chat history
        chat_history.append((user_input, result['answer']))
        
        return jsonify({'response': result['answer']})
    
    @app.route('/is_initialized')
    def is_initialized():
        return jsonify({'initialized': pinecone_initialized})
    
    # Run initialize() in a separate thread
    init_thread = Thread(target=initialize)
    init_thread.start()
    
    return app

# Global variable to keep track of the chat history
chat_history = []

def initialize():
    global pinecone_initialized

    # Replicate API token
    os.environ['REPLICATE_API_TOKEN'] = "API TOKEN HERE!"

    # Initialize Pinecone
    print("Initializing Pinecone...")
    pinecone.init(api_key='API TOKEN HERE!', environment='gcp-starter')

    # Load and preprocess the PDF document
    print("Loading and preprocessing the PDF document...")
    loader = PyPDFLoader('./doc.pdf')
    documents = loader.load()

    # Split the documents into smaller chunks for processing
    print("Splitting the documents into smaller chunks for processing...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Use HuggingFace embeddings for transforming text into numerical vectors
    print("Transforming text into numerical vectors...")
    embeddings = HuggingFaceEmbeddings()

    # Set up the Pinecone vector database
    print("Setting up the Pinecone vector database...")
    index_name = "llama-gg-v01"
    index = pinecone.Index(index_name)
    vectordb = Pinecone.from_documents(texts, embeddings, index_name=index_name)

    # Initialize Replicate Llama2 Model
    print("Initializing Replicate Llama2 Model...")
    llm = Replicate(
        model="a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5",
        input={"temperature": 0.75, "max_length": 3000}
    )

    # Set up the Conversational Retrieval Chain
    print("Setting up the Conversational Retrieval Chain...")
    global qa_chain
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm,
        vectordb.as_retriever(search_kwargs={'k': 2}),
        return_source_documents=True
    )

    pinecone_initialized = True

if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)