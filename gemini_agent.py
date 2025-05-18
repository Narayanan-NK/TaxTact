import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_financial_plan(user):
    mode = user.get("user_mode", "Beginner")

    if mode == "Expert":
        detail_level = """
## 📋 Expert Output Instructions

- Provide a detailed 3-year financial roadmap.
- Include tax regime comparison table (Old vs New).
- Add SIP projection table (monthly, yearly, final corpus).
- Recommend term insurance coverage based on income.
- Add estimated Net Worth table year-wise.
- Use markdown sections and bullet points to format.
"""
    else:
        detail_level = """
## ✨ Beginner Output Instructions

- Keep output simple and friendly.
- No large tables or technical jargon.
- Summarize key actions:
  - Monthly SIP
  - Which tax regime to choose
  - Whether to get insurance
- Provide clear section titles and 2–3 bullet points each.
- End with a motivational call to action.
"""

    prompt = f"""
You are a 25+ year experienced Indian financial planner and tax strategist.

## 👤 User Profile:
- Age: {user['age']}
- Marital Status: {user['marital_status']}
- Dependents: {', '.join(user['dependents'])}
- Income: ₹{user['income']:,}
- Risk Appetite: {user['risk']}
- Growth Rate: {user['growth_rate']*100:.1f}%
- Loans: ₹{user['loans']:,}
- Savings Potential: {user['savings_percent']}%
- SIP: ₹{user['sip_amount']}/month @ {user['sip_rate']}% for {user['sip_years']} yrs
- Existing Investments: ₹{user['existing_investments']:,}
- Goals: {', '.join(user['goals'])}
- City Tier: {user['city_tier']}
- Has Term Insurance: {user['has_insurance']}
- Owns Home: {user['owns_home']}
- Preferences: {', '.join(user['preferences'])}
- Target Corpus: ₹{user['target_corpus']:,}

{detail_level}

Generate a clean 3-year financial plan.
"""

    model = None
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
    except Exception:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

    return response.text
