# ingest.py
import os
from dotenv import load_dotenv 
from langchain_community.document_loaders import TextLoader  
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

DOCS_PATH = "rag_docs"
DB_PATH = "faiss_store"




def load_documents():
    docs = []
    folder = "rag_docs"
    for file in os.listdir(folder):
        if file.endswith(".md"):
            loader = TextLoader(os.path.join(folder, file), encoding="utf-8")
            docs.extend(loader.load())
    print(f"Loaded {len(docs)} documents.")
    return docs


def split_documents(docs):
    """
    Splits documents into smaller overlapping chunks for better retrieval.
    """
    print("✂️ Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=80,
    )
    chunks = splitter.split_documents(docs)
    print(f"✅ Created {len(chunks)} chunks.")
    return chunks


def build_vector_store(chunks):
    """
    Creates FAISS vector store from document chunks and saves it locally.
    """
    print("🧠 Creating embeddings model...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("📦 Building FAISS vector store...")
    vector_db = FAISS.from_documents(chunks, embeddings)

    print(f"💾 Saving vector store to: {DB_PATH}")
    vector_db.save_local(DB_PATH)
    print("✅ Ingestion complete. FAISS store ready.")


def main():
    docs = load_documents()
    chunks = split_documents(docs)
    build_vector_store(chunks)


if __name__ == "__main__":
    main()
