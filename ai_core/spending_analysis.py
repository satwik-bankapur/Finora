import json
from collections import defaultdict
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

# --- Load transactions for a user ---
def load_user_transactions(user_id: int) -> list:
    with open("data/transactions.json") as f:
        all_txns = json.load(f)
    return [t for t in all_txns if t["user_id"] == user_id]

# --- Load user profile ---
def load_user(user_id: int) -> dict:
    with open("data/users.json") as f:
        users = json.load(f)
    return next((u for u in users if u["id"] == user_id), None)

# --- Spending Analysis ---
def analyse_spending(transactions: list) -> dict:
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)

    for txn in transactions:
        category = txn["category"]
        amount = txn["amount"]
        category_totals[category] += amount
        category_counts[category] += 1

    total_spent = sum(category_totals.values())

    breakdown = {}
    for cat, total in category_totals.items():
        breakdown[cat] = {
            "total": round(total, 2),
            "count": category_counts[cat],
            "percentage": round((total / total_spent) * 100, 1)
        }

    # Sort by total spent
    breakdown = dict(
        sorted(breakdown.items(), 
               key=lambda x: x[1]["total"], reverse=True)
    )

    return {
        "total_spent": round(total_spent, 2),
        "breakdown": breakdown
    }

# --- Savings Analysis ---
def analyse_savings(user: dict, transactions: list) -> dict:
    monthly_income = user["annual_income"] / 12

    # Get salary credits and investment amounts
    salary_txns = [t for t in transactions if t["category"] == "salary"]
    investment_txns = [t for t in transactions if t["category"] == "investment"]
    expense_txns = [t for t in transactions 
                   if t["category"] not in ["salary", "investment"]]

    total_salary = sum(t["amount"] for t in salary_txns)
    total_investments = sum(t["amount"] for t in investment_txns)
    total_expenses = sum(t["amount"] for t in expense_txns)
    total_income = max(total_salary, monthly_income * 
                      len(set(t["date"][:7] for t in transactions)))

    savings_rate = ((total_income - total_expenses) / total_income * 100 
                   if total_income > 0 else 0)

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "total_investments": round(total_investments, 2),
        "net_savings": round(total_income - total_expenses, 2),
        "savings_rate": round(savings_rate, 1)
    }

# --- Anomaly Detection ---
def detect_anomalies(transactions: list) -> list:
    amounts = [t["amount"] for t in transactions]
    avg = sum(amounts) / len(amounts)
    std = (sum((x - avg) ** 2 for x in amounts) / len(amounts)) ** 0.5
    threshold = avg + (2 * std)  # anything 2 std deviations above avg

    anomalies = []
    for txn in transactions:
        if txn["amount"] > threshold:
            anomalies.append({
                "date": txn["date"],
                "amount": txn["amount"],
                "category": txn["category"],
                "description": txn["description"],
                "reason": f"Unusually high (avg: ₹{avg:,.0f}, this: ₹{txn['amount']:,})"
            })

    return anomalies

# --- Detect Subscriptions ---
def detect_subscriptions(transactions: list) -> list:
    # Group by description, find recurring ones
    desc_counts = defaultdict(list)
    for txn in transactions:
        desc_counts[txn["description"]].append(txn["amount"])

    subscriptions = []
    for desc, amounts in desc_counts.items():
        if len(amounts) >= 2:  # appears more than once
            subscriptions.append({
                "description": desc,
                "occurrences": len(amounts),
                "avg_amount": round(sum(amounts) / len(amounts), 2),
                "total_spent": round(sum(amounts), 2)
            })

    return subscriptions

