"""
Snowflake EVM (Enterprise Value Management) Analysis Engine

This module provides the deterministic financial calculations and
Snowflake-specific cloud economic levers used to generate an account
economics snapshot (TCO, ROI, NPV, Payback Period) for a prospective
customer migration.
"""

def normalize_cost(infra_cost, licensing_cost, labor_cost):
    """
    Normalizes the diverse cost components into a unified baseline TCO.
    """
    return infra_cost + licensing_cost + labor_cost

# --- Snowflake Specific Cloud Economic Factors ---

def _load_extracted_benchmarks():
    try:
        import os, json
        benchmarks_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "extracted_benchmarks.json")
        with open(benchmarks_path, "r") as f:
            return json.load(f)
    except Exception:
        return {"implied_compute_efficiency_gain": 0.30, "implied_storage_compression_improvement": 0.30}

_SEC_BENCHMARKS = _load_extracted_benchmarks()

def estimate_compute_efficiency_gain(current_compute_cost, migration_factor=1.0):
    """
    Estimates the compute elasticity savings (on-demand vs reserved capacity).
    Uses dynamically extracted benchmarks from Snowflake's 10-K filings.
    """
    efficiency_multiplier = _SEC_BENCHMARKS.get("implied_compute_efficiency_gain", 0.30)
    return current_compute_cost * (migration_factor * efficiency_multiplier)

def estimate_storage_savings(current_storage_cost, migration_factor=1.0):
    """
    Estimates storage reduction through Snowflake's columnar micro-partitioning
    and advanced compression.
    """
    # Average 30% compression improvement
    compression_improvement = 0.30 
    return current_storage_cost * (migration_factor * compression_improvement)

def estimate_productivity_lift(data_team_headcount, fully_loaded_salary, migration_factor=1.0):
    """
    Estimates developer/analyst productivity lift due to concurrency improvements,
    reduced operational overhead (no indexes to tune, vacuuming, etc.), and 
    faster time-to-insight.
    """
    # Assuming 15% of a data engineer/analyst's time is freed up from maintenance
    time_savings_pct = 0.15
    total_labor_cost = data_team_headcount * fully_loaded_salary
    return total_labor_cost * (migration_factor * time_savings_pct)

# --- Core Financial Metrics (ROI, NPV, Payback) ---

def calculate_roi(total_benefits, total_costs):
    """
    ROI = (Benefits - Costs) / Costs
    """
    if total_costs == 0:
        return 0.0
    return ((total_benefits - total_costs) / total_costs) * 100

def calculate_npv(cash_flows, discount_rate=0.08):
    """
    NPV = sum of discounted net cash flows over the analysis period.
    cash_flows: List of net cash flows for each year (Year 0, Year 1, Year 2...)
    discount_rate: The rate used to discount future cash flows (default 8%)
    """
    npv = 0.0
    for year, cash_flow in enumerate(cash_flows):
        npv += cash_flow / ((1 + discount_rate) ** year)
    return npv

def calculate_payback_period(initial_investment, continuous_cash_flows):
    """
    Simple continuous payback period = time until cumulative benefits exceed initial cost.
    Assumes straight-line cash flow accrual throughout the year.
    Returns the number of years (as a float).
    """
    if continuous_cash_flows <= 0:
        return float('inf') # Will never pay back
    
    return initial_investment / continuous_cash_flows

# --- The Main Value Assessment Engine ---

