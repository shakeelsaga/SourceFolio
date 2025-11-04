# This script handles the user interface of the application.
# It uses the rich and InquirerPy libraries to create a beautiful and interactive command-line interface.

from typing import List, Dict, Any
from rich.console import Console
from typing import List, Dict, Any, Optional
from rich.panel import Panel
from rich.table import Table
from rich.progress import (
    Progress,
    BarColumn,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.theme import Theme
from rich.traceback import install as rich_tracebacks
from InquirerPy import inquirer
import typer

# I'm creating a console object with a custom theme for styling the output.
console = Console(
    theme=Theme(
        {
            "primary": "bold cyan",
            "secondary": "bright_black",
            "success": "green",
            "warn": "yellow",
            "error": "bold red",
        }
    )
)

# I'm installing rich tracebacks for beautiful and readable error messages.
rich_tracebacks(show_locals=False)

# I'm creating a typer application.
app = typer.Typer(help="A CLI tool for collecting research data")

# This function displays the splash screen of the application.

def splash():
    console.rule("[primary]SourceFolio[/primary]", style="primary")
    console.print(Panel(
        "[bold cyan]Welcome to SourceFolio![/bold cyan]\n\n" +
        "A tool to help gather research from Wikipedia, OpenLibrary, and NewsAPI.\n\n" +
        "For full documentation and instructions, please visit the GitHub repository:\n" +
        "[bold][link=https://github.com/shakeelsaga/SourceFolio]https://github.com/shakeelsaga/SourceFolio[/link][/bold]\n\n" +
        "Created by: [bold][link=https://github.com/shakeelsaga]shakeelsaga (https://github.com/shakeelsaga)[/link][/bold]",
        title="[secondary]Interactive Mode[/secondary]",
        border_style="primary",
        padding=(1, 1)
    ))
    console.print()

# This function prompts the user to enter keywords.
# It supports both comma-separated keywords and multi-line input.
def prompt_keywords(existing: Optional[List[str]] = None) -> List[str]:
    kw_str = inquirer.text(
        message="Enter keywords (comma separated). Press Enter for multi-line:",
        default=", ".join(existing or []),
    ).execute()
    if not kw_str.strip():
        kw_str = (
            inquirer.text(
                message="Enter keywords (one per line, press 'Enter' to go to the next line):",
                multiline=True,
            ).execute() or ""
        )
    kws = [k.strip() for k in kw_str.replace("\n", ",").split(",") if k.strip()]
    return kws

# This function prompts the user to select the Wikipedia data mode.
# The user can choose between summary, full details, or manual selection for each keyword.
def prompt_mode() -> int:
    choice = inquirer.select(
        message="Select Wikipedia data mode:",
        choices=[
            {"name": "Summary only", "value": 1},
            {"name": "Full details", "value": 2},
            {"name": "Manual (choose per keyword)", "value": 3},
        ],
        default=1,
    ).execute()
    return int(choice)

# This function displays a simple exit message.
def exit_message():
    console.print("\n[bold cyan]Exiting. Thank you for using SourceFolio![/bold cyan]")

# This function displays a preview of the collected data in a table.
def preview_selection(data_model: Dict[str, Dict[str, Any]]):
    table = Table("Keyword", "Wikipedia Title", "Books/News", show_lines=False)
    for key, sections in data_model.items():
        title = sections["wiki"]["data"].get("title") or "—"
        url = sections["wiki"]["data"].get("url")

        # Create a clickable link if a URL exists
        title_display = f"[link={url}]{title}[/link]" if url and title != "—" else title

        bn = f"{len(sections.get('olib', []))} books, {len(sections.get('news', []))} articles"
        table.add_row(key, title_display, bn)
    console.print(Panel(table, title="[primary]Preview[/primary]", border_style="primary"))

# This is the main command for the typer application.
@app.command()
def run():
    splash()


if __name__ == "__main__":
    app()