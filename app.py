import streamlit as st
from rag.ingestion import load_pdf, build_index
from rag.retrieval import retrieve_and_answer

st.set_page_config(page_title="RAG PDF Chatbot")
st.title("RAG PDF Chatbot")
st.caption("Upload a PDF and ask questions. Answers are grounded in the document with page citations.")

with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Google AI Studio API Key", type="password")
    st.markdown("Get your key at [aistudio.google.com](https://aistudio.google.com)")

    st.divider()

    st.header("Upload PDF")
    uploaded = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded and api_key:
        try:
            with st.spinner("Reading and indexing document..."):
                pages = load_pdf(uploaded)
                st.session_state["index"] = build_index(pages)
                st.session_state["messages"] = []
                st.session_state["api_key"] = api_key
            st.success("Indexed " + str(len(pages)) + " pages.")
        except ValueError as e:
            st.error(str(e))
    elif uploaded and not api_key:
        st.warning("Please enter your API key first.")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask a question about your PDF...")

if query:
    if "index" not in st.session_state:
        st.warning("Please upload a PDF and enter your API key first.")
    else:
        st.session_state["messages"].append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = retrieve_and_answer(
                        query,
                        st.session_state["index"],
                        st.session_state["api_key"]
                    )
                    st.markdown(result["answer"])
                    with st.expander("Source chunks"):
                        for s in result["sources"]:
                            st.markdown("**Page " + str(s["page"]) + ":** " + s["snippet"] + "...")
                    st.session_state["messages"].append({
                        "role": "assistant",
                        "content": result["answer"]
                    })
                except ValueError as e:
                    st.error(str(e))