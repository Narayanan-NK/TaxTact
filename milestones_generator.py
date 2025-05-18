import pandas as pd

def generate_monthly_plan(sip_amount, rate, years):
    total_months = years * 12
    rows = []
    value = 0

    for m in range(1, total_months + 1):
        value = (value + sip_amount) * (1 + rate / 1200)
        milestone = ""

        if m == 3:
            milestone = "Emergency fund setup"
        elif m == 6:
            milestone = "Health/term insurance review"
        elif m == 12:
            milestone = "Year 1 corpus checkpoint"
        elif m == 24:
            milestone = "Mid-plan check-in"
        elif m == 36:
            milestone = "Goal maturity"

        rows.append({
            "Month": f"Month {m}",
            "SIP Invested (₹)": sip_amount * m,
            "Estimated Value (₹)": round(value),
            "Milestone": milestone
        })

    return pd.DataFrame(rows)
