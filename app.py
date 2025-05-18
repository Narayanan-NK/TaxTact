import streamlit as st
import json, os, uuid
from datetime import datetime
import plotly.express as px
import pandas as pd

from gemini_agent import get_financial_plan
from planner import (
    estimate_tax_old_regime,
    estimate_tax_new_regime,
    estimate_sip_growth,
    generate_sip_chart,
    generate_net_worth_projection
)

# Page Setup
st.set_page_config(page_title="TaxTact – AI Financial Planner", layout="wide", page_icon="🧠")
st.markdown("""
    <div style='text-align: center; margin-top: -1rem; margin-bottom: -1rem;'>
        <h1 style='font-size: 2.5em;'>🧠 <span style='color:#f63366;'>TaxTact</span></h1>
        <p style='color: gray; font-size: 1.1em;'>Smart 3-Year Financial Planning – For Every Indian</p>
    </div>
""", unsafe_allow_html=True)

# Setup session state defaults
if "mode" not in st.session_state:
    st.session_state["mode"] = "Beginner"
if "mode_selector_shown" not in st.session_state:
    st.session_state["mode_selector_shown"] = False

tab1, tab2, tab3, tab4 = st.tabs(["🧾 Your Info", "📄 Generate Plan", "📊 Insights", "📊 Dashboard"])

# -------------------------
# Tab 1: Inputs
# -------------------------
with tab1:
    st.markdown("## 🧾 Your Information")
    st.markdown("📌 This AI-generated plan is tailored to help you reach your financial goals over the next **3 years**.")

    if "mode" not in st.session_state:
        st.session_state["mode"] = "Beginner"

    mode = st.radio(
        "Choose your mode", ["Beginner", "Expert"],
        horizontal=True,
        key="mode_selector",
        index=["Beginner", "Expert"].index(st.session_state["mode"])
    )

    # Sync back to session_state
    st.session_state["mode"] = mode

    mode = st.session_state["mode"]

    with st.expander("👤 Personal Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email (optional)")
            age = st.number_input("Current Age", 18, 70, 30)
            marital_status = st.selectbox("Marital Status", ["single", "married"])
            city_tier = st.selectbox("Your City Tier", ["Metro", "Tier 1", "Tier 2", "Rural"])
        with col2:
            dependents = st.multiselect("Dependents", ["parents", "children"])
            income = st.number_input("Annual Income (₹)", 100000, 5000000, 1200000)
            loans = st.number_input("Total Loans/EMIs (₹)", 0, 5000000, 200000, step=10000)
            growth_percent = st.slider("Expected CTC Growth (%)", 0, 50, 10)
            growth_rate = growth_percent / 100
            savings_percent = st.slider("How much can you save annually (%)", 0, 100, 30)

    with st.expander("🎯 Financial Goals & Preferences", expanded=True):
        col3, col4 = st.columns(2)
        with col3:
            goals = st.multiselect("Financial Goals", [
                "Buy a house", "Save ₹10L corpus", "Child planning", "Retirement fund"
            ])
            target_corpus = st.number_input("Target Corpus (₹)", 100000, 10000000, 1000000, step=100000)
            has_insurance = st.radio("Do you already have term insurance?", ["Yes", "No"], horizontal=True, key="radio_insurance")
            owns_home = st.radio("Do you own a house?", ["Yes", "No"], horizontal=True, key="radio_home")
        with col4:
            existing_investments = st.number_input("Existing Investments (₹)", 0, 10000000, 200000, step=10000)
            sip_amount = st.number_input("Monthly SIP (₹)", 1000, 100000, 10000, step=1000)
            sip_rate = st.slider("Expected SIP Return (%)", 5, 20, 12)
            sip_years = st.number_input("Investing Duration (Years)", 1, 30, 3)
            preferences = st.multiselect("Investment Preferences", ["ELSS", "PPF", "SIP", "FD", "NPS", "Insurance"])

