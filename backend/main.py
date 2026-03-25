from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# So we can import from ai_core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core.tax_agent import tax_agent, calculate_tax, calculate_deductions
from ai_core.investment_agent import investment_agent, allocate_portfolio, estimate_returns

app = FastAPI(title="Finora API", version="1.0.0")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- Data Models ---
class TaxRequest(BaseModel):
    name: str
    annual_income: float
    investments: dict = {}

class InvestmentRequest(BaseModel):
    name: str
    monthly_savings: float
    risk_profile: str
    age: int
    goal: str = "wealth creation"

# --- Routes ---
@app.get("/")
def root():
    return {"message": "Welcome to Finora API 🚀"}

@app.get("/health")
def health():
    return {"status": "running"}

@app.post("/tax")
def get_tax_advice(request: TaxRequest):
    user_data = {
        "name": request.name,
        "annual_income": request.annual_income,
        "investments": request.investments
    }
    
    # Run calculations
    deduction_result = calculate_deductions(request.investments)
    total_deductions = deduction_result["total_deductions"]
    
    gross_tax = calculate_tax(request.annual_income)
    taxable_income = max(0, request.annual_income - total_deductions)
    net_tax = calculate_tax(taxable_income)
    tax_saved = gross_tax["total_tax"] - net_tax["total_tax"]
    
    return {
        "name": request.name,
        "annual_income": request.annual_income,
        "deductions": deduction_result["deductions"],
        "total_deductions": total_deductions,
        "tax_before_deductions": gross_tax["total_tax"],
        "tax_after_deductions": net_tax["total_tax"],
        "tax_saved": tax_saved
    }

@app.post("/invest")
def get_investment_advice(request: InvestmentRequest):
    years = 60 - request.age
    portfolio = allocate_portfolio(request.monthly_savings, request.risk_profile)
    returns = estimate_returns(portfolio, years)
    
    return {
        "name": request.name,
        "monthly_savings": request.monthly_savings,
        "risk_profile": request.risk_profile,
        "years": years,
        "portfolio": portfolio,
        "estimated_returns": returns
    }