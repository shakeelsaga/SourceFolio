# This is the main script that orchestrates the entire research process.
# It brings together all the different modules to fetch, process, and export data.

from fetchers import (
    wikipedia_function as wiki,
    openlibrary_api as olib,
    news_api as news,
)
from processing import pdf_exporter as pd, csv_exporter as cd
from processing import utils
import warnings
import wikipedia as wp
import sys
from processing.ui import (
    splash,
    prompt_keywords,
    prompt_mode,
    preview_selection,
    console,
    exit_message,
)
from InquirerPy import inquirer
from datetime import datetime
from processing.config import get_api_key, save_api_key
from fetchers.news_api import validate_api_key

# I'm ignoring a specific warning from BeautifulSoup that is not relevant to the user.
try:
    from bs4 import GuessedAtParserWarning

    warnings.filterwarnings("ignore", category=GuessedAtParserWarning)
except ImportError:
    pass

# This function checks for a NewsAPI key and prompts the user to enter one if it's not found.
# It also allows the user to use an existing key, change it, or remove it.
def check_and_prompt_for_api_key():
    existing_key = get_api_key("NEWS_API_KEY")

    if existing_key:
        masked_key = f"...{existing_key[-4:]}"
        console.print(f"[info]Found existing NewsAPI key: [cyan]{masked_key}[/cyan][/info]")
        action = inquirer.select(
            message="What would you like to do?",
            choices=[
                {"name": "Use this key", "value": "use"},
                {"name": "Enter a different key", "value": "change"},
                {"name": "Remove the key (skip news)", "value": "remove"},
            ],
            default="use",
        ).execute()

        if action == "use":
            if not validate_api_key(existing_key):
                console.print("[warn]The existing API key is no longer valid.[/warn]")
            else:
                console.print("[success]API key is valid.[/success]\n")
                return
        elif action == "remove":
            save_api_key(None, "NEWS_API_KEY")
            console.print("[info]API key removed. News fetching will be skipped.[/info]\n")
            return

    # If there's no existing key or the user wants to change it, I'm prompting for a new key.
    while True:
        new_key = inquirer.text(
            message="Please enter your NewsAPI key (or leave blank to skip news fetching):",
        ).execute()

        if not new_key:
            console.print("[info]No API key entered. News fetching will be skipped.[/info]\n")
            save_api_key(None, "NEWS_API_KEY")
            break

        if validate_api_key(new_key):
            save_api_key(new_key, "NEWS_API_KEY")
            console.print("[success]NewsAPI key is valid and has been saved.[/success]\n")
            break
        else:
            console.print("[error]The provided API key is invalid. Please try again.[/error]")

