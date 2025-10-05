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
)
from InquirerPy import inquirer
from datetime import datetime
from processing.config import get_api_key, save_api_key
from fetchers.news_api import validate_api_key

try:
    from bs4 import GuessedAtParserWarning

    warnings.filterwarnings("ignore", category=GuessedAtParserWarning)
except ImportError:
    pass


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


def process_keyword(keyword, data):
    current_keyword = keyword

    # --- Wikipedia ---
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


def main():
    try:
        while True:
            splash()

            list_of_keys = prompt_keywords()

            if not list_of_keys:
                console.print("\n[warn]⚠️ No keywords entered.[/warn]")
                if not inquirer.confirm(message="Do you want to try again?", default=True).execute():
                    console.print("\n[bold cyan]Exiting. Thank you for using SourceFolio![/bold cyan]")
                    sys.exit(0)
                else:
                    continue

            data = {
                keyword: {"wiki": {"is_detailed": None, "data": {}}, "news": [], "olib": []}
                for keyword in list_of_keys
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
                        choices=[
                            {"name": "Summary", "value": False},
                            {"name": "Detailed", "value": True},
                        ],
                        default=False,
                    ).execute()
                    data[keyword]["wiki"]["is_detailed"] = ans

            console.rule("[primary]Preview[/primary]")
            for key, value in data.items():
                status = "Detailed" if value["wiki"]["is_detailed"] else "Summary"
                console.print(f"[secondary]Keyword:[/secondary] {key} → [primary]{status}[/primary]")
            console.rule()

            console.print("\n[primary]Starting data collection...[/primary]\n")

            check_and_prompt_for_api_key()

            for keyword in list(data.keys()):
                if keyword in data:
                    process_keyword(keyword, data)

            has_data = False
            if data:
                for k in data:
                    if (data[k].get("wiki", {}).get("data", {}).get("content")) or \
                       data[k].get("olib") or \
                       data[k].get("news"):
                        has_data = True
                        break
            
            if not has_data:
                console.print("\n[warn]No data was collected for any of the keywords.[/warn]")
                if inquirer.confirm(message="Do you want to perform another research?", default=True).execute():
                    continue
                else:
                    console.print("\n[bold cyan]Thank you for using SourceFolio![/bold cyan]")
                    break

            else:
                console.print("\n[success]Data collection done![/success]")
                
                preview_selection(data)
                console.rule("[primary]Export[/primary]")
                console.print("\n[secondary]Data collection complete. Next step: export (PDF/CSV).[/secondary]\n")

                export_choice = inquirer.select(
                    message="Choose export format:",
                    choices=["PDF", "CSV", "Both", "Skip"],
                    default="PDF",
                ).execute()

                ts = datetime.now().strftime("%Y%m%d_%H%M%S")

                if export_choice == "PDF":
                    pd.export_to_pdf(data, f"research_output_{ts}.pdf")
                    console.print(f"\n[success]Exported to research_output_{ts}.pdf[/success]")
                elif export_choice == "CSV":
                    cd.export_to_csv(data, f"research_output_{ts}.csv")
                    console.print(f"\n[success]Exported to research_output_{ts}.csv[/success]")
                elif export_choice == "Both":
                    pd.export_to_pdf(data, f"research_output_{ts}.pdf")
                    cd.export_to_csv(data, f"research_output_{ts}.csv")
                    console.print(f"\n[success]Exported to research_output_{ts}.pdf and research_output_{ts}.csv[/success]")
                else:
                    console.print("\n[secondary]Export skipped. Thank you for using SourceFolio![/secondary]")

            if inquirer.confirm(message="Do you want to perform another research?", default=False).execute():
                continue
            else:
                console.print("\n[bold cyan]Thank you for using SourceFolio![/bold cyan]")
                break

    except KeyboardInterrupt:
        console.print("\n\n[bold red]Program interrupted by user. Exiting.[/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()