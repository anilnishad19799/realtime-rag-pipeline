import os
import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "global_rag_collection"

client = chromadb.PersistentClient(path=CHROMA_PATH)
openai_emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

def index_chunks(chunks, source_name, job_id):
    collection = client.get_or_create_collection(
        COLLECTION_NAME, embedding_function=openai_emb
    )
    ids = [f"{job_id}_{i}" for i in range(len(chunks))]
    metas = [{"source": source_name, "job_id": job_id, "chunk_id": i} for i in range(len(chunks))]
    collection.add(documents=chunks, ids=ids, metadatas=metas)
    return len(chunks)
