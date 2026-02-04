from scrapers.times_scraper import (
    fetch_times_headlines,
    save_times_headlines_to_csv,
)
from scrapers.nation_scraper import (
    fetch_nation_headlines,
    save_nation_headlines_to_csv,
)


def run_all_scrapers():
    total_articles = 0

    # Times
    times_data = fetch_times_headlines()
    if times_data:
        save_times_headlines_to_csv(times_data)
        total_articles += len(times_data)

    # Nation
    nation_data = fetch_nation_headlines()
    if nation_data:
        save_nation_headlines_to_csv(nation_data)
        total_articles += len(nation_data)

    print(f"Total collected: {total_articles} articles")


if __name__ == "__main__":
    run_all_scrapers()
