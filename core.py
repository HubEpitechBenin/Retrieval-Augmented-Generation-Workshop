from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import os


def load_environment_variables():
    """Load and validate environment variables."""
    load_dotenv()
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
    
    openai_api_base = os.getenv("OPENAI_API_BASE")
    if openai_api_base is None:
        openai_api_base = "https://api.openai.com/v1"
        print("OPENAI_API_BASE not set, using default OpenAI endpoint.")
    
    model_name = os.getenv("MODEL_NAME")
    if model_name is None:
        raise ValueError("MODEL_NAME is not set in the environment variables.")
    
    if model_name not in ["gpt-3.5-turbo", "gpt-4"]:
        raise ValueError("MODEL_NAME must be either 'gpt-3.5-turbo' or 'gpt-4'.")
    
    return openai_api_key, openai_api_base, model_name

def load_and_split_documents(pdf_path, chunk_size=10000, chunk_overlap=200):
    """Load PDF and split into chunks."""
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(pages)
    
    return chunks

def create_vector_store(chunks, model_name, api_key=None):
    """Create embeddings and vector store."""
    embeddings = OpenAIEmbeddings(
        model=model_name,
        openai_api_key=api_key,
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    return vectorstore

def get_openai_llm(model_name, api_key, api_base, temperature=1.3, max_tokens=500):
    """Configure the OpenAI LLM with appropriate timeouts and error handling."""
    return ChatOpenAI(
        model=model_name,
        openai_api_key=api_key,
        openai_api_base=api_base,
        temperature=temperature,
        max_tokens=max_tokens,
        request_timeout=60,
        max_retries=2
    )

def create_qa_chain(llm, vectorstore):
    """Create the RAG pipeline for question answering."""
    return RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

def ask_question(qa_chain, query):
    """Run a query through the QA chain."""
    return qa_chain.invoke(query)

def pipeline(filename="data/B-SVR-500_project.pdf", user_query="What is the goal of the project in two-three small sentences"):
    """Main function to run the entire pipeline."""
    try:
        # Step 1: Load environment variables
        hf_token, openai_api_key, openai_api_base, model_name = load_environment_variables()
        embedding_model = "text-embedding-3-small"
        
        # Step 2: Load and split documents
        chunks = load_and_split_documents(filename)
        
        # Step 3: Create vector store
        try:
            vectorstore = create_vector_store(chunks, embedding_model, openai_api_key)
        except Exception as e:
            if "Connection" in str(e):
                raise ConnectionError(f"Failed to connect to OpenAI API when creating embeddings. Please check your network connection and API key. Error: {e}")
            raise
        
        # Step 4: Set up the LLM
        llm = get_openai_llm(model_name, openai_api_key, openai_api_base)
        
        # Step 5: Create QA chain
        qa_chain = create_qa_chain(llm, vectorstore)
        
        # Step 6: Ask a question
        try:
            response = ask_question(qa_chain, user_query)
            return response["result"]
        except Exception as e:
            if "Connection" in str(e):
                raise ConnectionError(f"Failed to connect to OpenAI API when querying the model. Please check your network connection and API key. Error: {e}")
            raise
            
    except ConnectionError as e:
        return f"Connection Error: {str(e)}\n\nTroubleshooting tips:\n1. Check your internet connection\n2. Verify your OpenAI API key is valid\n3. Check if the API endpoint URL (OPENAI_API_BASE) is correct\n4. If using a proxy, check proxy settings"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    console.print(Markdown(pipeline(input("Enter the PDF file path: "), input("Enter your question: "))))
