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
        temperature=0.3
    )

# --- Tool 1: Portfolio Allocator ---
def allocate_portfolio(monthly_savings: float, risk_profile: str) -> dict:
    """Suggests portfolio allocation based on risk profile"""
    
    allocations = {
        "low": {
            "PPF": 0.30,
            "FD": 0.30,
            "Debt Mutual Funds": 0.25,
            "ELSS": 0.10,
            "Emergency Fund": 0.05
        },
        "medium": {
            "ELSS": 0.30,
            "PPF": 0.20,
            "Debt Mutual Funds": 0.20,
            "Index Funds": 0.20,
            "FD": 0.10
        },
        "high": {
            "ELSS": 0.35,
            "Index Funds": 0.30,
            "Direct Stocks": 0.20,
            "Debt Mutual Funds": 0.10,
            "Emergency Fund": 0.05
        }
    }
    
    profile = allocations.get(risk_profile, allocations["medium"])
    
    portfolio = {}
    for instrument, percentage in profile.items():
        amount = monthly_savings * percentage
        portfolio[instrument] = {
            "percentage": f"{int(percentage * 100)}%",
            "monthly_amount": round(amount, 2)
        }
    
    return portfolio

# --- Tool 2: Calculate returns ---
def estimate_returns(portfolio: dict, years: int = 10) -> dict:
    """Estimates future value of portfolio"""
    
    return_rates = {
        "PPF": 0.071,
        "FD": 0.065,
        "Debt Mutual Funds": 0.075,
        "ELSS": 0.12,
        "Index Funds": 0.11,
        "Direct Stocks": 0.13,
        "Emergency Fund": 0.04
    }
    
    estimates = {}
    total_future_value = 0
    
    for instrument, details in portfolio.items():
        monthly = details["monthly_amount"]
        rate = return_rates.get(instrument, 0.07)
        monthly_rate = rate / 12
        months = years * 12
        
        # Future value of SIP formula
        if monthly_rate > 0:
            fv = monthly * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        else:
            fv = monthly * months
            
        estimates[instrument] = round(fv, 2)
        total_future_value += fv
    
    return {
        "instrument_wise": estimates,
        "total_future_value": round(total_future_value, 2)
    }

# --- Main Investment Agent ---
def investment_agent(user_data: dict):
    """
    user_data example:
    {
        "name": "Priya",
        "monthly_savings": 15000,
        "risk_profile": "medium",
        "age": 28,
        "goal": "retirement"
    }
    """
    print(f"\n{'='*50}")
    print(f"Investment Plan for {user_data['name']}")
    print(f"{'='*50}")
    
    monthly_savings = user_data["monthly_savings"]
    risk_profile = user_data["risk_profile"]
    age = user_data.get("age", 30)
    goal = user_data.get("goal", "wealth creation")
    years = 60 - age  # invest till retirement
    
    # Step 1: Allocate portfolio
    portfolio = allocate_portfolio(monthly_savings, risk_profile)
    
    # Step 2: Estimate returns
    returns = estimate_returns(portfolio, years)
    
    # Step 3: Query RAG for investment tips
    rag = load_rag()
    rag_results = rag.similarity_search(
        f"investment options mutual funds tax saving for {risk_profile} risk", k=2
    )
    rag_context = "\n".join([r.page_content for r in rag_results])
    
    # Step 4: Generate advice with LLM
    llm = load_llm()
    prompt = f"""You are a friendly Indian investment advisor.
    
User Profile:
- Name: {user_data['name']}
- Age: {age}
- Monthly Savings: ₹{monthly_savings:,}
- Risk Profile: {risk_profile}
- Goal: {goal}
- Years to invest: {years}

Portfolio Allocation:
{portfolio}

Estimated corpus after {years} years: ₹{returns['total_future_value']:,.0f}

Context from financial documents:
{rag_context}

Give a friendly 3-4 line summary of their investment plan and 
2 specific actionable tips for their age and risk profile.
Keep it simple and encouraging."""

    response = llm.invoke(prompt)
    
    # Print results
    print(f"\n👤 Age: {age} | Risk: {risk_profile.upper()} | Goal: {goal}")
    print(f"💵 Monthly Savings: ₹{monthly_savings:,}")
    print(f"\n📊 Recommended Portfolio:")
    for instrument, details in portfolio.items():
        print(f"  {instrument}: {details['percentage']} → ₹{details['monthly_amount']:,}/month")
    
    print(f"\n📈 Estimated Returns after {years} years:")
    for instrument, fv in returns['instrument_wise'].items():
        print(f"  {instrument}: ₹{fv:,.0f}")
    print(f"\n🏆 Total Corpus: ₹{returns['total_future_value']:,.0f}")
    
    print(f"\n🤖 AI Advisor says:")
    print(response.content)

# --- Test it ---
if __name__ == "__main__":
    user = {
        "name": "Priya Patel",
        "monthly_savings": 15000,
        "risk_profile": "medium",
        "age": 28,
        "goal": "retirement"
    }
    investment_agent(user)