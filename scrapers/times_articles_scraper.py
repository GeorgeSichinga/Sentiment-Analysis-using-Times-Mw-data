
from urllib.parse import urljoin
import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://times.mw"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def extract_article_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    candidates = [
        soup.find("div", class_="entry-content"),
        soup.find("div", class_="post-content"),
        soup.find("div", class_="td-post-content"),
    ]

    for c in candidates:
        if c:
            paragraphs = [p.get_text(strip=True) for p in c.find_all("p")]
            text = "\n".join([p for p in paragraphs if p])
            if text:
                return text

    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    text = "\n".join([p for p in paragraphs if p])
    return text


def fetch_article(url: str) -> str:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching article {url}: {e}")
        return ""
    return extract_article_text(resp.text)


def categorise_article(title: str, text: str) -> str:
    """
    Keyword-based categorisation: sports / politics / economy / other.
    Title is trusted more than body, to avoid noise from page templates.
    """
    title = title or ""
    text = text or ""
    title_lower = title.lower()
    text_lower = text.lower()

    sports_keywords_title = [
        "sports arena",
        "sports",
        "sport",
        "football",
        "soccer",
        "flames",
        "super league",
        "match",
        "matches",
        "goal",
        "goals",
        "coach",
        "player",
        "players",
        "tournament",
        "stadium",
        "afcon",
        "caf",
        "champions league",
        "fifa",
        "netball",
        "basketball",
        "league",
        "cup",
        "fixture",
        "kick-off",
        "kick off",
    ]
    sports_keywords_body = [
        "football",
        "soccer",
        "flames",
        "super league",
        "match",
        "tournament",
        "afcon",
        "stadium",
        "caf",
        "champions league",
        "fifa",
        "league",
        "cup",
    ]

    politics_keywords_title = [
        "election",
        "elections",
        "parliament",
        " mp ",
        "member of parliament",
        "president",
        "presidential",
        "minister",
        "cabinet",
        "politics",
        "politician",
        "campaign",
        "vote",
        "voting",
        "government",
        "opposition",
        "ruling party",
    ]
    politics_keywords_body = [
        "government",
        "ministry",
        "parliament",
        "president",
        "minister",
        "cabinet",
        "mps",
        "party",
        "coalition",
    ]

    economy_keywords_title = [
        "economy",
        "economic",
        "budget",
        "finance",
        "financial",
        "inflation",
        "kwacha",
        "reserve bank",
        "rbm",
        "trade",
        "investment",
        "business",
        "tax",
        "revenue",
        "loan",
        "debt",
    ]
    economy_keywords_body = [
        "economy",
        "economic",
        "budget",
        "finance",
        "financial",
        "inflation",
        "kwacha",
        "reserve bank",
        "rbm",
        "trade",
        "investment",
        "business",
        "tax",
        "revenue",
        "loan",
        "debt",
        "imports",
        "exports",
    ]

    def contains_any(text_value: str, keywords):
        return any(kw in text_value for kw in keywords)

    # 1) Sports first, based on TITLE
    if contains_any(title_lower, sports_keywords_title):
        return "sports"
    # 2) Then politics/economy based on TITLE
    if contains_any(title_lower, politics_keywords_title):
        return "politics"
    if contains_any(title_lower, economy_keywords_title):
        return "economy"

    # 3) If title is ambiguous, look at BODY (but body can be noisy)
    if contains_any(text_lower, sports_keywords_body):
        return "sports"
    if contains_any(text_lower, politics_keywords_body):
        return "politics"
    if contains_any(text_lower, economy_keywords_body):
        return "economy"

    return "other"



def build_times_articles(
    headlines_csv: str = "data/times_headlines.csv",
    output_csv: str = "data/times_articles.csv",
):
    headlines_path = Path(headlines_csv)
    if not headlines_path.exists():
        print(f"Headlines file not found: {headlines_path}")
        return

    df_headlines = pd.read_csv(headlines_path)
    articles = []

    for idx, row in df_headlines.iterrows():
        url = row.get("url")
        title = row.get("title")
        source = row.get("source", "Times")

        if not isinstance(url, str) or not url.startswith("http"):
            continue

        print(f"[{idx+1}/{len(df_headlines)}] Fetching article: {title}")
        text = fetch_article(url)
        if not text:
            print("  -> No text extracted.")
        else:
            print(f"  -> Extracted {len(text)} characters.")

        category = categorise_article(title, text)

        articles.append(
            {
                "source": source,
                "title": title,
                "url": url,
                "category": category,
                "text": text,
            }
        )

        time.sleep(1)  # be polite

    df_articles = pd.DataFrame(articles)
    out_path = Path(output_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df_articles.to_csv(out_path, index=False)
    print(f"Saved {len(df_articles)} articles with text to {out_path}")


if __name__ == "__main__":
    build_times_articles()



