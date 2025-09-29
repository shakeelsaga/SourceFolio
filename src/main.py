from fetchers import wikipedia_function as wiki, openlibrary_api as olib, news_api as news
from processing import pdf_exporter as pd
from processing import utils
import warnings
import wikipedia as wp
import sys

try:
    from bs4 import GuessedAtParserWarning
    warnings.filterwarnings("ignore", category=GuessedAtParserWarning)
except Exception:
    pass


print(
    '''
==============================================================
       Welcome to the Automated Research Data Collector
==============================================================

Enter keywords to research and receive structured data including definitions (detailed or summary), recommended books, and recent news.

You may enter multiple keywords separated by commas ",".
'''
)

keywords = input("\nPlease enter your research keywords (separated by commas):\n>> ")
list_of_keys = utils.keyword_separator(keywords)

if not list_of_keys:
    print("⚠️ No keywords entered. Please try again.")
    sys.exit(1)

data = {
    keyword: {
        "wiki": {"is_detailed": None, "data": {}},
        "news": [],
        "olib": []
    } for keyword in list_of_keys
}

print(
    '''
============================
 Select Wikipedia Data Mode
============================
1. Summary only
2. Full details
3. Manual selection (choose for each keyword)
'''
)

while True:
    try:
        choice = int(input('Please enter your choice (1, 2, or 3):\n>> '))
        if choice in [1, 2, 3]:
            break
        else:
            print("\n⚠️ Invalid input, please try again.\n")
    except ValueError:
        print("\n⚠️ Invalid input, please try again.\n")

if choice == 1:
    for keyword in list_of_keys:
        data[keyword]["wiki"]["is_detailed"] = False
elif choice == 2:
    for keyword in list_of_keys:
        data[keyword]["wiki"]["is_detailed"] = True
else:
    print('\nFor each keyword, enter "y" for detailed explanation or "n" for summary.\n')
    for keyword in list_of_keys:
        while True:
            ans = input(f"{keyword}: ").strip().lower()
            if ans in ("y", "yes"):
                data[keyword]["wiki"]["is_detailed"] = True
                break
            elif ans in ("n", "no"):
                data[keyword]["wiki"]["is_detailed"] = False
                break
            else:
                print("⚠️ Invalid input! Please type y/n.\n")

print('\n========= Preview =========')
for key, value in data.items():
    status = "Detailed" if value["wiki"]["is_detailed"] else "Summary"
    print(f"Keyword: {key} → Mode: {status}")
print('=============================\n')

print("Starting data collection...\n")

for keyword in list_of_keys:
    # Wikipedia
    while True:
        try:
            wiki_data = utils.fetch_with_animation(
                f"Gathering Wikipedia data for '{keyword}'",
                wiki.get_wiki_data,
                keyword,
                data[keyword]["wiki"]["is_detailed"]
            )
            data[keyword]["wiki"]["data"] = wiki_data

            if not wiki_data or not wiki_data.get("content"):
                print(f"\n⚠️ No definitive Wikipedia page found for '{keyword}'.")
                new_kw = input(
                    "Enter a more specific keyword (e.g., 'python (programming)') "
                    "or press Enter to skip Wikipedia for this term:\n>> "
                ).strip()
                if new_kw:
                    data[new_kw] = data.pop(keyword)
                    keyword = new_kw
                    continue
            break

        except wp.DisambiguationError as e:
            print(f"\n⚠️ The keyword '{keyword}' is ambiguous. Some possible options:")
            for option in e.options[:8]:
                print(f"- {option}")
            new_kw = input(
                "\nPlease refine the keyword and re-enter "
                "(or press Enter to skip Wikipedia for this term):\n>> "
            ).strip()
            if not new_kw:
                print("Skipping Wikipedia for this term.")
                break
            data[new_kw] = data.pop(keyword)
            keyword = new_kw

        except wp.PageError:
            print(f"\n⚠️ Could not find a Wikipedia page for '{keyword}'.")
            new_kw = input(
                "Enter a different keyword "
                "(or press Enter to skip Wikipedia for this term):\n>> "
            ).strip()
            if not new_kw:
                print("Skipping Wikipedia for this term.")
                break
            data[new_kw] = data.pop(keyword)
            keyword = new_kw
            

