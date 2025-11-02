# This script is responsible for fetching news articles from the NewsAPI.
# It provides functions to validate the API key and fetch news based on a keyword.

import requests
from datetime import datetime, timedelta
from processing.config import get_api_key

# I'm setting the base URL for the NewsAPI.
BASE_URL = "https://newsapi.org/v2/everything"

# This function validates the NewsAPI key.
# It makes a test request to the API and checks the response status code.
def validate_api_key(api_key):
    if not api_key:
        return False
    url = f"{BASE_URL}?q=test&apiKey={api_key}"
    try:
        response = requests.get(url)
        # A status code of 200 (OK) or 429 (Too Many Requests) means the key is likely valid.
        return response.status_code in [200, 429]
    except requests.RequestException:
        return False

# This function returns a default date range for the news search.
# It defaults to the last 7 days.
def default_date_range(days=7):
    from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")
    return from_date, to_date

# This is the main function that fetches news articles for a given keyword.
def get_news(keyword, page_size=20, max_pages=1, days=7):
    # I'm getting the API key from the config file.
    API_KEY = get_api_key("NEWS_API_KEY")
    if not API_KEY:
        raise Exception("NewsAPI key not found. Please configure it first.")

    # I'm setting the date range for the search.
    from_date, to_date = default_date_range(days)
    articles = []

    # I'm paginating through the results to get more articles if needed.
    for page in range(1, max_pages + 1):
        url = (
            f"{BASE_URL}?q={keyword}"
            f"&from={from_date}&to={to_date}"
            f"&sortBy=publishedAt&pageSize={page_size}&page={page}"
            f"&language=en&apiKey={API_KEY}"
        )
        response = requests.get(url)

        # I'm handling potential errors from the API.
        if response.status_code == 429:
            raise Exception("Rate limit exceeded. Try again later.")
        if response.status_code != 200:
            raise Exception(
                f"NewsAPI request failed: {response.status_code} {response.text}"
            )

        data = response.json()
        if data.get("status") != "ok":
            raise Exception(f"NewsAPI error: {data}")

        # I'm extracting the relevant information from each article and adding it to the list.
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

        # I'm breaking the loop if there are no more articles to fetch.
        if len(data.get("articles", [])) < page_size:
            break

    return articles


from rich.console import Console
from rich.table import Table

console = Console()

# This block is for testing the script directly.
if __name__ == "__main__":
    try:
        # I'm fetching news for the keyword "shakespeare".
        results = get_news("shakespeare", page_size=5, max_pages=2)
        console.print(f"[bold green]Found {len(results)} articles[/bold green]")

        # I'm creating a table to display the results in a user-friendly way.
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
