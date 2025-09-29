import os
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

