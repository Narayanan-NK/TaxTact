import json
from planner import estimate_tax_old_regime, estimate_sip_growth
from gemini_agent import get_financial_plan
from rich import print

# Load user profile
with open("user_profile.json") as f:
    user = json.load(f)

# Sample deductions
deductions = 150000 + 25000  # 80C + 80D

# Calculate tax (Old Regime)
tax_old = estimate_tax_old_regime(user["income"], deductions)
print(f"[bold green]Estimated tax (Old Regime):[/bold green] ₹{tax_old:,.0f}")

# Sample SIP projection
sip_amount = 10000
sip_future = estimate_sip_growth(sip_amount, rate=12, years=3)
print(f"[bold blue]SIP Projection for ₹10,000/month at 12% for 3 years:[/bold blue] ₹{sip_future:,.0f}")

# Gemini Advice
print("\n[bold yellow]Getting personalized AI plan from Gemini...[/bold yellow]\n")
ai_plan = get_financial_plan(user)
print(ai_plan)
