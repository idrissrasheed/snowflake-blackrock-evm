import streamlit as st
import pandas as pd
import json
import os

from evm_engine import run_evm_assessment
from agent import run_workshop_summarizer

st.set_page_config(layout="wide", page_title="Snowflake EVM Sales Agent")

# --- BlackRock Custom Value Engineering Presentation ---

st.title("❄️ Snowflake Value Engineering: BlackRock Aladdin")
st.markdown("A tailored value assessment for expanding Snowflake workloads within BlackRock's Aladdin Data Cloud.")
st.divider()

tab1, tab2, tab3 = st.tabs(["The Business Case", "The Financial Model", "AI Discovery Brief"])

with tab1:
    # Customer Background
    st.header("1. Customer Background: BlackRock Aladdin")
    st.markdown("""
    * **Global investment & risk platform** handling massive institutional volumes.
    * **Heavy market data pipelines** ingesting petabytes of ticks, trades, and reference data.
    * **Huge compute needs** to run highly complex financial risk models at market close.
    """)
    st.divider()
    
    # Pain Points
    st.header("2. Pain Points")
    st.markdown("""
    * **Rigid batch processing** delaying critical market risk assessments.
    * **High infra cost for peak-load risk modeling** leading to massive over-provisioning.
    * **Hard to scale data environments** acting as a bottleneck for new quants and ML teams.
    * **Difficult cross-client data sharing** causing friction when onboarding asset managers.
    """)
    st.divider()
    
    # Snowflake Value Hypothesis
    st.header("3. Snowflake Value Hypothesis")
    st.markdown("""
    * **Elastic compute for risk modeling** allowing BlackRock to spin up instantly and scale down to zero when models finish.
    * **Lower-cost storage with micro-partitioning** vastly reducing the footprint of historical tick data.
    * **Data sharing for asset managers** enabling instant, secure access without copying files.
    * **Reduced time-to-insight** empowering portfolio managers to react to market changes faster.
    """)

with tab2:
    # Financial Model
    st.header("4. Financial Model (Aladdin Expansion)")
    st.markdown("Adjust the levers below to dynamically calculate the expected financial return of moving to Snowflake.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Your Assumptions")
        migration_pct = st.slider("Percentage of Risk Models moving to Snowflake (%)", min_value=10, max_value=100, value=50, step=10) / 100.0
        contract_length = st.slider("How many years are we planning for?", min_value=1, max_value=25, value=3)
        
        st.markdown("#### Your Current Yearly Spend")
        current_infra_cost = st.number_input("Current Server & Hardware Costs ($)", value=25000000, step=1000000)
        current_compute_cost = st.number_input("Cost of Running Risk Models ($)", value=45000000, step=1000000)
        current_storage_cost = st.number_input("Cost of Storing Market Data ($)", value=15000000, step=1000000)
        current_licensing_cost = st.number_input("Software Licenses (Oracle, etc.) ($)", value=12000000, step=1000000)
        
        st.markdown("#### Your Team & Setup Costs")
        data_team_headcount = st.number_input("Number of Data Engineers", value=300, step=25)
        implementation_cost = st.number_input("One-time Setup / Migration Cost ($)", value=5000000, step=500000)

    with col2:
        # Run the deterministic math engine
        evm_results = run_evm_assessment(
            current_infra_cost=current_infra_cost,
            current_compute_cost=current_compute_cost,
            current_storage_cost=current_storage_cost,
            current_licensing_cost=current_licensing_cost,
            data_team_headcount=data_team_headcount,
            # NYC Financial Scale Salary
            avg_salary=180000, 
            migration_factor=migration_pct,
            discount_rate=0.08,
            analysis_years=contract_length,
            implementation_cost=implementation_cost
        )
        
        st.subheader("Your Financial Outcomes")
        
        mcol1, mcol2 = st.columns(2)
        mcol1.metric("Cost If You Do Nothing", f"${evm_results['Baseline_3Yr_TCO']:,.0f}")
        mcol2.metric("Cost With Snowflake", f"${evm_results['Proposed_3Yr_TCO']:,.0f}", delta=f"-${evm_results['Baseline_3Yr_TCO'] - evm_results['Proposed_3Yr_TCO']:,.0f} Total Savings", delta_color="inverse")
        
        mcol3, mcol4, mcol5, mcol6 = st.columns(4)
        mcol3.metric("Return on Investment", f"{evm_results['ROI_Percentage']:.1f}%")
        mcol4.metric("Payback Period (Months)", f"{evm_results['Payback_Period_Years'] * 12:.1f}")
        mcol5.metric("Total Net Savings", f"${evm_results['NPV']:,.0f}")
        mcol6.metric("Function-to-Cost Ratio", f"{evm_results['Function_to_Cost_Ratio']:.2f}x")
        
        st.markdown("#### What You Actually Buy (Snowflake AWS Enterprise)")
        sizing = evm_results["Infrastructure_Sizing"]
        scol1, scol2 = st.columns(2)
        scol1.metric("Compute Power Needed", f"{sizing['Estimated_Annual_Credits']:,.0f} Credits/Yr", help=f"At ${sizing['Price_Per_Credit']:.2f} per credit")
        scol2.metric("Storage Space Needed", f"{sizing['Estimated_Storage_TB']:,.0f} TB/Month", help=f"At ${sizing['Price_Per_Storage_TB_Month']:.2f} per TB")
        
        st.markdown("#### Where Do The Savings Come From?")
        for bucket_name, bucket_data in evm_results["Value_Buckets"].items():
            numeric_val = next(iter(bucket_data.values()))
            if isinstance(numeric_val, (int, float)):
                st.markdown(f"**{bucket_name}**: :green[+${numeric_val:,.0f}/year]")
            else:
                st.markdown(f"**{bucket_name}**: (Qualitative Impact)")

with tab3:
    st.header("5. AI Discovery Brief (Scraped Context)")
    st.markdown("This briefing document is generated by the AI Agent scanning actual BlackRock/Aladdin case studies and Summit24 presentations.")
    st.divider()
    
    # Run the AI
    ai_results = run_workshop_summarizer()
    
    st.subheader("💡 Hypothesized Pain Points (NLP Extracted)")
    for point in ai_results.get("Extracted_Pain_Points", []):
        st.markdown(f"- {point}")
        
    st.subheader("🎯 Value Engineering Next Steps")
    st.markdown("Before presenting the financial model, ask the BlackRock leadership team:")
    for question in ai_results.get("VE_Next_Discovery_Questions", []):
        st.markdown(f"- *{question}*")
        
    with st.expander("Show AI Value Driver Mapping"):
        for category, mappings in ai_results.get("Hypothesized_Value_Drivers", {}).items():
            st.markdown(f"**{category}**")
            for m in mappings:
                st.markdown(f"- {m}")