def run_evm_assessment(
    current_infra_cost,
    current_compute_cost,
    current_storage_cost,
    current_licensing_cost,
    data_team_headcount,
    avg_salary,
    migration_factor=0.40, # E.g., migrating 40% of workloads to Snowflake
    discount_rate=0.08,
    analysis_years=3,
    implementation_cost=150000 
):
    """
    Runs the full deterministic "As-Is" vs "To-Be" Value Engineering assessment.
    Organizes the output into Snowflake's 3 Value Buckets.
    """
    # 1. Baseline (As-Is) TCO 
    current_labor_cost = data_team_headcount * avg_salary
    baseline_annual_tco = normalize_cost(current_infra_cost, current_licensing_cost, current_labor_cost)
    
    baseline_3yr_tco = baseline_annual_tco * analysis_years

    # 2. To-Be Savings (Value Levers)
    compute_savings = estimate_compute_efficiency_gain(current_compute_cost, migration_factor)
    storage_savings = estimate_storage_savings(current_storage_cost, migration_factor)
    productivity_savings = estimate_productivity_lift(data_team_headcount, avg_salary, migration_factor)
    
    total_annual_savings = compute_savings + storage_savings + productivity_savings

    # "To-Be" Annual TCO
    proposed_annual_tco = baseline_annual_tco - total_annual_savings
    proposed_3yr_tco = proposed_annual_tco * analysis_years + implementation_cost

    # 3. Formulate Cash Flows for NPV
    # Year 0: Negative cash flow (Implementation cost)
    # Year 1-3: Positive net savings
    cash_flows = [-implementation_cost] + [total_annual_savings] * analysis_years
    
    npv = calculate_npv(cash_flows, discount_rate)
    roi = calculate_roi(total_annual_savings * analysis_years, proposed_3yr_tco)
    payback_period = calculate_payback_period(implementation_cost, total_annual_savings)

    # 4. Map to Snowflake Value Buckets with Value Engineering Terminology
    value_buckets = {
        "Cost Reduction (Cost Value)": {
            "Infrastructure Efficiency (Compute + Storage)": compute_savings + storage_savings,
            "Description": "Direct reduction in physical/cloud infrastructure footprint via Snowflake elasticity, actively improving the 'Cost Value' of the data platform."
        },
        "Revenue Enablement (Use Value)": {
            "Productivity Lift": productivity_savings,
            "Description": "Faster time-to-insight and reduced administrative overhead freeing up data engineers, drastically improving the functional 'Use Value' of the team."
        },
        "Risk Reduction (Esteem & Exchange Value)": {
            "Reduced Technical Debt": "Qualitative - Migrating to a fully managed SaaS reduces patching and version upgrades.",
            "Description": "Migration to a single governed copy of data limits compliance surface area, boosting 'Esteem Value' via trust, and 'Exchange Value' via easier data sharing."
        }
    }
    
    # Calculate Function-to-Cost Ratio
    # Function = Total Benefits (Total Annual Savings over 3 years)
    # Cost = Total Lifecycle Cost (Proposed 3Yr TCO)
    function_to_cost_ratio = (total_annual_savings * analysis_years) / proposed_3yr_tco if proposed_3yr_tco > 0 else 0
    
    # 5. Infrastructure Sizing (Actual Consumption Pricing)
    # Assuming standard AWS US East (N. Virginia) Capacity
    PRICE_PER_CREDIT_ENTERPRISE = 3.00
    PRICE_PER_TB_STORAGE_MONTHLY = 23.00
    
    proposed_compute_annual_cost = (current_compute_cost * migration_factor) - compute_savings
    proposed_storage_annual_cost = (current_storage_cost * migration_factor) - storage_savings
    
    infrastructure_sizing = {
        "Edition": "AWS Enterprise",
        "Price_Per_Credit": PRICE_PER_CREDIT_ENTERPRISE,
        "Price_Per_Storage_TB_Month": PRICE_PER_TB_STORAGE_MONTHLY,
        "Estimated_Annual_Credits": proposed_compute_annual_cost / PRICE_PER_CREDIT_ENTERPRISE if PRICE_PER_CREDIT_ENTERPRISE > 0 else 0,
        "Estimated_Storage_TB": (proposed_storage_annual_cost / 12) / PRICE_PER_TB_STORAGE_MONTHLY if PRICE_PER_TB_STORAGE_MONTHLY > 0 else 0
    }

    return {
        "Baseline_Annual_TCO": baseline_annual_tco,
        "Baseline_3Yr_TCO": baseline_3yr_tco,
        "Proposed_Annual_TCO": proposed_annual_tco,
        "Proposed_3Yr_TCO": proposed_3yr_tco,
        "Infrastructure_Sizing": infrastructure_sizing,
        "Total_Annual_Savings": total_annual_savings,
        "NPV": npv,
        "ROI_Percentage": roi,
        "Payback_Period_Years": payback_period,
        "Function_to_Cost_Ratio": function_to_cost_ratio,
        "Value_Buckets": value_buckets
    }

if __name__ == "__main__":
    # Sample Test Run
    result = run_evm_assessment(
        current_infra_cost=2000000,
        current_compute_cost=1500000,
        current_storage_cost=500000,
        current_licensing_cost=300000,
        data_team_headcount=12,
        avg_salary=140000,
        migration_factor=0.50 # Moving 50% to Snowflake
    )
    import json
    print(json.dumps(result, indent=2))
