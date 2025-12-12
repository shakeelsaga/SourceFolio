# This script contains utility functions that are used across the application.
# These are helper functions that perform common tasks like progress bars and text formatting.

import time
import sys
import os  # Added for force kill
import concurrent.futures
from rich.progress import (
    Progress,
    SpinnerColumn,
    BarColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.console import Console
from InquirerPy import inquirer

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
# It uses a strict loop to allow the user to retry or exit if the connection fails.
def fetch_with_progress(message, fetch_func, *args, **kwargs):
    # I'm starting an infinite loop to keep retrying as long as the user wants.
    while True:
        result = None
        # I'm setting up the rich progress bar to give visual feedback.
        # I set transient=True so the bar disappears after it's done, keeping the UI clean.
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        ) as progress:
            task_id = progress.add_task(message, total=None)
            
            # I'm creating the executor manually instead of using 'with' context.
            # This prevents the app from blocking/waiting for stuck threads if a timeout occurs.
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            try:
                future = executor.submit(fetch_func, *args, **kwargs)
                
                # I'm giving the task 15 seconds max. If it takes longer, it raises TimeoutError.
                result = future.result(timeout=15)
                
                # If the function returns nothing (soft fail), I'm marking it as failed.
                if not result: 
                    progress.update(task_id, description=f"{message} [bold red]failed ✘[/bold red]")
                    progress.stop()
                    # Shutdown the executor but don't wait for it
                    executor.shutdown(wait=False)
                    return None
                
                # If successful, I'm updating the bar to show completion.
                progress.update(task_id, description=f"{message} [bold green]completed ✔[/bold green]")
                executor.shutdown(wait=False)
                return result

            except concurrent.futures.TimeoutError:
                # This catches the hanging issue.
                progress.update(task_id, description=f"{message} [bold red]timed out ✘[/bold red]")
                progress.stop()
                console.print(f"   [bold red]Error:[/bold red] Request timed out (server took too long).")
                # Important: Kill the executor reference so we don't wait for it
                executor.shutdown(wait=False)
                
            except Exception as e:
                # If a network error or crash happens, I'm catching it here.
                progress.update(task_id, description=f"{message} [bold red]failed ✘[/bold red]")
                progress.stop()
                executor.shutdown(wait=False)
                
                # I'm printing a simple connection lost message instead of the raw error.
                console.print(f"   [bold red]Connection lost.[/bold red]")
        
        # I'm asking the user what they want to do next: Retry or Exit.
        action = inquirer.select(
            message="Connection lost. What would you like to do?",
            choices=[
                {"name": "Retry Connection", "value": "retry"},
                {"name": "Exit Application", "value": "exit"},
            ],
            default="retry",
        ).execute()

        if action == "retry":
            console.print("[cyan]Retrying...[/cyan]")
            continue  # Loops back to try the function again.
        elif action == "exit":
            # I'm printing the standard exit message before quitting.
            console.print("\n[bold cyan]Exiting. Thank you for using SourceFolio![/bold cyan]")
            # os._exit(0) kills the process immediately, ignoring stuck threads.
            os._exit(0)

    return result

# This function takes a list of authors and formats it into a single string.
# If the list is empty, it keeps it as "Unknown".
def format_author(list):
    author = ""
    for auth in list:
        author = author + auth
    if author.strip() == "":
        author = "Unknown"

    return author