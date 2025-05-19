from datetime import date, timedelta
import requests
import time

BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

def fetch_articles_by_week(year, week, pages=1, api_key=None, max_retries=5):
    articles = []

    # Get start and end dates of the ISO week
    start_of_week = date.fromisocalendar(year, week, 1)  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    begin_date = start_of_week.strftime("%Y%m%d")
    end_date = end_of_week.strftime("%Y%m%d")

    for page in range(0, pages):
        retries = 0
        while retries <= max_retries:
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
                    break  # success, exit retry loop

                elif response.status_code == 429: # Too many requests error
                    wait = 2 ** retries
                    print(f"Rate limit hit (429). Retrying in {wait} seconds...")
                    time.sleep(wait)
                    retries += 1
                else:
                    print(f"Request failed with status code: {response.status_code}")
                    break

            except requests.exceptions.RequestException as e:
                print(f"Request error occurred: {e}")
                time.sleep(30)
                retries += 1

        time.sleep(8)  # Rate limiting
        print('Sleeping...')

    return articles