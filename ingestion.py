import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

EMBED_MODEL = "all-MiniLM-L6-v2"

def load_pdf(file):
    pages = []
    with pdfplumber.open(file) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({"page": i + 1, "text": text})
    return pages

def build_index(pages):
    if not pages:
        raise ValueError("No readable text found in the PDF. The file may be a scanned image. Please use a text-based PDF.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = []
    for p in pages:
        chunks = splitter.create_documents(
            [p["text"]], metadatas=[{"page": p["page"]}]
        )
        docs.extend(chunks)

    if not docs:
        raise ValueError("Could not split the PDF into chunks. The document may have too little text.")

    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    index = FAISS.from_documents(docs, embeddings)
    return index