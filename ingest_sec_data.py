import os
from sec_edgar_downloader import Downloader

# SEC requires a company name and email address to form the User-Agent string
dl = Downloader("Risk Analysis Agent", "idris@example.com", "./sec_data")

def download_filings(ticker="BLK", years=[2020, 2021, 2022, 2023, 2024, 2025]):
    print(f"Downloading SEC filings for {ticker}...")
    for year in years:
        try:
            # Download 10-K (Annual Reports)
            print(f"Fetching {year} 10-K...")
            # The API uses 'after' and 'before' for filtering by date, we can filter by year using strings
            dl.get("10-K", ticker, after=f"{year}-01-01", before=f"{year}-12-31")
            
        except Exception as e:
            print(f"Error fetching data for {year}: {e}")
            
    print("\nDownload complete. Files saved to ./sec_data")

if __name__ == "__main__":
    download_filings()
