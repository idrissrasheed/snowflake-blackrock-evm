import os
import re
import json
from bs4 import BeautifulSoup

def extract_financial_levers():
    """
    Scans the downloaded SEC filings for BlackRock (BLK) to extract
    realistic benchmark percentages for the EVM Engine.
    """
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sec_data", "sec-edgar-filings", "BLK", "10-K")
    
    if not os.path.exists(base_dir):
        print("SEC data not found. Run ingest_sec_data.py first.")
        return None
        
    extracted_data = {
        "implied_storage_compression_improvement": 0.30, # Fallback baseline
        "implied_compute_efficiency_gain": 0.25,        # Fallback baseline
        "operating_margin": 0.0,
        "revenue_growth": 0.0
    }
    
    print("Scanning 10-K filings for economic benchmarks...")
    
    try:
        # Just grab the first available 10-K directory as a sample extraction
        filing_dirs = os.listdir(base_dir)
        if filing_dirs:
            target_file = os.path.join(base_dir, filing_dirs[-1], "primary-document.html")
            if os.path.exists(target_file):
                with open(target_file, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    soup = BeautifulSoup(content, 'html.parser')
                    text_content = soup.get_text()
                    
                    # 1. Search for Operating Margin
                    # Operating margin gives us a sense of their operational efficiency
                    margin_match = re.search(r'operating margin(?:.*?)(\d{2})%', text_content, re.IGNORECASE)
                    if margin_match:
                        extracted_data["operating_margin"] = int(margin_match.group(1)) / 100.0
                        print(f"Found Operating Margin: {margin_match.group(1)}%")
                    
                    # 2. Search for Revenue Growth (as a proxy for scale/expansion)
                    growth_match = re.search(r'revenue growth(?:.*?)(\d{1,2})%', text_content, re.IGNORECASE)
                    if growth_match:
                        extracted_data["revenue_growth"] = int(growth_match.group(1)) / 100.0
                        print(f"Found Revenue Growth: {growth_match.group(1)}%")
            
    except Exception as e:
        print(f"Extraction error: {e}")
        
    # If we found an Operating Margin > 35% (BlackRock is highly profitable), 
    # it implies they have capital to invest in massive Aladdin infrastructure shifts.
    # We tune EVM compute efficiency gain up to 40% reflecting their high-end ML modeling needs.
    if extracted_data.get("operating_margin", 0) > 0.35:
        extracted_data["implied_compute_efficiency_gain"] = 0.40
        
    # Save the extracted benchmarks so the EVM engine can use them
    output_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "extracted_benchmarks.json")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(extracted_data, f, indent=4)
        
    print(f"\nExtraction complete. Saved to {output_file}")
    return extracted_data

if __name__ == "__main__":
    extract_financial_levers()
