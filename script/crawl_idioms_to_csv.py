import time
import csv
import requests
from bs4 import BeautifulSoup
from typing import List

BASE_URL = "https://www.theidioms.com/list/page/{}/"
TOTAL_PAGES = 228
OUTPUT_CSV = "idioms_sorted.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; IdiomCrawler/1.0; +https://example.com)"
}


def fetch_idioms_from_page(page: int) -> List[str]:
    url = BASE_URL.format(page)
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    idioms = []
    for a in soup.select("div.idiom p.idt strong a"):
        idiom = a.get_text(strip=True)
        if idiom:
            idioms.append(idiom)

    return idioms


def crawl_all_idioms() -> List[str]:
    all_idioms = []

    for page in range(1, TOTAL_PAGES + 1):
        try:
            idioms = fetch_idioms_from_page(page)
            all_idioms.extend(idioms)
            print(f"Page {page}: {len(idioms)} idioms")
        except Exception as e:
            print(f"⚠️ Failed page {page}: {e}")

        time.sleep(0.5)  # polite delay

    return all_idioms


def save_to_csv(idioms: List[str], path: str):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # writer.writerow(["idiom"])
        for idiom in idioms:
            writer.writerow([idiom])


if __name__ == "__main__":
    idioms = crawl_all_idioms()

    # Remove duplicates while preserving order
    idioms = list(dict.fromkeys(idioms))

    # Sort by starting character (case-insensitive)
    idioms.sort(key=lambda s: s.lower())

    save_to_csv(idioms, OUTPUT_CSV)

    print(f"\n✅ Saved {len(idioms)} sorted idioms to {OUTPUT_CSV}")

