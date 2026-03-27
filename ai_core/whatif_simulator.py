from tax_agent import calculate_tax, calculate_deductions
from investment_agent import estimate_returns, allocate_portfolio
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

def load_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.2
    )

# --- Scenario 1: What if I invest more monthly? ---
def whatif_more_sip(current_monthly: float, new_monthly: float, 
                     years: int, risk_profile: str) -> dict:
    current_portfolio = allocate_portfolio(current_monthly, risk_profile)
    new_portfolio = allocate_portfolio(new_monthly, risk_profile)

    current_returns = estimate_returns(current_portfolio, years)
    new_returns = estimate_returns(new_portfolio, years)

    difference = new_returns["total_future_value"] - current_returns["total_future_value"]
    extra_monthly = new_monthly - current_monthly

    return {
        "scenario": "Increased Monthly SIP",
        "current_monthly": current_monthly,
        "new_monthly": new_monthly,
        "extra_per_month": extra_monthly,
        "current_corpus": current_returns["total_future_value"],
        "new_corpus": new_returns["total_future_value"],
        "additional_wealth": difference,
        "years": years
    }

# --- Scenario 2: What if I maximize 80C? ---
def whatif_maximize_80c(annual_income: float, 
                         current_investments: dict) -> dict:
    current_deductions = calculate_deductions(current_investments)
    current_tax = calculate_tax(
        annual_income - current_deductions["total_deductions"]
    )

    # Maximize 80C to 1.5 lakh
    maxed_investments = current_investments.copy()
    current_80c = sum(
        current_investments.get(k, 0) 
        for k in ["ELSS", "PPF", "NPS", "FD"]
    )
    if current_80c < 150000:
        maxed_investments["ELSS"] = maxed_investments.get("ELSS", 0) + (150000 - current_80c)

    maxed_deductions = calculate_deductions(maxed_investments)
    maxed_tax = calculate_tax(
        annual_income - maxed_deductions["total_deductions"]
    )

    tax_saved = current_tax["total_tax"] - maxed_tax["total_tax"]
    extra_investment = maxed_deductions["total_deductions"] - current_deductions["total_deductions"]

    return {
        "scenario": "Maximize Section 80C",
        "current_tax": current_tax["total_tax"],
        "new_tax": maxed_tax["total_tax"],
        "additional_investment_needed": extra_investment,
        "tax_saved": tax_saved,
        "current_deductions": current_deductions["total_deductions"],
        "new_deductions": maxed_deductions["total_deductions"]
    }

# --- Scenario 3: What if I retire earlier? ---
def whatif_early_retirement(current_age: int, early_age: int,
                             monthly_savings: float, 
                             risk_profile: str) -> dict:
    normal_years = 60 - current_age
    early_years = early_age - current_age

    normal_portfolio = allocate_portfolio(monthly_savings, risk_profile)
    early_portfolio = allocate_portfolio(monthly_savings, risk_profile)

    normal_returns = estimate_returns(normal_portfolio, normal_years)
    early_returns = estimate_returns(early_portfolio, early_years)

    corpus_difference = normal_returns["total_future_value"] - early_returns["total_future_value"]

    return {
        "scenario": f"Retire at {early_age} instead of 60",
        "normal_retirement_age": 60,
        "early_retirement_age": early_age,
        "corpus_at_60": normal_returns["total_future_value"],
        "corpus_at_early": early_returns["total_future_value"],
        "corpus_difference": corpus_difference,
        "years_saved": normal_years - early_years
    }

# --- Scenario 4: What if I reduce expenses? ---
def whatif_reduce_expenses(current_monthly_savings: float,
                            expense_reduction: float,
                            years: int,
                            risk_profile: str) -> dict:
    new_monthly_savings = current_monthly_savings + expense_reduction

    current_portfolio = allocate_portfolio(current_monthly_savings, risk_profile)
    new_portfolio = allocate_portfolio(new_monthly_savings, risk_profile)

    current_returns = estimate_returns(current_portfolio, years)
    new_returns = estimate_returns(new_portfolio, years)

    return {
        "scenario": f"Reduce expenses by ₹{expense_reduction:,}/month",
        "current_savings": current_monthly_savings,
        "new_savings": new_monthly_savings,
        "current_corpus": current_returns["total_future_value"],
        "new_corpus": new_returns["total_future_value"],
        "additional_wealth": new_returns["total_future_value"] - current_returns["total_future_value"]
    }

