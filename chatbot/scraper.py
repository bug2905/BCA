import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def scrape_page(url):
    """Scrape text content from a webpage"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        texts = [p.get_text(strip=True) for p in soup.find_all("p")]
        return " ".join(texts) if texts else "No content found"
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)

    print("🌐 Enter website URLs (comma separated):")
    urls = input("👉 ").split(",")

    for i, url in enumerate(urls, start=1):
        url = url.strip()
        if not url:
            continue
        text = scrape_page(url)
        if text:
            filename = f"data/scraped_page{i}.csv"
            pd.DataFrame([{"url": url, "content": text}]).to_csv(filename, index=False)
            print(f"✅ Saved: {filename}")
