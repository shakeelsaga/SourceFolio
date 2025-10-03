import requests
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"


def default_date_range(days=7):
    from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")
    return from_date, to_date


def get_news(keyword, page_size=20, max_pages=1, days=7):
    from_date, to_date = default_date_range(days)
    articles = []

    for page in range(1, max_pages + 1):
        url = (
            f"{BASE_URL}?q={keyword}"
            f"&from={from_date}&to={to_date}"
            f"&sortBy=publishedAt&pageSize={page_size}&page={page}"
            f"&language=en&apiKey={API_KEY}"
        )
        response = requests.get(url)

        if response.status_code == 429:
            raise Exception("Rate limit exceeded. Try again later.")
        if response.status_code != 200:
            raise Exception(
                f"NewsAPI request failed: {response.status_code} {response.text}"
            )

        data = response.json()
        if data.get("status") != "ok":
            raise Exception(f"NewsAPI error: {data}")

        for article in data.get("articles", []):
            articles.append(
                {
                    "title": article.get("title") or "No title available",
                    "description": article.get("description")
                    or "No description available",
                    "url": article.get("url"),
                    "source": article.get("source", {}).get("name") or "Unknown",
                    "publishedAt": article.get("publishedAt"),
                }
            )

        if len(data.get("articles", [])) < page_size:
            break

    return articles


from rich.console import Console
from rich.table import Table

console = Console()

if __name__ == "__main__":
    try:
        results = get_news("shakespeare", page_size=5, max_pages=2)
        console.print(f"[bold green]Found {len(results)} articles[/bold green]")

        table = Table(title="News Articles")
        table.add_column("No.", justify="right")
        table.add_column("Title", style="cyan", no_wrap=True)
        table.add_column("Source", style="magenta")
        table.add_column("Published At", style="yellow")
        table.add_column("Description", style="white")

        for i, article in enumerate(results, start=1):
            table.add_row(
                str(i),
                article["title"],
                article["source"],
                article["publishedAt"] or "N/A",
                article["description"] or "N/A",
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
