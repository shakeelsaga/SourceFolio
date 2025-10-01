import requests

BASE_URL = "https://openlibrary.org/search.json"

def get_books(keyword, limit=5):
    """Fetch book results for a given keyword from OpenLibrary."""
    url = f"{BASE_URL}?q={keyword}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"OpenLibrary request failed: {response.status_code}")

    data = response.json()
    docs = data.get("docs", [])

    books = []
    for doc in docs[:limit]:
        books.append({
            "title": doc.get("title"),
            "author": ", ".join(doc.get("author_name", [])) if doc.get("author_name") else "Unknown",
            "first_publish_year": doc.get("first_publish_year"),
            "isbn": doc.get("isbn", ["N/A"])[0],
            "link": f"https://openlibrary.org{doc.get('key')}" if doc.get("key") else None,
            "edition_link": f"https://openlibrary.org/books/{doc.get('cover_edition_key')}" if doc.get("cover_edition_key") else None,
            "cover_image": f"https://covers.openlibrary.org/b/id/{doc.get('cover_i')}-L.jpg" if doc.get("cover_i") else None
        })
    return books

if __name__ == "__main__":
    bokkies = get_books("shakespere")
    print(bokkies)