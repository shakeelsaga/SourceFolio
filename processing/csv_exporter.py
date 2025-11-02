# This script is all about exporting the research data into a CSV file.
# It takes the collected data and organizes it into a structured CSV format.

import csv
import processing.utils as util
from rich.console import Console

console = Console()

# This is the main function that takes the data and exports it to a CSV file.
def export_to_csv(data, filename="research_output.csv"):
    # I'm opening the CSV file in write mode.
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # I'm writing the header row of the CSV file.
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
        # I'm looping through the data for each keyword.
        for keyword, content in data.items():
            # First, I'm writing the Wikipedia data.
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
            # Next, I'm writing the book data from OpenLibrary.
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
            # Finally, I'm writing the news data.
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
    # I'm printing a success message to the console.
    console.print(f"[green]CSV exported successfully to {filename}[/green]\n")
