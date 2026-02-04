import requests

def check_site(url):
    try:
        resp = requests.get(url, timeout=10)
        print(f"{url} -> status {resp.status_code}")
        print("First 100 chars:", resp.text[:100].replace("\n", " "))
    except Exception as e:
        print(f"Error for {url}: {e}")

if __name__ == "__main__":
    for u in [
        "https://example.com",
        "https://times.mw",
        "https://www.bbc.com",
        "https://www.mwnation.com",
        "https://malawi24.com",
    ]:
        check_site(u)
        print("-" * 60)
