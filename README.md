# RAG PDF Chatbot

A Retrieval-Augmented Generation (RAG) app that lets you chat with any PDF document.
Upload a PDF, ask questions in plain English, and get answers grounded in the document with page-level citations.

## How it works

1. You upload a PDF
2. The app splits the text into chunks and converts them into vector embeddings
3. Your question is also converted into an embedding
4. The most relevant chunks are retrieved using similarity search (FAISS)
5. Those chunks are sent to Gemini along with your question
6. Gemini returns a grounded answer with page citations

## Project Structure

## Tech Stack

| Component     | Tool                              |
|---------------|-----------------------------------|
| PDF parsing   | pdfplumber                        |
| Chunking      | LangChain RecursiveTextSplitter   |
| Embeddings    | sentence-transformers (local)     |
| Vector store  | FAISS                             |
| LLM           | Gemini 1.5 Flash (Google AI)      |
| UI            | Streamlit                         |

## Setup and Run

1. Clone the repo

git clone https://github.com/yourusername/rag-pdf-chatbot
cd rag-pdf-chatbot

2. Install dependencies

pip install -r requirements.txt

3. Run the app

streamlit run app.py

4. In the sidebar, paste your Google AI Studio API key and upload a PDF

## Notes

- Works only with text-based PDFs (not scanned image PDFs)
- The embedding model runs locally, no extra API key needed
- API key is entered at runtime in the sidebar, never stored