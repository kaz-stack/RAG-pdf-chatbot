from google import genai
from langchain_community.vectorstores import FAISS

def retrieve_and_answer(query, index, api_key, k=4):
    client = genai.Client(api_key=api_key)

    results = index.similarity_search_with_score(query, k=k)

    context_parts = []
    sources = []
    for doc, score in results:
        page = doc.metadata.get("page", "unknown")
        context_parts.append("Page " + str(page) + ":\n" + doc.page_content)
        sources.append({"page": page, "snippet": doc.page_content[:150]})

    context = "\n\n---\n\n".join(context_parts)

    prompt = (
        "You are a helpful assistant. Answer the question using ONLY the context provided below.\n"
        "If the answer is not in the context, say: I could not find that in the document.\n"
        "Always mention which page your answer comes from.\n\n"
        "Context:\n" + context + "\n\n"
        "Question: " + query + "\n"
        "Answer:"
    )

    try:
        response = client.models.generate_content(
            model="models/gemini-2.0-flash",
            contents=prompt
        )
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "quota" in error_msg.lower():
            raise ValueError("API quota exceeded. Please wait a minute and try again.")
        raise ValueError("Gemini API error: " + error_msg)

    return {
        "answer": response.text,
        "sources": sources
    }