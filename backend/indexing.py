import os
<<<<<<< HEAD
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from uuid import uuid4
=======
import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
>>>>>>> 6ceebea9ac7cd2a11e5830be9bd21b267c8055d8

load_dotenv()

# ------------------------------
# Paths & config
# ------------------------------
VECTOR_STORE_PATH = "/app/chroma_db"  # absolute path inside container
VECTOR_STORE_COLLECTION = "global_rag_collection"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

<<<<<<< HEAD
=======
client = chromadb.PersistentClient(path=CHROMA_PATH)
openai_emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
>>>>>>> 6ceebea9ac7cd2a11e5830be9bd21b267c8055d8

def index_chunks(chunks, source_name, job_id):
    """
    Index chunks safely into Chroma inside Celery task.
    """

    # 1️⃣ Initialize Chroma inside the task
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        collection_name=VECTOR_STORE_COLLECTION,
        embedding_function=embeddings,
    )

    # 2️⃣ Prepare Document objects
    documents = [
        Document(page_content=chunk, metadata={"source": source_name, "chunk_id": i})
        for i, chunk in enumerate(chunks)
    ]
    ids = [str(uuid4()) for _ in documents]

    # 3️⃣ Add to vector store
    vector_store.add_documents(documents=documents, ids=ids)

    # 4️⃣ Persist explicitly
    # vector_store.persist()

    print(
        f"✅ Indexed {len(chunks)} chunks into '{VECTOR_STORE_COLLECTION}' at '{VECTOR_STORE_PATH}'"
    )
    return len(chunks)
