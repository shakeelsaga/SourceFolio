from fetchers import wikipedia_function as wiki, openlibrary_api as olib, news_api as news
from processing import pdf_exporter as pd, csv_exporter as cd
from processing import utils
import warnings
import wikipedia as wp
import sys
from processing.ui import splash, prompt_keywords, prompt_mode, preview_selection, console
from InquirerPy import inquirer

try:
    from bs4 import GuessedAtParserWarning
    warnings.filterwarnings("ignore", category=GuessedAtParserWarning)
except Exception:
    pass


splash()

list_of_keys = prompt_keywords()

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

choice = prompt_mode()

if choice == 1:
    for keyword in list_of_keys:
        data[keyword]["wiki"]["is_detailed"] = False
elif choice == 2:
    for keyword in list_of_keys:
        data[keyword]["wiki"]["is_detailed"] = True
else:
    console.print("\n[secondary]For each keyword, choose detail level.[/secondary]\n")
    for keyword in list_of_keys:
        ans = inquirer.select(
            message=f"{keyword}:",
            choices=[("Summary", "n"), ("Detailed", "y")],
            default="n"
        ).execute()
        data[keyword]["wiki"]["is_detailed"] = True if ans == "y" else False

console.rule("[primary]Preview[/primary]")
for key, value in data.items():
    status = "Detailed" if value["wiki"]["is_detailed"] else "Summary"
    console.print(f"[secondary]Keyword:[/secondary] {key} → [primary]{status}[/primary]")
console.rule()

console.print("\n[primary]Starting data collection...[/primary]\n")

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

            # If your fetcher swallowed ambiguity and returned nothing, handle it here
            if not wiki_data or not wiki_data.get("content"):
                console.print(f"\n[warn]No definitive Wikipedia page found for '{keyword}'.[/warn]")
                new_kw = inquirer.text(
                    message="Enter a more specific keyword (or leave blank to skip):"
                ).execute().strip()
                if new_kw:
                    # move the data bucket to the refined keyword and try again
                    data[new_kw] = data.pop(keyword)
                    keyword = new_kw
                    continue
            # success (or user chose to skip) → move on
            break

        except wp.DisambiguationError as e:
            console.print(f"\n[warn]The keyword '{keyword}' is ambiguous. Some possible options:[/warn]")
            for option in e.options[:8]:
                print(f"- {option}")
            new_kw = inquirer.text(
                message="Please refine the keyword and re-enter (or leave blank to skip):"
            ).execute().strip()
            if not new_kw:
                console.print("Skipping Wikipedia for this term.")
                break
            # move the bucket to new key and retry
            data[new_kw] = data.pop(keyword)
            keyword = new_kw
            # loop continues and re-fetches

        except wp.PageError:
            console.print(f"\n[warn]Could not find a Wikipedia page for '{keyword}'.[/warn]")
            new_kw = inquirer.text(
                message="Enter a different keyword (or leave blank to skip):"
            ).execute().strip()
            if not new_kw:
                console.print("Skipping Wikipedia for this term.")
                break
            data[new_kw] = data.pop(keyword)
            keyword = new_kw
            # loop continues and re-fetches

    # OpenLibrary
    try:
        books = utils.fetch_with_animation(
            f"Gathering book data for '{keyword}'",
            olib.get_books,
            keyword
        )

        while not books:  # retry until user decides to skip
            console.print(f"\n[warn]Could not find any book for '{keyword}'.[/warn]")
            new_kw = inquirer.text(
                message="Enter a different keyword (or leave blank to skip):"
            ).execute().strip()
            if not new_kw:
                console.print("Skipping fetching books for this term.")
                break
            # move the data bucket to the refined keyword and try again
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

        while not news_data:  # retry until user decides to skip
            console.print(f"\n[warn]Could not find any News article for '{keyword}'.[/warn]")
            new_kw = inquirer.text(
                message="Enter a different keyword (or leave blank to skip):"
            ).execute().strip()
            if not new_kw:
                console.print("Skipping fetching news for this term.")
                break
            # move the data bucket to the refined keyword and try again
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

    console.print()

console.print("\n[success]Data collection done![/success]")

preview_selection(data)

console.rule("[primary]Export Step[/primary]")
console.print("\n[secondary]Data collection complete. Next step: export (PDF/CSV).[/secondary]\n")

export_choice = inquirer.select(
    message="Choose export format:",
    choices=[
        "pdf",
        "csv",
        "both",
        "skip"
    ],
    default="pdf"
).execute()

if export_choice == "pdf":
    pd.export_to_pdf(data, "research_output.pdf")
    console.print("\n[success]Exported to research_output.pdf[/success]")
elif export_choice == "csv":
    cd.export_to_csv(data, "research_output.csv")
    console.print("\n[success]Exported to research_output.csv[/success]")
elif export_choice == "both":
    pd.export_to_pdf(data, "research_output.pdf")
    cd.export_to_csv(data, "research_output.csv")
    console.print("\n[success]Exported to both PDF and CSV[/success]")
else:
    console.print("\n[success]Export skipped. Thank you for using SourceFolio![/success]")
