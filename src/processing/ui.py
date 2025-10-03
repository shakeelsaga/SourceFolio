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
    console.rule("[primary]SourceFolio", style="primary")
    console.print(
        "[secondary]A fast research assistant for Wikipedia, Books, and News[/secondary]\n"
    )


def prompt_keywords(existing: List[str] | None = None) -> List[str]:
    kw_str = inquirer.text(
        message="Enter keywords (comma separated). Press Enter for multi-line:",
        default=", ".join(existing or []),
    ).execute()
    if not kw_str.strip():
        kw_str = (
            inquirer.editor(message="Enter keywords (one per line):").execute() or ""
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


def preview_selection(data_model: Dict[str, Dict[str, Any]]):
    table = Table("Keyword", "Wikipedia Title", "Books/News", show_lines=False)
    for key, sections in data_model.items():
        title = sections["wiki"]["data"].get("title") or "—"
        bn = f"{len(sections.get('olib', []))} books, {len(sections.get('news', []))} articles"
        table.add_row(key, title, bn)
    console.print(Panel(table, title="Preview", border_style="primary"))

@app.command()
def run():
    splash()
    # we’ll call your main3 logic here step by step


if __name__ == "__main__":
    app()