# --- Financial Score ---
def calculate_financial_score(savings: dict, 
                               spending: dict, 
                               anomalies: list) -> dict:
    score = 100
    reasons = []

    # Savings rate scoring (max 40 points)
    savings_rate = savings["savings_rate"]
    if savings_rate >= 30:
        savings_score = 40
        reasons.append("✅ Excellent savings rate (30%+)")
    elif savings_rate >= 20:
        savings_score = 30
        reasons.append("🟡 Good savings rate (20-30%)")
    elif savings_rate >= 10:
        savings_score = 20
        reasons.append("🟠 Average savings rate (10-20%)")
    else:
        savings_score = 10
        reasons.append("🔴 Low savings rate (<10%) — try to save more")

    # Investment scoring (max 30 points)
    investment_pct = (savings["total_investments"] / 
                     savings["total_income"] * 100 
                     if savings["total_income"] > 0 else 0)
    if investment_pct >= 20:
        investment_score = 30
        reasons.append("✅ Strong investment habit (20%+ of income)")
    elif investment_pct >= 10:
        investment_score = 20
        reasons.append("🟡 Moderate investing (10-20% of income)")
    else:
        investment_score = 10
        reasons.append("🔴 Low investments — consider SIP")

    # Anomaly penalty (max -30 points)
    anomaly_penalty = min(len(anomalies) * 5, 30)
    if anomaly_penalty == 0:
        reasons.append("✅ No unusual spending detected")
    else:
        reasons.append(f"⚠️ {len(anomalies)} unusual transactions detected")

    final_score = savings_score + investment_score - anomaly_penalty
    final_score = max(0, min(100, final_score))

    grade = ("A" if final_score >= 80 else 
             "B" if final_score >= 60 else 
             "C" if final_score >= 40 else "D")

    return {
        "score": final_score,
        "grade": grade,
        "breakdown": {
            "savings_score": savings_score,
            "investment_score": investment_score,
            "anomaly_penalty": -anomaly_penalty
        },
        "reasons": reasons
    }

# --- AI Insights ---
def generate_ai_insights(user: dict, spending: dict, 
                          savings: dict, score: dict) -> str:
    llm = load_llm()
    prompt = f"""You are Finora, an AI financial advisor analyzing 
spending patterns for an Indian user.

USER: {user['name']}, Income: ₹{user['annual_income']:,}/year

SPENDING BREAKDOWN:
{json.dumps(spending['breakdown'], indent=2)}

SAVINGS:
- Total Expenses: ₹{savings['total_expenses']:,}
- Net Savings: ₹{savings['net_savings']:,}
- Savings Rate: {savings['savings_rate']}%

FINANCIAL SCORE: {score['score']}/100 (Grade: {score['grade']})

Give 3 specific, actionable insights about their spending patterns.
Be conversational, friendly and specific to Indian context.
Keep it under 150 words."""

    return llm.invoke(prompt).content

# --- Main Runner ---
def run_spending_analysis(user_id: int = 1):
    print(f"\n{'='*60}")
    print(f"  FINORA - Spending & Savings Analysis")
    print(f"{'='*60}")

    user = load_user(user_id)
    transactions = load_user_transactions(user_id)

    print(f"\n👤 Analysing: {user['name']}")
    print(f"📝 Total transactions: {len(transactions)}")

    spending = analyse_spending(transactions)
    savings = analyse_savings(user, transactions)
    anomalies = detect_anomalies(transactions)
    subscriptions = detect_subscriptions(transactions)
    score = calculate_financial_score(savings, spending, anomalies)
    insights = generate_ai_insights(user, spending, savings, score)

    # Print results
    print(f"\n💸 SPENDING BREAKDOWN:")
    for cat, data in spending["breakdown"].items():
        print(f"  {cat}: ₹{data['total']:,} ({data['percentage']}%)")

    print(f"\n💰 SAVINGS SUMMARY:")
    print(f"  Total Income: ₹{savings['total_income']:,}")
    print(f"  Total Expenses: ₹{savings['total_expenses']:,}")
    print(f"  Net Savings: ₹{savings['net_savings']:,}")
    print(f"  Savings Rate: {savings['savings_rate']}%")

    print(f"\n⚠️ ANOMALIES DETECTED: {len(anomalies)}")
    for a in anomalies[:3]:
        print(f"  ₹{a['amount']:,} on {a['date']} ({a['category']})")

    print(f"\n🔄 RECURRING TRANSACTIONS: {len(subscriptions)}")

    print(f"\n🏆 FINANCIAL SCORE: {score['score']}/100 (Grade {score['grade']})")
    for r in score["reasons"]:
        print(f"  {r}")

    print(f"\n🤖 AI INSIGHTS:")
    print(insights)

    return {
        "user": user,
        "spending": spending,
        "savings": savings,
        "anomalies": anomalies,
        "subscriptions": subscriptions,
        "score": score,
        "insights": insights
    }

if __name__ == "__main__":
    run_spending_analysis(user_id=1)