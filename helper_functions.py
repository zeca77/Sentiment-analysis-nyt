import requests
import time
import sqlite3
BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
def _get_last_day(year, month):
    if month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        # Check for leap year
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 29
        return 28
    return 31


def fetch_articles(year, month, pages=1, api_key=None):
    articles = []
    begin_date = f"{year}{month:02d}01"
    last_day = _get_last_day(year, month)
    end_date = f"{year}{month:02d}{last_day}"

    for page in range(0, pages):  # Fetch articles (n pages * 10 articles)
        try:
            params = {
                "api-key": api_key,
                "begin_date": begin_date,
                "end_date": end_date,
                "fq": 'section.name:("U.S." "World")',
                "page": page
            }

            response = requests.get(BASE_URL, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if "response" in data and "docs" in data["response"]:
                    articles.extend([doc["headline"]["main"] for doc in data["response"]["docs"]])
            else:
                print(f"Request failed with status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Request error occurred: {e}")
            time.sleep(30)  # Wait longer on error
            continue

        time.sleep(6)  # Rate limiting
        print('sleeping.....')
    return articles

