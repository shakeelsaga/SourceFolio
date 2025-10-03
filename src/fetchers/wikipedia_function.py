from rich.console import Console
from rich.table import Table

console = Console()
import re
import wikipedia


def clean_keyword(keyword):
    return re.sub(
        r"[^a-zA-Z0-9\s\(\)\+\-]", "", keyword
    ).strip()  # remove unwanted characters in the keywords


# fetching wiki data
def get_wiki_data(term, is_detailed=False, lang="en"):
    term = clean_keyword(term)
    wikipedia.set_lang(lang)
    try:
        if is_detailed:
            page = wikipedia.page(term, auto_suggest=False)
            return {"title": page.title, "content": page.content, "url": page.url}
        else:
            page = wikipedia.page(term, auto_suggest=False)
            summary = wikipedia.summary(term, auto_suggest=False)
            return {"title": page.title, "content": summary, "url": page.url}

    except wikipedia.exceptions.DisambiguationError as e:
        console.print(f"[bold yellow]DisambiguationError:[/bold yellow] The term '{term}' may refer to multiple pages.")
        table = Table(title="Possible Options")
        table.add_column("Options", style="cyan")
        for option in e.options[:10]:
            table.add_row(option)
        console.print(table)
        return None
    except wikipedia.exceptions.PageError:
        console.print(f"[bold red]PageError:[/bold red] The page for '{term}' does not exist.")
        return None
    except KeyError as e:
        console.print(f"[bold red]KeyError:[/bold red] Missing key {e} in Wikipedia response.")
        return None
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")
        return None


if __name__ == "__main__":
    keyword = "Halo (game)"
    data = get_wiki_data(keyword, False, lang="en")
    if data:
        table = Table(title="Wikipedia Result")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")
        for k, v in data.items():
            display_val = v if len(v) < 120 else v[:120] + "..."
            table.add_row(k, display_val)
        console.print(table)
    else:
        console.print("[bold red]No data retrieved.[/bold red]")
