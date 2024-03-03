# Import necessary libraries
import openai
import streamlit as st
from openai import OpenAI

import os

os.environ["OPENAI_API_KEY"] = st.secrets["general"]["OPENAI_API_KEY"]
# Set the API key for OpenAI
#api_key = st.secrets["general"]["OPENAI_API_KEY"]
# Set the API key for OpenAI
#openai.api_key = api_key
# Now you can use the OpenAI client
client = openai.Client()
from brain import get_index_for_pdf
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
import time



# Set up the Streamlit app
st.title("RAG based search tool")
st.subheader("Ask questions based on the provided PDF files")

# Read the app secrets named 'API_TOKEN'

# Cached function to create a vectordb for the provided PDF files
@st.cache_resource
def create_vectordb(files, filenames):
    with st.spinner("Thinking..."):
        vectordb = get_index_for_pdf([file.getvalue() for file in files], filenames, os.environ["OPENAI_API_KEY"])
    return vectordb

# Upload PDF files using Streamlit's file uploader
pdf_files = st.file_uploader("Upload your pdf", type="pdf", accept_multiple_files=True)

# If PDF files are uploaded, create the vectordb and store it in the session state
if pdf_files:
    pdf_file_names = [file.name for file in pdf_files]
    st.session_state["vectordb"] = create_vectordb(pdf_files, pdf_file_names)

# Define the template for the chatbot prompt
prompt_template = """
    You are a helpful Assistant who answers to users questions based on multiple contexts given to you.
    Keep your answer short and to the point.
    The evidence are the context of the pdf extract with metadata. 
    Carefully focus on the metadata specially 'filename' and 'page' whenever answering.
    Make sure to add filename and page number at the end of sentence you are citing to.
    Reply "Not applicable" if text is irrelevant.
    The PDF content is:
    {pdf_extract}
"""

# Get the current prompt from the session state or set a default value
prompt = st.session_state.get("prompt", [{"role": "system", "content": "none"}])

# Display previous chat messages
if "prompt" not in st.session_state:
    st.session_state.prompt = [{"role": "system", "content": "none"}]

# Get the current prompt from the session state
prompt = st.session_state.prompt

# Display previous chat messages
for message in prompt:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Get the user's question using Streamlit's chat input
question = st.chat_input("Ask anything")

# Handle the user's question
if question:
    vectordb = st.session_state.get("vectordb", None)
    if not vectordb:
        st.warning("You need to provide a PDF")
        st.stop()

    # Search the vectordb for similar content to the user's question
    search_results = vectordb.similarity_search(question, k=3)
    #search_results
    pdf_extract = "/n ".join([result.page_content for result in search_results])

     # Update the prompt with the pdf extract
    prompt[0] = {
        "role": "system",
        "content": prompt_template.format(pdf_extract=pdf_extract),
    }

    # Add the user's question to the prompt and display it
    prompt.append({"role": "user", "content": question})
    #print(question)
    with st.chat_message("user", avatar="👤"):
        st.write(question)

    # Display an empty assistant message while waiting for the response
    with st.chat_message("assistant", avatar= "🤖"):
        botmsg = st.empty()

    # Call ChatGPT with streaming and display the response as it comes
    response = []
    result = ""
    for chunk in client.chat.completions.create(model="gpt-3.5-turbo", messages=prompt, stream=True):
        choice_text = chunk.choices[0].delta.content if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content') else None
        if choice_text is not None:
            response.append(choice_text)
            result = "".join(response).strip()
            #values = ','.join(str(v) for v in response)
            botmsg.write(result)
    time.sleep(2)

    # Add the assistant's response to the prompt
    prompt.append({"role": "assistant", "content": result})

    # Store the updated prompt in the session state
    st.session_state["prompt"] = prompt
    #prompt.append({"role": "assistant", "content": result})

    # Store the updated prompt in the session state
    #st.session_state["prompt"] = prompt