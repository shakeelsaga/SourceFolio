# This script is responsible for fetching book information from the OpenLibrary API.
# It provides a function to get a list of books based on a keyword.

import requests
from rich.console import Console
from rich.table import Table

# I'm setting the base URL for the OpenLibrary API.
BASE_URL = "https://openlibrary.org/search.json"

# This function fetches a list of books for a given keyword.
def get_books(keyword, limit=5):
    url = f"{BASE_URL}?q={keyword}"
    try:
        # I'm making a GET request to the OpenLibrary API.
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        # I'm handling potential errors from the API.
        raise Exception(f"OpenLibrary request failed: {e}")

    data = response.json()
    docs = data.get("docs", [])

    books = []
    # I'm extracting the relevant information for each book and adding it to the list.
    for doc in docs[:limit]:
        books.append(
            {
                "title": doc.get("title"),
                "author": (
                    ", ".join(doc.get("author_name", []))
                    if doc.get("author_name")
                    else "Unknown"
                ),
                "first_publish_year": doc.get("first_publish_year"),
                "isbn": doc.get("isbn", ["N/A"])[0],
                "link": (
                    f"https://openlibrary.org{doc.get('key')}"
                    if doc.get("key")
                    else None
                ),
                "edition_link": (
                    f"https://openlibrary.org/books/{doc.get('cover_edition_key')}"
                    if doc.get("cover_edition_key")
                    else None
                ),
                "cover_image": (
                    f"https://covers.openlibrary.org/b/id/{doc.get('cover_i')}-L.jpg"
                    if doc.get("cover_i")
                    else None
                ),
            }
        )
    return books

# This block is for testing the script directly.
if __name__ == "__main__":
    console = Console()
    try:
        # I'm fetching books for the keyword "shakespeare".
        books = get_books("shakespeare")
        # I'm creating a table to display the results in a user-friendly way.
        table = Table(title="OpenLibrary Books")
        table.add_column("Title", style="cyan")
        table.add_column("Author", style="magenta")
        table.add_column("First Published", justify="center")
        table.add_column("ISBN", style="yellow")
        for b in books:
            table.add_row(
                b["title"] or "N/A",
                b["author"] or "Unknown",
                str(b["first_publish_year"] or "N/A"),
                b["isbn"] or "N/A",
            )
        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
