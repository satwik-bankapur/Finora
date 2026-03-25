from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --- Step 1: Load PDF ---
def load_pdf(path):
    loader = PyPDFLoader(path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages")
    return documents

# --- Step 2: Split into chunks ---
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,       # 500 tokens per chunk
        chunk_overlap=50      # overlap so context isn't lost at edges
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks

# --- Step 3: Create embeddings & store in FAISS ---
def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"  # lightweight, fast, good quality
    )
    vector_store = FAISS.from_documents(chunks, embeddings)
    vector_store.save_local("data/faiss_index")
    print("Vector store saved!")
    return vector_store

# --- Step 4: Query the vector store ---
def query_vector_store(query):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(
        "data/faiss_index", 
        embeddings,
        allow_dangerous_deserialization=True
    )
    results = vector_store.similarity_search(query, k=3)  # top 3 chunks
    return results

# --- Test it ---
if __name__ == "__main__":
    # Change this to your PDF path
    docs = load_pdf("data/tax_doc.txt")
    chunks = split_documents(docs)
    create_vector_store(chunks)

    # Test a query
    query = "What is the deduction limit under section 80C?"
    results = query_vector_store(query)
    
    for i, res in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(res.page_content)