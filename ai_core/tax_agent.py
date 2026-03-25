from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()

# --- Load RAG ---
def load_rag():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(
        "data/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_store

# --- Load LLM ---
def load_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.1
    )

# --- Tool 1: Calculate tax under new regime ---
def calculate_tax(income: float) -> dict:
    """Calculates income tax under new regime FY 2025-26"""
    tax = 0
    slabs = [
        (300000, 0),
        (400000, 0.05),
        (300000, 0.10),
        (200000, 0.15),
        (300000, 0.20),
        (float('inf'), 0.30)
    ]
    
    remaining = income
    breakdown = []
    slab_start = 0
    
    for slab_size, rate in slabs:
        if remaining <= 0:
            break
        taxable = min(remaining, slab_size)
        tax_in_slab = taxable * rate
        tax += tax_in_slab
        if rate > 0:
            breakdown.append(
                f"₹{taxable:,.0f} @ {int(rate*100)}% = ₹{tax_in_slab:,.0f}"
            )
        remaining -= taxable
        slab_start += slab_size

    return {"total_tax": tax, "breakdown": breakdown}

# --- Tool 2: Calculate deductions ---
def calculate_deductions(investments: dict) -> dict:
    """Calculates total deductions from investments"""
    deductions = {}
    
    # 80C - max 1.5 lakh
    sec80c_instruments = ["ELSS", "PPF", "NPS", "FD", "life_insurance", "tuition_fees"]
    sec80c_total = 0
    for inst in sec80c_instruments:
        if inst in investments:
            sec80c_total += investments[inst]
    deductions["80C"] = min(sec80c_total, 150000)
    
    # 80D - health insurance max 25000
    if "health_insurance" in investments:
        deductions["80D"] = min(investments["health_insurance"], 25000)
    
    total = sum(deductions.values())
    return {"deductions": deductions, "total_deductions": total}

# --- Main Tax Agent ---
def tax_agent(user_data: dict):
    """
    user_data example:
    {
        "name": "Rahul",
        "annual_income": 800000,
        "investments": {
            "ELSS": 50000,
            "PPF": 30000,
            "health_insurance": 15000
        }
    }
    """
    print(f"\n{'='*50}")
    print(f"Tax Analysis for {user_data['name']}")
    print(f"{'='*50}")
    
    income = user_data["annual_income"]
    investments = user_data.get("investments", {})
    
    # Step 1: Calculate deductions
    deduction_result = calculate_deductions(investments)
    total_deductions = deduction_result["total_deductions"]
    
    # Step 2: Calculate tax on gross income
    gross_tax = calculate_tax(income)
    
    # Step 3: Calculate tax after deductions (old regime)
    taxable_income = max(0, income - total_deductions)
    net_tax = calculate_tax(taxable_income)
    
    tax_saved = gross_tax["total_tax"] - net_tax["total_tax"]
    
    # Step 4: Query RAG for additional tips
    rag = load_rag()
    rag_results = rag.similarity_search(
        f"tax saving deductions for income {income}", k=2
    )
    rag_context = "\n".join([r.page_content for r in rag_results])
    
    # Step 5: Generate advice with LLM
    llm = load_llm()
    prompt = f"""You are an Indian tax advisor. Given this user's financial data, 
provide a clear, friendly tax saving summary.

User: {user_data['name']}
Annual Income: ₹{income:,}
Investments: {investments}
Total Deductions: ₹{total_deductions:,}
Tax without deductions: ₹{gross_tax['total_tax']:,.0f}
Tax after deductions: ₹{net_tax['total_tax']:,.0f}
Tax Saved: ₹{tax_saved:,.0f}

Context from tax documents:
{rag_context}

Give a 3-4 line friendly summary and suggest 2-3 ways they can save more tax."""

    response = llm.invoke(prompt)
    
    # Print results
    print(f"\n📊 Income: ₹{income:,}")
    print(f"📉 Total Deductions: ₹{total_deductions:,}")
    print(f"  {deduction_result['deductions']}")
    print(f"\n💰 Tax without deductions: ₹{gross_tax['total_tax']:,.0f}")
    print(f"✅ Tax after deductions: ₹{net_tax['total_tax']:,.0f}")
    print(f"🎉 Tax Saved: ₹{tax_saved:,.0f}")
    print(f"\n🤖 AI Advisor says:")
    print(response.content)

# --- Test it ---
if __name__ == "__main__":
    user = {
        "name": "Rahul Sharma",
        "annual_income": 800000,
        "investments": {
            "ELSS": 50000,
            "PPF": 30000,
            "health_insurance": 15000
        }
    }
    tax_agent(user)