from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(text_path: str, chunk_size=500, chunk_overlap=50):
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)
