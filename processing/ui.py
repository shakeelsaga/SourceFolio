from typing import List, Dict, Any
from rich.console import Console
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

rich_tracebacks(show_locals=False)

app = typer.Typer(help="Research Collector CLI")


def splash():
    console.rule("[primary]SourceFolio[/primary]", style="primary")

    creator_url = "https://github.com/shakeelsaga"
    homepage_url = "https://github.com/shakeelsaga/sourcefolio"

    creator = f"[link={creator_url}]shakeelsaga[/link] ({creator_url})"
    homepage = f"[link={homepage_url}]SourceFolio[/link] ({homepage_url})"

    console.print(Panel(
        "[bold cyan]Welcome to SourceFolio![/bold cyan]\n\n"
        "This tool helps you gather research from Wikipedia, OpenLibrary, and NewsAPI.\n\n"
        f"[secondary]Created by:[/secondary] {creator}\n"
        f"[secondary]Homepage:[/secondary] {homepage}",
        title="[secondary]Interactive Mode[/secondary]",
        border_style="primary",
        padding=(1, 1, 1, 1)
    ))
    console.print()


def prompt_keywords(existing: List[str] | None = None) -> List[str]:
    kw_str = inquirer.text(
        message="Enter keywords (comma separated). Press Enter for multi-line:",
        default=", ".join(existing or []),
    ).execute()
    if not kw_str.strip():
        kw_str = (
            inquirer.text(
                message="Enter keywords (one per line, press Ctrl+D when done):",
                multiline=True,
            ).execute() or ""
        )
    kws = [k.strip() for k in kw_str.replace("\n", ",").split(",") if k.strip()]
    return kws


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


def exit_message():
    console.print("\n[bold cyan]Exiting. Thank you for using SourceFolio![/bold cyan]")

def preview_selection(data_model: Dict[str, Dict[str, Any]]):
    table = Table("Keyword", "Wikipedia Title", "Books/News", show_lines=False)
    for key, sections in data_model.items():
        title = sections["wiki"]["data"].get("title") or "—"
        bn = f"{len(sections.get('olib', []))} books, {len(sections.get('news', []))} articles"
        table.add_row(key, title, bn)
    console.print(Panel(table, title="[primary]Preview[/primary]", border_style="primary"))

@app.command()
def run():
    splash()


if __name__ == "__main__":
    app()