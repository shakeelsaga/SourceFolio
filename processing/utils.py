# This script contains utility functions that are used across the application.
# These are helper functions that perform common tasks.

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

# This function takes a string of comma-separated keywords and returns a list of cleaned and capitalized keywords.
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

# This function displays a progress bar while a given function is executing.
# It's a nice way to give feedback to the user for long-running tasks.
def fetch_with_progress(message, fetch_func, *args, **kwargs):
    result = None
    # I'm using the rich library to create a progress bar.
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task_id = progress.add_task(message, total=None)
        try:
            # I'm executing the provided function.
            result = fetch_func(*args, **kwargs)
            
            # If the function returns None/Empty, mark as failed (soft fail)
            if not result: 
                progress.update(task_id, description=f"{message} [bold red]failed ✘[/bold red]")
                progress.stop()
                return None
            
            # If the function succeeds, I'm updating the progress bar to show a success message.
            progress.update(task_id, description=f"{message} [bold green]completed ✔[/bold green]")
            progress.stop()
            
        except Exception as e:
            # Update the progress bar to show failure visually
            progress.update(task_id, description=f"{message} [bold red]failed ✘[/bold red]")
            progress.stop()
            
            # Prints the error message so the user knows WHY the error occured
            console.print(f"   [bold red]Error:[/bold red] {str(e)}")
            
            return None
            
    return result

# This function takes a list of authors and formats it into a single string.
# If the list is empty, it returns "Unknown".
def format_author(list):
    author = ""
    for auth in list:
        author = author + auth
    if author.strip() == "":
        author = "Unknown"

    return author