# -------------------------
# Tab 2: Generate Plan
# -------------------------
with tab2:
    st.markdown("## 📄 Generate Your Personalized Financial Plan")

    if st.session_state.get("tab") == "plan" or st.button("📊 Generate My Plan"):
        plan_id = str(uuid.uuid4())[:8]
        user = {
            "id": plan_id,
            "name": name,
            "email": email,
            "age": age,
            "marital_status": marital_status,
            "dependents": dependents,
            "income": income,
            "growth_rate": growth_rate,
            "loans": loans,
            "goals": goals,
            "risk": "moderate",
            "preferences": preferences,
            "sip_amount": sip_amount,
            "sip_rate": sip_rate,
            "sip_years": sip_years,
            "savings_percent": savings_percent,
            "target_corpus": target_corpus,
            "city_tier": city_tier,
            "has_insurance": has_insurance,
            "owns_home": owns_home,
            "existing_investments": existing_investments,
            "user_mode": mode

        }

        tax_old = estimate_tax_old_regime(income, 150000 + 25000)
        tax_new = estimate_tax_new_regime(income)
        better_regime = "New Regime" if tax_new < tax_old else "Old Regime"
        sip_projection = estimate_sip_growth(sip_amount, sip_rate, sip_years)
        ai_plan = get_financial_plan(user)

        summary = f"""
        **Plan ID**: `{plan_id}`  
        **Tax (Old Regime)**: ₹{tax_old:,.0f}  
        **Tax (New Regime)**: ₹{tax_new:,.0f}  
        **Recommended Regime**: {better_regime}  
        **Projected SIP Corpus**: ₹{sip_projection:,.0f}  
        """

        st.session_state["summary"] = summary
        st.session_state["ai_plan"] = ai_plan
        st.session_state["plan_id"] = plan_id
        st.session_state["sip_df"] = generate_sip_chart(sip_amount, sip_rate, sip_years)
        st.session_state["fd_df"] = generate_sip_chart(sip_amount, 6.5, sip_years)
        st.session_state["net_df"] = generate_net_worth_projection(income, savings_percent / 100, loans, sip_years, growth_rate)

        st.success("✅ Your 3-Year AI Plan has been generated!")

        st.markdown("### 📋 Summary Overview")
        st.markdown(summary)

        if ai_plan:
            st.markdown("### 📄 Your 3-Year Financial Plan")

            if mode == "Expert":
                st.markdown("🧠 **Expert Mode**: Full projections, tax tables, and investment strategy.")
            else:
                st.markdown("✨ **Beginner Mode**: Simple steps and friendly breakdown.")

            st.markdown(ai_plan, unsafe_allow_html=True)


        st.session_state["tab"] = "insights"



# ----------------------------
# TAB 3: Insights
# ----------------------------
with tab3:
    st.markdown("## 📊 Investment Insights & Download")

    if "summary" in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📈 SIP Projection")
            st.plotly_chart(
                px.line(st.session_state["sip_df"], x="Month", y="Value", title="Your SIP Growth"),
                use_container_width=True
            )

        with col2:
            st.markdown("#### 🏦 FD Benchmark (6.5%)")
            st.plotly_chart(
                px.line(st.session_state["fd_df"], x="Month", y="Value", title="FD Growth (6.5%)"),
                use_container_width=True
            )

        st.markdown("#### 💼 Net Worth Growth")
        st.plotly_chart(
            px.line(st.session_state["net_df"], x="Year", y="Net Worth", title="Projected Net Worth Over Time"),
            use_container_width=True
        )

        st.markdown("### 📥 Download Your Plan Summary")
        st.download_button(
            label="📥 Download .txt Plan",
            data=st.session_state["summary"] + "\n\n" + st.session_state["ai_plan"],
            file_name=f"TaxTact_{st.session_state['plan_id']}.txt",
            mime="text/plain"
        )
    else:
        st.warning("Please generate a plan first in the previous tab.")
        
from milestones_generator import generate_monthly_plan
import io

if "plan_id" in st.session_state:
    df = generate_monthly_plan(
        sip_amount=sip_amount,
        rate=sip_rate,
        years=sip_years
    )

    # .xlsx export
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Milestones")

    st.download_button(
        label="📥 Download .xlsx Roadmap",
        data=buffer,
        file_name=f"TaxTact_{st.session_state['plan_id']}_milestones.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # .md export
    md = df.to_markdown(index=False)
    st.download_button(
        label="📄 Export as .md (Markdown)",
        data=md,
        file_name=f"TaxTact_{st.session_state['plan_id']}.md",
        mime="text/markdown"
    )


# ----------------------------
# TAB 4: Dashboard
# ----------------------------
with tab4:
    st.markdown("## 📊 Dashboard Overview")

    if "summary" in st.session_state:
        st.markdown(f"**Plan ID**: `{st.session_state['plan_id']}`")

        col1, col2, col3 = st.columns(3)
        col1.metric("Tax (Old Regime)", f"₹{estimate_tax_old_regime(income, 150000 + 25000):,.0f}")
        col2.metric("Tax (New Regime)", f"₹{estimate_tax_new_regime(income):,.0f}")
        col3.metric("SIP Corpus", f"₹{estimate_sip_growth(sip_amount, sip_rate, sip_years):,.0f}")

        st.markdown("#### 🎯 Financial Goals")
        st.markdown(", ".join(goals) if goals else "_No goals selected_")

        st.markdown("#### 💬 Summary")
        st.markdown(st.session_state["summary"])

        if st.session_state["mode"] == "Expert":
            st.markdown("#### 🧠 AI Plan (Full)")
            st.markdown(st.session_state["ai_plan"])
    else:
        st.warning("Please generate a plan first.")







#cd "D:\AI Agent\FinancePlanner\financial_planner_ai"
#dir
#streamlit run app.py