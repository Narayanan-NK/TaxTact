def estimate_tax_old_regime(income, deductions):
    taxable = income - deductions
    if taxable <= 250000:
        return 0
    elif taxable <= 500000:
        return (taxable - 250000) * 0.05
    elif taxable <= 1000000:
        return 12500 + (taxable - 500000) * 0.2
    else:
        return 112500 + (taxable - 1000000) * 0.3

def estimate_tax_new_regime(income):
    tax = 0
    slabs = [
        (300000, 0.00),
        (300000, 0.05),
        (300000, 0.10),
        (300000, 0.15),
        (300000, 0.20),
        (float('inf'), 0.30)
    ]

    remaining = income
    for slab_amt, rate in slabs:
        if remaining <= 0:
            break
        taxable = min(remaining, slab_amt)
        tax += taxable * rate
        remaining -= taxable

    return round(tax, 2)

def estimate_sip_growth(monthly_sip, rate, years):
    n = years * 12
    r = rate / 12 / 100
    future_value = monthly_sip * (((1 + r)**n - 1) * (1 + r)) / r
    return round(future_value, 2)
import pandas as pd

def generate_sip_chart(monthly_sip, rate, years):
    r = rate / 12 / 100
    data = []
    total = 0

    for i in range(1, years * 12 + 1):
        total = (total + monthly_sip) * (1 + r)
        data.append((i, round(total, 2)))

    df = pd.DataFrame(data, columns=["Month", "Value"])
    return df

def generate_net_worth_projection(income, savings_rate, loans, years, growth_rate):
    data = []
    net_worth = -loans
    for year in range(1, years + 1):
        income += income * growth_rate
        savings = income * savings_rate
        net_worth += savings
        data.append((year, round(net_worth, 2)))
    df = pd.DataFrame(data, columns=["Year", "Net Worth"])
    return df