try:
    books = utils.fetch_with_animation(
        f"Gathering book data for '{keyword}'",
        olib.get_books,
        keyword
    )

    while not books:
        print(f"\n⚠️ Could not find any book for '{keyword}'. ")
        new_kw = input(
            "Enter a different keyword "
            "(or press Enter to skip fetching books for this term):\n>> "
        ).strip()
        if not new_kw:
            print("Skipping fetching books for this term.")
            break
        data[new_kw] = data.pop(keyword)
        keyword = new_kw
        books = utils.fetch_with_animation(
            f"Gathering book data for '{keyword}'",
            olib.get_books,
            keyword
        )  

    data[keyword]["olib"] = books if books else []
except Exception:
    utils.status_update(f"Error fetching books for '{keyword}'", success=False)


# News API
try:
    news_data = utils.fetch_with_animation(
        f"Gathering news data for '{keyword}'",
        news.get_news,
        keyword
    )

    while not news_data:
        print(f"\n⚠️ Could not find any News article for '{keyword}'. ")
        new_kw = input(
            "Enter a different keyword "
            "(or press Enter to skip fetching articles for this term):\n>> "
        ).strip()
        if not new_kw:
            print("Skipping fetching news for this term.")
            break
        data[new_kw] = data.pop(keyword)
        keyword = new_kw
        news_data = utils.fetch_with_animation(
            f"Gathering news data for '{keyword}'",
            news.get_news,
            keyword
        )

    data[keyword]["news"] = news_data if news_data else []
except Exception:
    utils.status_update(f"Error fetching news for '{keyword}'", success=False)

    print()

print('\nData collection done!')

# Preview
print("\n========= Data Preview =========\n")
for key, sections in data.items():
    print("=" * 60)
    print(f"🔑 Keyword: {key}\n")

    # Wikipedia
    if sections["wiki"]["data"]:
        print("📘 Wikipedia")
        print(f"  Title   : {sections['wiki']['data'].get('title', 'N/A')}")
        content = sections['wiki']['data'].get('content', 'N/A')
        snippet = (content[:250] + "...") if isinstance(content, str) and len(content) > 250 else content
        print(f"  Summary : {snippet}")
        print(f"  URL     : {sections['wiki']['data'].get('url', 'N/A')}\n")
    else:
        print("📘 Wikipedia: No data available\n")

    # Books
    if sections["olib"]:
        print(f"📚 Books ({len(sections['olib'])} results)")
        for book in sections["olib"][:3]:
            title = book.get("title", "N/A")
            author = ""
            for auth in book.get("author"):
                author = author + auth
            if author.strip() == "":
                author = "Unknown"
            print(f"  - {title} by {author.strip()}")
        if len(sections["olib"]) > 3:
            print("  ... more results\n")
        else:
            print()
    else:
        print("📚 Books: No results found\n")

    # News
    if sections["news"]:
        print(f"📰 News ({len(sections['news'])} articles)")
        for article in sections["news"][:3]:
            headline = article.get("title", "N/A")
            source = article.get("source","Unknown")
            print(f"  - {headline} ({source})")
        if len(sections["news"]) > 3:
            print("  ... more articles\n")
        else:
            print()
    else:
        print("📰 News: No articles found\n")

print("=" * 60)
print("\nData collection complete. Next step: export (PDF/CSV).\n")

print('Do you want to export the research data to PDF?\nEnter "y" to proceed and "n" to exit.')
ans = input(">>")
if ans in ["yes", "y"]:
    pd.export_to_pdf(data, "research_output.pdf")
else:
    print("\nThank You for using the automated research data collector program!!")
    
