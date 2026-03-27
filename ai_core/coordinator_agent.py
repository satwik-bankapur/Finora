from tax_agent import calculate_tax, calculate_deductions
from investment_agent import allocate_portfolio, estimate_returns
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()

def load_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )

def load_rag():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return FAISS.load_local(
        "data/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

def run_coordinator(user_profile: dict) -> dict:
    """
    user_profile example:
    {
        "name": "Rahul Sharma",
        "age": 30,
        "annual_income": 800000,
        "monthly_savings": 15000,
        "risk_profile": "medium",
        "goal": "retirement",
        "investments": {
            "ELSS": 50000,
            "PPF": 30000,
            "health_insurance": 15000
        }
    }
    """
    print(f"\n{'='*60}")
    print(f"  FINORA - Complete Financial Plan for {user_profile['name']}")
    print(f"{'='*60}")

    # --- Run Tax Agent ---
    print("\n[1/3] Running Tax Agent...")
    deduction_result = calculate_deductions(user_profile["investments"])
    total_deductions = deduction_result["total_deductions"]
    gross_tax = calculate_tax(user_profile["annual_income"])
    taxable_income = max(0, user_profile["annual_income"] - total_deductions)
    net_tax = calculate_tax(taxable_income)
    tax_saved = gross_tax["total_tax"] - net_tax["total_tax"]

    tax_results = {
        "annual_income": user_profile["annual_income"],
        "total_deductions": total_deductions,
        "deduction_breakdown": deduction_result["deductions"],
        "tax_before": gross_tax["total_tax"],
        "tax_after": net_tax["total_tax"],
        "tax_saved": tax_saved
    }

    # --- Run Investment Agent ---
    print("[2/3] Running Investment Agent...")
    years = 60 - user_profile["age"]
    portfolio = allocate_portfolio(
        user_profile["monthly_savings"],
        user_profile["risk_profile"]
    )
    returns = estimate_returns(portfolio, years)

    investment_results = {
        "monthly_savings": user_profile["monthly_savings"],
        "risk_profile": user_profile["risk_profile"],
        "years": years,
        "portfolio": portfolio,
        "total_corpus": returns["total_future_value"]
    }

    # --- Query RAG ---
    print("[3/3] Generating AI advice...")
    rag = load_rag()
    rag_chunks = rag.similarity_search(
        f"tax saving investment planning for income {user_profile['annual_income']}", 
        k=2
    )
    rag_context = "\n".join([c.page_content for c in rag_chunks])

    # --- Generate holistic advice with LLM ---
    llm = load_llm()
    prompt = f"""You are Finora, an expert Indian financial advisor.
    
Create a comprehensive but concise financial summary for this user.

USER PROFILE:
- Name: {user_profile['name']}
- Age: {user_profile['age']}
- Annual Income: ₹{user_profile['annual_income']:,}
- Risk Profile: {user_profile['risk_profile']}
- Goal: {user_profile['goal']}

TAX ANALYSIS:
- Total Deductions: ₹{total_deductions:,}
- Tax Saved: ₹{tax_saved:,.0f}
- Tax Payable: ₹{net_tax['total_tax']:,.0f}

INVESTMENT PLAN:
- Monthly SIP: ₹{user_profile['monthly_savings']:,}
- Expected Corpus in {years} years: ₹{returns['total_future_value']:,.0f}

CONTEXT FROM TAX DOCUMENTS:
{rag_context}

Write a friendly, professional 4-5 line financial summary and 
3 specific actionable recommendations. Format it clearly."""

    ai_advice = llm.invoke(prompt).content

    # --- Combine everything ---
    final_plan = {
        "user": user_profile,
        "tax": tax_results,
        "investment": investment_results,
        "ai_advice": ai_advice
    }

    # --- Print summary ---
    print(f"\n📊 TAX SUMMARY")
    print(f"  Income: ₹{user_profile['annual_income']:,}")
    print(f"  Deductions: ₹{total_deductions:,}")
    print(f"  Tax Saved: ₹{tax_saved:,.0f}")
    print(f"  Tax Payable: ₹{net_tax['total_tax']:,.0f}")

    print(f"\n💼 INVESTMENT SUMMARY")
    print(f"  Monthly SIP: ₹{user_profile['monthly_savings']:,}")
    print(f"  Risk Profile: {user_profile['risk_profile'].upper()}")
    print(f"  Estimated Corpus: ₹{returns['total_future_value']:,.0f}")

    print(f"\n🤖 FINORA SAYS:")
    print(ai_advice)

    return final_plan

# --- Test ---
if __name__ == "__main__":
    user = {
        "name": "Rahul Sharma",
        "age": 30,
        "annual_income": 800000,
        "monthly_savings": 15000,
        "risk_profile": "medium",
        "goal": "retirement",
        "investments": {
            "ELSS": 50000,
            "PPF": 30000,
            "health_insurance": 15000
        }
    }
    run_coordinator(user)