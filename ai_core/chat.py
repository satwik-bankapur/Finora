from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def load_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3
    )

def load_rag():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(
        "data/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

class FinoraChat:
    def __init__(self):
        print("🤖 Loading Finora Chat...")
        self.llm = load_llm()
        self.rag = load_rag()
        self.conversation_history = []
        print("✅ Finora Chat ready!\n")

    def chat(self, user_message: str, user_profile: dict = None) -> str:
        # Step 1: Get relevant context from RAG
        rag_results = self.rag.similarity_search(user_message, k=2)
        rag_context = "\n".join([r.page_content for r in rag_results])

        # Step 2: Build conversation history string
        history_text = ""
        for turn in self.conversation_history[-4:]:  # last 4 turns
            history_text += f"User: {turn['user']}\nFinora: {turn['assistant']}\n\n"

        # Step 3: Build user context if provided
        user_context = ""
        if user_profile:
            user_context = f"""
USER PROFILE:
- Name: {user_profile.get('name', 'User')}
- Income: ₹{user_profile.get('annual_income', 0):,}
- Age: {user_profile.get('age', 'Unknown')}
- Risk Profile: {user_profile.get('risk_profile', 'medium')}
"""

        # Step 4: Build prompt
        prompt = f"""You are Finora, a friendly and knowledgeable Indian 
financial advisor chatbot. You help users with tax planning, investments, 
savings, and financial goals in the Indian context.

{user_context}

RELEVANT KNOWLEDGE FROM TAX DOCUMENTS:
{rag_context}

CONVERSATION HISTORY:
{history_text}

User: {user_message}
Finora:"""

        # Step 5: Get response
        response = self.llm.invoke(prompt).content

        # Step 6: Save to history
        self.conversation_history.append({
            "user": user_message,
            "assistant": response
        })

        return response

    def reset(self):
        self.conversation_history = []
        print("🔄 Conversation reset!")


def run_chat():
    """Interactive chat session"""
    print("\n" + "="*60)
    print("  FINORA - AI Financial Chat Assistant")
    print("="*60)
    print("Type 'quit' to exit | Type 'reset' to start over\n")

    # Optional user profile for personalization
    user_profile = {
        "name": "Rahul",
        "annual_income": 800000,
        "age": 30,
        "risk_profile": "medium"
    }

    finora = FinoraChat()

    print("💬 Ask me anything about Indian taxes, investments, or savings!\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("👋 Goodbye! Stay financially fit!")
            break
        if user_input.lower() == "reset":
            finora.reset()
            continue

        response = finora.chat(user_input, user_profile)
        print(f"\nFinora: {response}\n")
        print("-" * 40)


if __name__ == "__main__":
    run_chat()