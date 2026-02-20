# Snowflake EVM Sales Agent: BlackRock Edition

This is a customized value engineering dashboard tailored exclusively for BlackRock's Aladdin Data Cloud expansion. It converts raw legacy IT costs into deterministic Snowflake ROI, TCO, and NPV metrics based on BlackRock's actual SEC financial footprint and public Snowflake pricing.

## Architecture

This project strictly follows the Value Engineering 4-Step Pitch Methodology:
1. **Customer Background (Aladdin)**
2. **Pain Points (Market Data Pipelines)**
3. **Snowflake Value Hypothesis**
4. **Financial Model & Credit Sizing**

## Core Components
* `evm_engine.py`: The deterministic math model. It consumes BlackRock's legacy spend, applies compute/storage efficiency multipliers extracted dynamically from their $BLK SEC 10-K filings, and maps the savings linearly across 3 years to project ROI, NPV, Total Savings, Payback Period, and required Snowflake Credits (AWS Enterprise pricing).
* `app.py`: The Streamlit-based interactive presentation. It visualizes the ROI calculations and explicit Value Drivers (Cost Reduction, Revenue Enablement, Risk Reduction).
* `ingest_sec_data.py`: Downloads BlackRock (BLK) 10-K filings natively from the SEC Edgar database from 2020 (the year prior to Aladdin's Snowflake launch) through 2025.
* `extract_sec_data.py`: A regex-based extraction tool that dynamically scours the 10-K filings to locate BlackRock's actual Operating Margin and Revenue Growth benchmarks to ground the EVM elasticity multipliers.
* `scrape_blackrock_urls.py`: A bespoke web scraper that captures factual snippets from exactly 4 core BlackRock/Snowflake web addresses (including Summit24 ML optimizations).

## Usage
1. Make sure all requirements are installed:
```bash
pip install -r requirements.txt
```
2. Pull the latest BlackRock SEC data:
```bash
python data_pipeline/ingest_sec_data.py
python data_pipeline/extract_sec_data.py
```
3. Scrape the bespoke URL facts:
```bash
python data_pipeline/scrape_blackrock_urls.py
```
4. Run the VE Presentation Dashboard:
```bash
streamlit run src/app.py
```