# --- AI Summary ---
def generate_whatif_summary(scenarios: list) -> str:
    llm = load_llm()
    
    scenario_text = "\n".join([
        f"- {s['scenario']}: Extra wealth = ₹{s.get('additional_wealth', s.get('tax_saved', s.get('corpus_difference', 0))):,.0f}"
        for s in scenarios
    ])

    prompt = f"""You are Finora, an Indian financial advisor.
    
A user ran these What-If scenarios:
{scenario_text}

In 3-4 lines, tell them which scenario gives the most impact 
and what they should prioritize first. Be specific and encouraging.
Use Indian financial context."""

    return llm.invoke(prompt).content

# --- Main Runner ---
def run_whatif_simulator(user_profile: dict):
    print(f"\n{'='*60}")
    print(f"  FINORA - What-If Simulator")
    print(f"{'='*60}")

    years = 60 - user_profile["age"]
    scenarios = []

    # Scenario 1: Double the SIP
    s1 = whatif_more_sip(
        current_monthly=user_profile["monthly_savings"],
        new_monthly=user_profile["monthly_savings"] * 1.5,
        years=years,
        risk_profile=user_profile["risk_profile"]
    )
    scenarios.append(s1)
    print(f"\n📈 SCENARIO 1: {s1['scenario']}")
    print(f"  Current SIP: ₹{s1['current_monthly']:,}/month")
    print(f"  New SIP: ₹{s1['new_monthly']:,}/month")
    print(f"  Current Corpus: ₹{s1['current_corpus']:,.0f}")
    print(f"  New Corpus: ₹{s1['new_corpus']:,.0f}")
    print(f"  💰 Additional Wealth: ₹{s1['additional_wealth']:,.0f}")

    # Scenario 2: Maximize 80C
    s2 = whatif_maximize_80c(
        annual_income=user_profile["annual_income"],
        current_investments=user_profile["investments"]
    )
    scenarios.append(s2)
    print(f"\n📉 SCENARIO 2: {s2['scenario']}")
    print(f"  Current Tax: ₹{s2['current_tax']:,.0f}")
    print(f"  New Tax: ₹{s2['new_tax']:,.0f}")
    print(f"  Extra Investment Needed: ₹{s2['additional_investment_needed']:,}")
    print(f"  💰 Tax Saved: ₹{s2['tax_saved']:,.0f}")

    # Scenario 3: Early retirement
    s3 = whatif_early_retirement(
        current_age=user_profile["age"],
        early_age=50,
        monthly_savings=user_profile["monthly_savings"],
        risk_profile=user_profile["risk_profile"]
    )
    scenarios.append(s3)
    print(f"\n🏖️ SCENARIO 3: {s3['scenario']}")
    print(f"  Corpus at 60: ₹{s3['corpus_at_60']:,.0f}")
    print(f"  Corpus at 50: ₹{s3['corpus_at_early']:,.0f}")
    print(f"  💸 Corpus Lost by Retiring Early: ₹{s3['corpus_difference']:,.0f}")

    # Scenario 4: Reduce expenses
    s4 = whatif_reduce_expenses(
        current_monthly_savings=user_profile["monthly_savings"],
        expense_reduction=5000,
        years=years,
        risk_profile=user_profile["risk_profile"]
    )
    scenarios.append(s4)
    print(f"\n✂️ SCENARIO 4: {s4['scenario']}")
    print(f"  Current Savings: ₹{s4['current_savings']:,}/month")
    print(f"  New Savings: ₹{s4['new_savings']:,}/month")
    print(f"  💰 Additional Wealth: ₹{s4['additional_wealth']:,.0f}")

    # AI Summary
    print(f"\n🤖 FINORA RECOMMENDS:")
    summary = generate_whatif_summary(scenarios)
    print(summary)

    return scenarios

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
    run_whatif_simulator(user)