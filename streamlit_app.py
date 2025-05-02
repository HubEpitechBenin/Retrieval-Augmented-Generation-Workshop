import streamlit as st
import time
import os
from core import (
    load_environment_variables,
    load_and_split_documents,
    create_vector_store,
    get_openai_llm,
    create_qa_chain,
    ask_question
)

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="📚",
    layout="centered"
)

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Welcome to the AI Document Assistant! Upload a PDF document to get started."
    }]

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

with st.sidebar:
    st.image("assets/langchain.png", width=250)
    st.title("Document Upload")
    st.divider()
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None:
        with open("temp_upload.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        if st.button("Process Document"):
            with st.spinner("Processing document..."):
                try:
                    openai_api_key, openai_api_base, model_name = load_environment_variables()
                    embedding_model = "text-embedding-3-small"
                    
                    chunks = load_and_split_documents("temp_upload.pdf")
                    vectorstore = create_vector_store(chunks, embedding_model)
                    llm = get_openai_llm(model_name, openai_api_key, openai_api_base)
                    qa_chain = create_qa_chain(llm, vectorstore)
                    
                    st.session_state.uploaded_file = uploaded_file.name
                    st.session_state.vectorstore = vectorstore
                    st.session_state.qa_chain = qa_chain
                    
                    st.success(f"✅ Successfully processed '{uploaded_file.name}'!")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"I've processed *{uploaded_file.name}*. You can now ask questions about it!"
                    })
                except Exception as e:
                    st.error(f"Error processing document: {str(e)}")

    if st.session_state.uploaded_file:
        st.info(f"Current document: {st.session_state.uploaded_file}")
    
    st.caption("Powered by LangChain and OpenAI LLM")

st.title("AI Document Assistant")

for message in st.session_state.messages:
    avatar = "🤓" if message["role"] == "assistant" else "😃"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

def pipeline(prompt):
    if st.session_state.qa_chain is None:
        return "Please upload and process a document first."
    
    response = ask_question(st.session_state.qa_chain, prompt)
    return response["result"]

def pipeline_stream(prompt):
    if st.session_state.qa_chain is None:
        yield "Please upload and process a document first."
    else:
        for chunk in ask_question(st.session_state.qa_chain, prompt)["result"]:
            yield chunk

if prompt := st.chat_input("Ask about the uploaded document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="😃"):
        st.write(prompt)

    with st.chat_message("assistant", avatar="🤓"):
        with st.spinner("Searching knowledge base..."):
            collected_response = [""]

            def stream_and_collect():
                for chunk in pipeline_stream(prompt):
                    collected_response[0] += chunk
                    time.sleep(0.01)
                    yield chunk

            st.write_stream(stream_and_collect())

        st.session_state.messages.append({
            "role": "assistant",
            "content": collected_response[0]
        })


if os.path.exists("temp_upload.pdf"):
    try:
        os.remove("temp_upload.pdf")
    except:
        pass