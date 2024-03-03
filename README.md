# RAG Based Search Tool
This project is a prototype search tool that utilizes a Retrieval-Augmented Generation (RAG) model to provide answers to user queries based on information extracted from PDF documents. The tool combines the functionalities of a document understanding AI with an intuitive front-end interface.

## Overview
The RAG model is trained on a set of provided PDF documents or any PDFs placed in a designated folder. The web application frontend interacts with the RAG model to display a list of documents fetched via an API and show their content when selected. Users can ask questions through a chat interface, with the RAG model providing answers based on the documents' content. Answers are highlighted in the PDF viewer when possible, or reference links to the section of the document containing the answer are provided.

## Setup Instructions

**Clone the Repository:**

```
git clone https://github.com/yourusername/rag-based-search-tool.git
```

**Install Dependencies:**

```
cd rag-based-search-tool
pip install -r requirements.txt
```

**Set Up OpenAI API Key:**

Obtain an API key from OpenAI and set it in the app.py file.

**Run the Application:**

```
streamlit run app.py
```

**Interacting with the Application**

### **Upload PDF Documents:**

Use the file uploader in the web application to upload PDF documents. These documents will be processed and used for document understanding and question answering.

**Ask Questions:**

Enter your questions in the chat interface provided by the web application. The RAG model will provide answers based on the content of the uploaded PDF documents.

**View Answers:**

The answers provided by the RAG model will be displayed in the chat interface. If applicable, answers will be highlighted in the PDF viewer, or reference links to the relevant section of the document will be provided.

**Design Choices and Technologies Used**

Streamlit: Used for building the web application frontend due to its ease of use and interactive features.
OpenAI API: Utilized for the RAG model to perform document understanding and question answering tasks.
PyMuPDF: Used for extracting text from PDF documents.
Python: Programming language used for development.
