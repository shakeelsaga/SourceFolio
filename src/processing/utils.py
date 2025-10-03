import time
import sys
import threading
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.console import Console

console = Console()


def keyword_separator(keywords):
    li = []
    word = ""
    for i in range(0, len(keywords)):
        if keywords[i] != ",":
            word = word + keywords[i]
        else:
            li.append(word.strip().capitalize())
            word = ""
    if word:
        li.append(word.strip().capitalize())
    return li


# New Rich-based fetch_with_progress function
def fetch_with_progress(message, fetch_func, *args, **kwargs):
    """Run fetch_func while showing a Rich progress bar."""
    result = None
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task_id = progress.add_task(message, total=None)
        try:
            result = fetch_func(*args, **kwargs)
            if not result:  # None, empty list, empty dict
                progress.update(task_id, description=f"[bold red]{message} failed ✘")
                progress.stop()
                console.print()
                return result
            progress.update(
                task_id, description=f"[bold green]{message} completed successfully ✔"
            )
            progress.stop()
            console.print()
        except Exception as e:
            progress.update(task_id, description=f"[bold red]{message} failed ✘")
            progress.stop()
            # The underlying function might print specific error, so we add a newline
            console.print()
            result = None  # Ensure result is None on exception
    return result


def format_author(list):
    author = ""
    for auth in list:
        author = author + auth
    if author.strip() == "":
        author = "Unknown"

    return author
