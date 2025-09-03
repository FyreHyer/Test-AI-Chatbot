from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama.embeddings  import OllamaEmbeddings
import os

persist_directory = "chroma_db"

# Initialize embeddings (using free HuggingFace embeddings)
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# Only rebuild vector store if it doesn't already exist
if os.path.exists(persist_directory) and os.listdir(persist_directory):
    print("Loading existing vector store...")
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    print("Vector store loaded successfully!")
else:
    print("Creating new vector store...")
    loader = PyPDFLoader(r"C:\Users\ISDAdmin\Documents\aichatbot\Test-AI-Chatbot\troubleshooting.pdf")
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from PDF")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=300,
        separators=[
            "\n## ", "\n### ", "\nProblem:", "\nSolution:", "\nSymptoms:", "\nCause:", "\nStep ", "\n\n", "\n", ". ", " ", ""
        ],
        length_function=len,
    )
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} text chunks")

    vectorstore = Chroma.from_documents(
        documents=texts,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    print(f"Created vector store with {len(texts)} documents")
    print(f"Vector store saved to: {persist_directory}")


retriever = vectorstore.as_retriever(k=3)
