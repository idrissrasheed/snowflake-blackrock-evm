import json
import re
import os

# In a real deployed app, this module would invoke the Snowflake Cortex AI or OpenAI.
# For demo purposes, we are simulating the Language Model's extraction logic deterministicly.

def extract_pain_points(transcript):
    """
    Simulates an LLM parsing the scraped case study facts to extract
    discrete customer pain points and business goals.
    """
    pain_points = []
    
    text = transcript.lower()
    
    # Catching common themes from actual Snowflake case studies
    if any(word in text for word in ["scale", "growth", "volume", "amount", "petabyte", "terabyte"]):
        pain_points.append("Inability to scale infrastructure to meet growing data volumes efficiently.")
    if any(word in text for word in ["time", "slow", "wait", "delay", "latency", "real-time"]):
        pain_points.append("Data latency and performance bottlenecks delaying critical business insights.")
    if any(word in text for word in ["silo", "fragment", "disparate", "multiple", "source", "single source"]):
        pain_points.append("Fragmented data silos preventing a unified, single source of truth.")
    if any(word in text for word in ["manage", "maintenance", "overhead", "admin", "operate"]):
        pain_points.append("High operational overhead and engineering time wasted on database maintenance.")
    if any(word in text for word in ["cost", "expensive", "save", "budget", "finance"]):
        pain_points.append("Unpredictable and escalating legacy infrastructure costs.")
    if any(word in text for word in ["compliance", "secure", "govern", "protect", "risk", "share", "collaboration"]):
        pain_points.append("Difficulty securely sharing governed data internally or externally.")
    if any(word in text for word in ["ai", "machine learning", "model", "predict", "forecast"]):
        pain_points.append("Current architecture is unable to support advanced ML/AI workloads.")
        
    # Fallback if transcript doesn't hit any of these broad keywords
    if len(pain_points) == 0:
        pain_points.append(f"General data architecture modernization: {transcript[:100]}...")
        
    return pain_points

def generate_value_driver_map(pain_points):
    """
    Maps the qualitative pain points into a formal, tabular Value Driver Map 
    used in elite Snowflake VE presentations.
    Columns: [Pain Point, Value Lever, Financial Driver, Metric Impact]
    """
    driver_map = []
    
    for pp in pain_points:
        text = pp.lower()
        
        # Performance/Batching -> Compute Elasticity
        if any(word in text for word in ["slow", "time", "delay", "batch"]):
            driver_map.append({
                "Pain Point": pp,
                "Value Lever": "Elastic Compute (Scale up/down instantly)",
                "Financial Driver": "Revenue Enablement",
                "Metric Impact": "Faster simulations & Quicker time-to-market"
            })
            
        # Cost/Infra/Maintenance -> Cost Reduction
        elif any(word in text for word in ["cost", "expensive", "overhead", "admin", "maintenance", "manage"]):
            driver_map.append({
                "Pain Point": pp,
                "Value Lever": "Managed SaaS & Micro-partitioning",
                "Financial Driver": "Cost Reduction",
                "Metric Impact": "Lower storage footprints & Zero tuning labor"
            })
            
        # Sharing/Silos/Risk -> Risk Reduction
        elif any(word in text for word in ["govern", "compliance", "silo", "secure", "protect", "risk", "share", "collaboration"]):
            driver_map.append({
                "Pain Point": pp,
                "Value Lever": "Secure Data Sharing (No copy)",
                "Financial Driver": "Risk Reduction",
                "Metric Impact": "Eliminated FTP ingestion overhead & High governance"
            })
            
        # ML/AI/Scaling -> Revenue Enablement
        elif any(word in text for word in ["ai", "model", "scale", "growth", "volume"]):
             driver_map.append({
                "Pain Point": pp,
                "Value Lever": "Snowpark / Unlimited Concurrency",
                "Financial Driver": "Revenue Enablement",
                "Metric Impact": "Unblocked quant teams & Higher model volume"
            })
            
        else:
            # Fallback
            driver_map.append({
                "Pain Point": pp,
                "Value Lever": "Data Cloud Consolidation",
                "Financial Driver": "Cost Reduction",
                "Metric Impact": "Consolidated tool sprawl"
            })
            
    return driver_map

def generate_followup_questions(pain_points, primary_use_case):
    """
    Generates context-aware discovery questions for the Value Engineer to ask next.
    """
    questions = []
    
    if any("performance" in p.lower() for p in pain_points):
        questions.append(f"Can you quantify the business impact when {primary_use_case} workloads timeout? (e.g., lost productivity, delayed campaigns)")
    if any("overhead" in p.lower() for p in pain_points):
        questions.append("How many FTE hours per week are currently dedicated just to 'keeping the lights on' (tuning, backups)?")
    if any("silo" in p.lower() for p in pain_points):
        questions.append("If data sharing was instantaneous and secure, what new business capabilities would that unlock?")
        
    # Always append a generic value constraint question
    questions.append("What is the compelling event driving this modernization initiative right now?")
        
    return questions

def run_workshop_summarizer():
    """
    Orchestrates the 'VE Workshop Facilitator Mode'.
    Reads the scraped facts from the data_pipeline and outputs a structured VE plan.
    """
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "scraped_blk_facts.json")
    
    try:
        with open(data_path, "r") as f:
            facts = json.load(f)
    except FileNotFoundError:
        return {"Raw_Transcript": "No scraped data found. Run scrape_blackrock_urls.py.", "Extracted_Pain_Points": [], "Hypothesized_Value_Drivers": {}, "VE_Next_Discovery_Questions": []}
        
    # Combine all scraped context into one transcript for the AI to parse
    transcript = "\\n".join(facts.values())
    use_case = "Aladdin Data Cloud"
    
    pain_points = extract_pain_points(transcript)
    value_drivers = generate_value_driver_map(pain_points)
    next_questions = generate_followup_questions(pain_points, use_case)
    
    return {
        "Raw_Transcript": tuple(facts.keys()), # just returning the keys as context info instead of massive text blobs
        "Extracted_Pain_Points": pain_points,
        "Hypothesized_Value_Drivers": value_drivers,
        "VE_Next_Discovery_Questions": next_questions
    }

if __name__ == "__main__":
    # Test the agent parser with the actual BlackRock scraped facts
    print(f"\\n--- Running AI Agent VE Summarizer for: BlackRock Aladdin ---")
    result = run_workshop_summarizer()
    print(json.dumps(result, indent=2))
