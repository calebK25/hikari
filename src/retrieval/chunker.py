from langchain_text_splitters import RecursiveCharacterTextSplitter

def split(raw_pages):
    md = "\n".join([p["text"] for p in raw_pages])
    splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=50)
    return splitter.create_documents([md])