# This function processes a single keyword. It fetches data from Wikipedia, OpenLibrary, and NewsAPI.
# It also handles cases where a keyword is ambiguous or no data is found.
def process_keyword(keyword, data):
    current_keyword = keyword

    # --- Wikipedia ---
    # I'm fetching data from Wikipedia. If the keyword is ambiguous, I'm asking the user to refine it.
    while True:
        try:
            wiki_data = utils.fetch_with_progress(
                f"Gathering Wikipedia data for '{current_keyword}'",
                wiki.get_wiki_data,
                current_keyword,
                data[current_keyword]["wiki"]["is_detailed"],
            )
            if wiki_data and wiki_data.get("content"):
                data[current_keyword]["wiki"]["data"] = wiki_data
                break

            console.print(
                f"\n[warn]No definitive Wikipedia page found for '{current_keyword}'.[/warn]"
            )
            new_kw = (
                inquirer.text(
                    message="Enter a more specific keyword (or leave blank to skip):"
                )
                .execute()
                .strip()
            )
            if new_kw:
                data[new_kw] = data.pop(current_keyword)
                console.print(
                    f"[info]Keyword updated:[/info] '{current_keyword}' → '{new_kw}'\n"
                )
                current_keyword = new_kw
                continue
            else:
                console.print(
                    "[secondary]Skipping fetching Wikipedia for this term.[/secondary]\n"
                )
                break 

        except wp.DisambiguationError as e:
            from rich.table import Table

            console.print(
                f"\n[warn]The keyword '{current_keyword}' is ambiguous. Some possible options:[/warn]"
            )
            table = Table(title="Possible options")
            table.add_column("Suggestions", style="cyan")
            for option in e.options[:8]:
                table.add_row(option)
            console.print(table)
            new_kw = (
                inquirer.text(
                    message="Please refine the keyword and re-enter (or leave blank to skip):"
                )
                .execute()
                .strip()
            )
            if new_kw:
                data[new_kw] = data.pop(current_keyword)
                console.print(
                    f"[info]Keyword updated:[/info] '{current_keyword}' → '{new_kw}'\n"
                )
                current_keyword = new_kw
                continue
            else:
                console.print(
                    "[secondary]Skipping fetching Wikipedia for this term.[/secondary]\n"
                )
                break

        except wp.PageError:
            console.print(
                f"\n[warn]Could not find a Wikipedia page for '{current_keyword}'.[/warn]"
            )
            new_kw = (
                inquirer.text(
                    message="Enter a different keyword (or leave blank to skip):"
                )
                .execute()
                .strip()
            )
            if new_kw:
                data[new_kw] = data.pop(current_keyword)
                console.print(
                    f"[info]Keyword updated:[/info] '{current_keyword}' → '{new_kw}'\n"
                )
                current_keyword = new_kw
                continue
            else:
                console.print(
                    "[secondary]Skipping fetching Wikipedia for this term.[/secondary]\n"
                )
                break

    # --- OpenLibrary ---
    # I'm fetching book data from OpenLibrary.
    while True:
        books = utils.fetch_with_progress(
            f"Gathering book data for '{current_keyword}'",
            olib.get_books,
            current_keyword,
        )
        if books:
            if current_keyword in data:
                data[current_keyword]["olib"] = books
            break

        console.print(
            f"\n[warn]Could not find any book for '{current_keyword}'.[/warn]"
        )
        new_kw = (
            inquirer.text(message="Enter a different keyword (or leave blank to skip):")
            .execute()
            .strip()
        )
        if new_kw:
            if current_keyword in data:
                data[new_kw] = data.pop(current_keyword)
                console.print(
                    f"[info]Keyword updated:[/info] '{current_keyword}' → '{new_kw}'\n"
                )
            else:
                data[new_kw] = {
                    "wiki": {"is_detailed": None, "data": {}},
                    "news": [],
                    "olib": [],
                }
            current_keyword = new_kw
            continue
        else:
            console.print(
                "[secondary]Skipping fetching books for this term.[/secondary]\n"
            )
            break

    # --- News API ---
    # I'm fetching news data from NewsAPI, but only if an API key is available.
    if get_api_key("NEWS_API_KEY"):
        while True:
            news_data = utils.fetch_with_progress(
                f"Gathering news data for '{current_keyword}'",
                news.get_news,
                current_keyword,
            )
            if news_data:
                if current_keyword in data:
                    data[current_keyword]["news"] = news_data
                break

            console.print(
                f"\n[warn]Could not find any News article for '{current_keyword}'.[/warn]"
            )
            new_kw = (
                inquirer.text(message="Enter a different keyword (or leave blank to skip):")
                .execute()
                .strip()
            )
            if new_kw:
                if current_keyword in data:
                    data[new_kw] = data.pop(current_keyword)
                    console.print(
                        f"[info]Keyword updated:[/info] '{current_keyword}' → '{new_kw}'\n"
                    )
                else:
                    data[new_kw] = {
                        "wiki": {"is_detailed": None, "data": {}},
                        "news": [],
                        "olib": [],
                    }
                current_keyword = new_kw
                continue
            else:
                console.print(
                    "[secondary]Skipping fetching news for this term.[/secondary]\n"
                )
                break

    console.print("\n")

