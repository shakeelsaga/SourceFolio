import csv
import processing.utils as util
from rich.console import Console

console = Console()


def export_to_csv(data, filename="research_output.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Keyword",
                "Source",
                "Title/Name",
                "Author/Publisher",
                "Description",
                "Link",
                "Published At",
            ]
        )
        for keyword, content in data.items():
            # Wikipedia
            if "wiki" in content:
                writer.writerow(
                    [
                        keyword,
                        "Wikipedia",
                        content["wiki"]["data"].get("title", ""),
                        "",
                        content["wiki"]["data"].get("content", ""),
                        content["wiki"]["data"].get("url", ""),
                        "",
                    ]
                )
            # Books
            for olib in content.get("olib", []):
                writer.writerow(
                    [
                        keyword,
                        "Book",
                        olib.get("title", ""),
                        util.format_author(olib.get("author", "")),
                        "",
                        olib.get("link", ""),
                        olib.get("first_publish_year", ""),
                    ]
                )
            # News
            for news in content.get("news", []):
                writer.writerow(
                    [
                        keyword,
                        "News",
                        news.get("title", ""),
                        news.get("source", ""),
                        news.get("description", ""),
                        news.get("url", ""),
                        news.get("publishedAt", ""),
                    ]
                )
    console.print(f"[bold green]CSV exported successfully to {filename}[/bold green]")
