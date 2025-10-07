import os
<<<<<<< HEAD
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
=======
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# ----- Setup -----
VECTOR_STORE_PATH = "./chroma_db"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vector_store = Chroma(
    persist_directory=VECTOR_STORE_PATH,
    embedding_function=embeddings
)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# ----- Prompt -----
system_prompt = (
    "Use the given context to answer the question. "
    "If you don't know the answer, say you don't know. "
    "Use three sentences maximum and keep the answer concise.\n"
    "Context: {context}"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}")
])

# ----- LLM -----
llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

# ----- Chains -----
question_answer_chain = create_stuff_documents_chain(llm, prompt)
chain = create_retrieval_chain(retriever, question_answer_chain)

# ----- Ask Question Function -----
def ask_question(query: str) -> str:
    """
    Return answer from RAG pipeline (synchronous, non-streaming).
    """
    result = chain.invoke({"input": query})
    print("*"*100)
    print("result", result)
    return result.get("answer", "No answer found.")

>>>>>>> 6ceebea9ac7cd2a11e5830be9bd21b267c8055d8
