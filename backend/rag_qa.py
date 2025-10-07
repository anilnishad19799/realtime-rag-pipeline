import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

load_dotenv()

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    BASE_DIR = os.getcwd()

VECTOR_STORE_PATH = "/app/chroma_db"
VECTOR_STORE_COLLECTION = "global_rag_collection"

# ---------------------------------------------------------
# Embeddings
# ---------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# ---------------------------------------------------------
# Load Chroma vector store (default collection)
# ---------------------------------------------------------
vector_store = Chroma(
    persist_directory=VECTOR_STORE_PATH,
    collection_name=VECTOR_STORE_COLLECTION,
    embedding_function=embeddings,
)

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# ---------------------------------------------------------
# LLM and prompt
# ---------------------------------------------------------
system_prompt = (
    "You are an assistant that answers questions **only** using the provided context. "
    "Do not make up answers. If the answer is not in the context, reply exactly: 'I don't know.' "
    "Use a maximum of three sentences.\n"
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("human", "{input}")]
)

llm = ChatOpenAI(
    temperature=0, openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo"
)

qa_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, qa_chain)


# ---------------------------------------------------------
# Ask question function
# ---------------------------------------------------------
def ask_question(query: str) -> str:
    result = chain.invoke({"input": query})
    return result.get("answer", "No answer found.")
