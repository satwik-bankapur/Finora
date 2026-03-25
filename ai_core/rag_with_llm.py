from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

# --- Load vector store ---
def load_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(
        "data/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_store

# --- Load LLM ---
def load_llm():
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )
    return llm

# --- Ask a question ---
def ask(query):
    # Step 1: find relevant chunks
    vector_store = load_vector_store()
    relevant_chunks = vector_store.similarity_search(query, k=3)
    
    # Step 2: combine chunks into one context string
    context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])
    
    # Step 3: build prompt
    prompt = f"""You are a helpful Indian tax and finance assistant.
Use the following context from Indian tax documents to answer the question.
If you don't know, say "I don't have enough information."

Context:
{context}

Question: {query}

Answer:"""
    
    # Step 4: send to LLM
    llm = load_llm()
    response = llm.invoke(prompt)
    
    print("\n--- Answer ---")
    print(response.content)
    
    print("\n--- Sources used ---")
    for i, chunk in enumerate(relevant_chunks):
        print(f"\nSource {i+1}:")
        print(chunk.page_content[:200])

# --- Test ---
if __name__ == "__main__":
    ask("What is the deduction limit under section 80C?")