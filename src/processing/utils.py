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


def fetch_with_progress(message, fetch_func, *args, **kwargs):
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
            if not result: 
                progress.update(task_id, description=f"{message} [bold red]failed ✘[/bold red]")
                progress.stop()
                return result
            progress.update(task_id, description=f"{message} [bold green]completed ✔[/bold green]")
            progress.stop()
        except Exception as e:
            progress.update(task_id, description=f"{message} [bold red]failed ✘[/bold red]")
            progress.stop()
            raise e
    return result


def format_author(list):
    author = ""
    for auth in list:
        author = author + auth
    if author.strip() == "":
        author = "Unknown"

    return author