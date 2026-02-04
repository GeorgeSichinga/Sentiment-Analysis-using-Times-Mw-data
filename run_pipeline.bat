@echo off
cd /d "C:\Users\Mtebetiii\Documents\Web sc\malawi_news"

REM activate venv
call venv\Scripts\activate.bat

REM run scrapers and analysis
python main.py
python scrapers\times_articles_scraper.py
python analyze_sentiment.py