# This is the main function of the application.
# It guides the user through the process of entering keywords, selecting options, and exporting the data.
def main():
    try:
        while True:
            # I'm displaying the splash screen.
            splash()

            # I'm prompting the user to enter keywords.
            list_of_keys = prompt_keywords()

            # If no keywords are entered, I'm asking the user if they want to try again.
            if not list_of_keys:
                console.print("\n[warn]⚠️ No keywords entered.[/warn]")
                if not inquirer.confirm(message="Do you want to try again?", default=True).execute():
                    exit_message()
                    sys.exit(0)
                else:
                    continue

            # I'm initializing the data structure for the keywords.
            data = {
                keyword: {"wiki": {"is_detailed": None, "data": {}}, "news": [], "olib": []}
                for keyword in list_of_keys
            }

            # I'm prompting the user to select the Wikipedia data mode (summary or full details).
            choice = prompt_mode()

            if choice == 1:
                for keyword in list_of_keys:
                    data[keyword]["wiki"]["is_detailed"] = False
            elif choice == 2:
                for keyword in list_of_keys:
                    data[keyword]["wiki"]["is_detailed"] = True
            else:
                # If the user chooses manual mode, I'm asking for the detail level for each keyword.
                console.print("\n[secondary]For each keyword, choose detail level.[/secondary]\n")
                for keyword in list_of_keys:
                    ans = inquirer.select(
                        message=f"{keyword}:",
                        choices=[
                            {"name": "Summary", "value": False},
                            {"name": "Detailed", "value": True},
                        ],
                        default=False,
                    ).execute()
                    data[keyword]["wiki"]["is_detailed"] = ans

            # I'm showing a preview of the selected keywords and their detail level.
            console.rule("[primary]Preview[/primary]")
            for key, value in data.items():
                status = "Detailed" if value["wiki"]["is_detailed"] else "Summary"
                console.print(f"[secondary]Keyword:[/secondary] {key} → [primary]{status}[/primary]")
            console.rule()

            console.print("\n[primary]Starting data collection...[/primary]\n")

            # I'm checking for the NewsAPI key.
            check_and_prompt_for_api_key()

            # I'm processing each keyword to fetch the data.
            for keyword in list(data.keys()):
                if keyword in data:
                    process_keyword(keyword, data)

            # I'm checking if any data was collected.
            has_data = False
            if data:
                for k in data:
                    if (data[k].get("wiki", {}).get("data", {}).get("content")) or \
                       data[k].get("olib") or \
                       data[k].get("news"):
                        has_data = True
                        break
            
            # If no data was collected, I'm asking the user if they want to perform another research.
            if not has_data:
                console.print("\n[warn]No data was collected for any of the keywords.[/warn]")
                if inquirer.confirm(message="Do you want to perform another research?", default=True).execute():
                    continue
                else:
                    exit_message()
                    break

            else:
                # If data was collected, I'm showing a preview and prompting for export options.
                console.print("\n[success]Data collection done![/success]")
                
                preview_selection(data)
                console.rule("[primary]Export[/primary]")
                console.print("\n[secondary]Data collection complete. Next step: export (PDF/CSV).[/secondary]\n")

                export_choice = inquirer.select(
                    message="Choose export format:",
                    choices=["PDF", "CSV", "Both", "Skip"],
                    default="PDF",
                ).execute()

                # I'm creating a timestamp for the output files.
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")

                if export_choice == "PDF":
                    pd.export_to_pdf(data, f"research_output_{ts}.pdf")
                elif export_choice == "CSV":
                    cd.export_to_csv(data, f"research_output_{ts}.csv")
                elif export_choice == "Both":
                    pd.export_to_pdf(data, f"research_output_{ts}.pdf")
                    cd.export_to_csv(data, f"research_output_{ts}.csv")
                else:
                    console.print("\n[secondary]Export skipped. Thank you for using SourceFolio![/secondary]")

            # I'm asking the user if they want to perform another research.
            if inquirer.confirm(message="Do you want to perform another research?", default=False).execute():
                continue
            else:
                exit_message()
                break

    # I'm handling the KeyboardInterrupt exception to exit gracefully.
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Program interrupted by user. Exiting.[/bold red]")
        sys.exit(0)

# This is the entry point of the script.
if __name__ == "__main__":
    main()
