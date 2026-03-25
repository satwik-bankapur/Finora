from faker import Faker
import random
import json

fake = Faker('en_IN')  # Indian locale

# --- Generate Users ---
def generate_users(n=10):
    users = []
    for i in range(n):
        user = {
            "id": i + 1,
            "name": fake.name(),
            "email": fake.email(),
            "city": fake.city(),
            "annual_income": random.randint(300000, 1500000),  # 3L to 15L
            "risk_profile": random.choice(["low", "medium", "high"])
        }
        users.append(user)
    return users

# --- Generate Transactions ---
def generate_transactions(users):
    categories = ["salary", "rent", "food", "entertainment", "medical", "investment"]
    transactions = []
    tid = 1
    for user in users:
        for _ in range(20):  # 20 transactions per user
            txn = {
                "id": tid,
                "user_id": user["id"],
                "date": str(fake.date_this_year()),
                "amount": random.randint(500, 50000),
                "category": random.choice(categories),
                "description": fake.bs()
            }
            transactions.append(txn)
            tid += 1
    return transactions

# --- Generate Investments ---
def generate_investments(users):
    types = ["ELSS", "PPF", "FD", "NPS", "Health Insurance"]
    investments = []
    iid = 1
    for user in users:
        for _ in range(3):  # 3 investments per user
            inv = {
                "id": iid,
                "user_id": user["id"],
                "type": random.choice(types),
                "amount": random.randint(5000, 150000),
                "returns_rate": round(random.uniform(5.0, 15.0), 2)
            }
            investments.append(inv)
            iid += 1
    return investments

# --- Run & Save ---
users = generate_users(10)
transactions = generate_transactions(users)
investments = generate_investments(users)

with open("data/users.json", "w") as f:
    json.dump(users, f, indent=2)

with open("data/transactions.json", "w") as f:
    json.dump(transactions, f, indent=2)

with open("data/investments.json", "w") as f:
    json.dump(investments, f, indent=2)

print(f"Generated {len(users)} users, {len(transactions)} transactions, {len(investments)} investments")