# ai/rag.py
import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.config import Config

DB_DIR = "vector_db"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=Config.OPENAI_API_KEY
)

def load_text_file(path: str) -> list[str]:
    """Read a text file and return each non-empty line as a document."""
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def build_vector_db_from_txt(file_path: str):
    """Build vector DB from a .txt file."""
    docs = load_text_file(file_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = splitter.split_text("\n".join(docs))
    vectordb = Chroma.from_texts(texts, embeddings, persist_directory=DB_DIR)
    return vectordb

def load_retriever():
    """Load retriever from persisted DB."""
    vectordb = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    return vectordb.as_retriever(search_kwargs={"k": 3})
