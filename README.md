# llama-gg-v01

## **Overview**

This application is a Conversational Retrieval System built using Flask, Pinecone, Replicate, and LangChain. It is designed to process and respond to user queries in a conversational manner, utilizing advanced NLP and vector database technologies.

## **Features**

- Conversational interface for user queries.
- Integration with Pinecone for vector database handling.

- Utilization of Replicate with the Llama2 model for language understanding and response generation.
- LangChain for conversational retrieval, providing context-aware answers.
- PDF document processing and embedding for content-based query answering.

## **Requirements**

- Python 3.x
- Flask
- Pinecone API key
- Replicate API token
- HuggingFace
- LangChain and its dependencies
- Internet connection for API access

## **Installation**

1. **Clone the Repository**:
    
    ```bash
    bashCopy code
    git clone [repository-url]
    cd [repository-directory]
    
    ```
    
2. **Install Dependencies**:
    
    ```bash
    bashCopy code
    pip install flask pinecone langchain huggingface_hub
    
    ```
    
3. **Environment Variables**:
    - Set your Replicate API token and Pinecone API key in the **`initialize`** function within the application.
4. **Document Preparation**:
    - Place the PDF document you want to use in the project directory and ensure it is named **`doc.pdf`**.

## **Usage**

1. **Start the Application**:
    
    ```bash
    bashCopy code
    python [app_filename].py
    
    ```
    
2. **Access the Application**:
    - Open a web browser and navigate to **`http://localhost:5000`**.
3. **Interact with the Chatbot**:
    - Use the chat interface to input your queries and receive responses.

## **API Endpoints**

- **`/`**: The home page serving the chat interface.
- **`/chat`**: POST endpoint to send user input and receive chatbot responses.
- **`/is_initialized`**: GET endpoint to check if the Pinecone vector database is initialized.

## **Initialization Process**

- The application initializes the Pinecone vector database and sets up the conversational retrieval chain in a separate thread at startup.

## **Notes**

- The application is set for production with **`debug`** set to **`False`**.
- Ensure you have the necessary API tokens and keys for Pinecone and Replicate.
- This system is designed for English language processing.

## **Troubleshooting**

- Ensure all required modules are installed and properly configured.
- Check API tokens and keys for validity and proper placement in the code.
- For issues related to Pinecone or Replicate, refer to their respective documentation.
