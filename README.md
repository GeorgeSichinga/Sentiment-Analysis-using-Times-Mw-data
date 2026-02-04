# Sentiment Analysis using Times.mw Data

An end‑to‑end news analytics project that scrapes articles from **Times.mw** (The Times Group, Malawi), runs **sentiment analysis**, auto‑tags **categories** (politics / economy / sports / other), and presents everything in an interactive **Streamlit dashboard**.

---

## Features

- **Web scraping (Times.mw)**  
  - Scrapes latest headlines and article URLs from Times.mw.  
  - Fetches full article content for each story.

- **Automatic categorisation**  
  - Simple keyword‑based classifier:  
    - `sports` – football, Flames, Super League, AFCON, etc.  
    - `politics` – parliament, elections, president, government, etc.  
    - `economy` – budget, finance, kwacha, inflation, business, etc.  
    - `other` – anything that doesn’t match the above.

- **Sentiment analysis (TextBlob)**  
  - Computes:
    - **Polarity** (−1 = very negative, +1 = very positive).  
    - **Subjectivity** (0 = objective, 1 = very subjective).  
  - Labels each article as `positive`, `neutral`, or `negative`.

- **Streamlit dashboard**
  - Filter articles by:
    - Source (currently Times),  
    - Category (politics / economy / sports / other),  
    - Sentiment (positive / neutral / negative).
  - Charts:
    - **Sentiment counts** (with color: positive = blue, neutral = black, negative = red).  
    - **Average polarity by category**.  
    - **Average subjectivity by category**.
  - Article view:
    - Title, category, sentiment, polarity, subjectivity, full text, and link to original article.
  - Simple custom styling and footer:
    - `© George Sichinga`.

- **Automation**
  - Batch script (`run_pipeline.bat`) designed to be scheduled with **Windows Task Scheduler** to:
    - Refresh headlines,
    - Rebuild articles with text + categories,
    - Recompute sentiment.

---

## Project Structure

```text
.
├─ dashboard/
│  └─ app.py                      # Streamlit dashboard
├─ scrapers/
│  ├─ times_scraper.py            # Scrapes Times.mw headlines + URLs
│  └─ times_articles_scraper.py   # Fetches full article text + auto-categorises
├─ data/                          # (Ignored in Git; generated at runtime)
│  ├─ times_headlines.csv
│  ├─ times_articles.csv
│  └─ times_articles_with_sentiment.csv
├─ analyze_sentiment.py           # Runs TextBlob sentiment over articles
├─ main.py                        # Orchestrates scrapers (Times headlines)
├─ run_pipeline.bat               # For Windows Task Scheduler
├─ requirements.txt               # Python dependencies
├─ .gitignore
└─ README.md
