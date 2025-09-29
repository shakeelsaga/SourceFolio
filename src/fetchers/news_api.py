import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")  # set your key in environment for safety
BASE_URL = "https://newsapi.org/v2/everything"

def get_news(keyword, page_size=5):
    """Fetch top news articles for a given keyword using NewsAPI."""
    url = f'{BASE_URL}?q={keyword}&sortBy=relevancy&pageSize={page_size}&language=en&apiKey={API_KEY}'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"NewsAPI request failed: {response.status_code} {response.text}")

    data = response.json()
    if data.get("status") != "ok":
        raise Exception(f"NewsAPI error: {data}")

    articles = []
    for article in data.get("articles", []):
        articles.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "url": article.get("url"),
            "source": article.get("source", {}).get("name"),
            "publishedAt": article.get("publishedAt")
        })
    return articles


if __name__ == "__main__":
    try:
        results = get_news("shakespere")
        print(f"Found {len(results)} articles:")
        for i, article in enumerate(results, start=1):
            print(f"{i}. '{article['title']}' ({article['source']})")
            print(f"  - {article['description']}")
            print(f"   {article['url']}")
            print("\n")
    except Exception as e:
        print("Error:", e)