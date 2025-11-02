# Hey there! This script is all about turning the research data into a neat PDF report.
# I'm using the reportlab library, which is a powerful tool for creating PDFs in Python.

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    PageBreak,
    ListFlowable,
    ListItem,
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from processing import utils
from rich.console import Console

console = Console()


# This is my custom document template. I'm inheriting from BaseDocTemplate
# to create a structure for my report with a consistent footer.
class ReportDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        # I'm setting up the main frame of my page here.
        # It's like defining the margins of my document.
        frame = Frame(
            cm, cm, self.pagesize[0] - 2 * cm, self.pagesize[1] - 2 * cm, id="normal"
        )
        # I'm adding a page template with my frame and a footer.
        self.addPageTemplates([PageTemplate("Normal", frame, onPage=self._add_footer)])
        self.styles = getSampleStyleSheet()
        self.current_keyword = None

    # This method is called for every flowable (like a paragraph) that's added to the document.
    # I'm using it to build my table of contents.
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            text = flowable.getPlainText()
            style_name = flowable.style.name
            # If it's a Heading1 or Heading2, I add it to the TOC.
            if style_name == "Heading1":
                self.notify("TOCEntry", (0, text, self.page))
            elif style_name == "Heading2":
                self.notify("TOCEntry", (1, text, self.page))

    # This method adds a footer to each page.
    def _add_footer(self, canvas, doc):
        canvas.saveState()
        footer_text = "Powered by SourceFolio"
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(self.pagesize[0] - cm, cm / 2, footer_text)
        canvas.restoreState()


# This is the main function that takes my data and spits out a PDF.
def export_to_pdf(data, filename="research_output.pdf"):
    # I'm creating an instance of my custom document template.
    doc = ReportDocTemplate(filename, pagesize=A4)
    styles = doc.styles
    h1 = styles["Heading1"]
    h2 = styles["Heading2"]
    normal = styles["Normal"]

    # The 'story' is a list of all the elements that will go into my PDF.
    story = []

    # I'll create a table of contents.
    toc = TableOfContents()
    # And here's how I style it.
    toc.levelStyles = [
        ParagraphStyle(
            name="TOCHeading1",
            fontName="Times-Bold",
            fontSize=14,
            leftIndent=20,
            firstLineIndent=-20,
            spaceBefore=5,
        ),
        ParagraphStyle(
            name="TOCHeading2",
            fontSize=12,
            leftIndent=40,
            firstLineIndent=-20,
            spaceBefore=0,
        ),
    ]
    toc_heading_style = ParagraphStyle(
        name="TOCMainHeading",
        fontSize=16,
        leading=20,
        alignment=0,
        fontName="Helvetica-Bold",
        spaceAfter=6,
    )
    story.append(Paragraph("Table of Contents", toc_heading_style))
    doc.notify("TOCEntry", (0, "Table of Contents", 1))
    from reportlab.platypus import HRFlowable

    # A horizontal line for some visual separation.
    line_width = doc.width
    story.append(
        HRFlowable(
            width="99%",
            thickness=1,
            color="black",
            hAlign="LEFT",
            spaceBefore=2,
            spaceAfter=10,
        )
    )
    story.append(toc)
    story.append(PageBreak())

    # Now, I loop through my data and add it to the story.
    for i, (key, sections) in enumerate(data.items(), start=1):
        doc.current_keyword = key
        # This is the main title for each section.
        # Use the wiki title if it exists, otherwise fall back to the keyword
        title = sections["wiki"]["data"].get("title", key)
        story.append(Paragraph(f"{i}. {title}", h1))
        story.append(Spacer(1, 6))

        # This is the subtitle for the Wikipedia section.
        story.append(
            Paragraph(
                f"Full Details" if sections["wiki"]["is_detailed"] else "Summary", h2
            )
        )
        # I'll add the Wikipedia content.
        if sections["wiki"]["data"]:
            wiki = sections["wiki"]["data"]
            content = wiki.get("content", "N/A")
            if content and isinstance(content, str):
                # I'm splitting the content into paragraphs and adding them to the story.
                for para in content.split("\n\n"):
                    para = para.strip().replace("\n", "<br/>")
                    if para:
                        story.append(Paragraph(para, normal))
                        story.append(Spacer(1, 6))
            else:
                story.append(Paragraph("N/A", normal))
            url = wiki.get("url", "N/A")
            # And a link to the Wikipedia page.
            story.append(
                Paragraph(
                    f'\n<b>Page Link:</b> <link href="{url}">{url}</link>', normal
                )
            )
        else:
            story.append(Paragraph("No Wikipedia data available.", normal))
        story.append(Spacer(1, 12))

        # Now for the books section.
        story.append(Paragraph("Books to Refer", h2))
        if sections["olib"]:
            books_list = []
            # I'm taking the top 5 books.
            for b in sections["olib"][:5]:
                book_link = b.get("edition_link") or b.get("link", "")
                book_text = f"<b>{b.get('title')}</b> by {utils.format_author(b.get('author'))} ({b.get('first_publish_year')})"

                # If there's a link, let's make the text clickable.
                if book_link:
                    book_text = f'<link href="{book_link}">{book_text}</link>'

                books_list.append(ListItem(Paragraph(book_text, normal)))

            # I'm creating a numbered list of books.
            story.append(
                ListFlowable(
                    books_list,
                    bulletType="1",
                    bulletFormat="%s.",
                    bulletFontSize=normal.fontSize,
                )
            )
        else:
            story.append(Paragraph("No books found.", normal))
        story.append(Spacer(1, 12))

        # And finally, the news section.
        story.append(Paragraph("Recent News", h2))
        if sections["news"]:
            news_list = []
            # I'm taking the top 5 news articles.
            for a in sections["news"][:5]:
                headline = a.get("title", "N/A")
                source = a.get("source", "Unknown")
                desc = a.get("description", "")
                news_url = a.get("url", "")

                text = f"<b>{headline}</b> ({source})"
                if desc:
                    text += f" - {desc}"

                # If there's a link, let's make the text clickable.
                if news_url:
                    text = f'<link href="{news_url}">{text}</link>'

                news_list.append(ListItem(Paragraph(text, normal)))
            # I'm creating a lettered list of news articles.
            story.append(
                ListFlowable(
                    news_list,
                    bulletType="a",
                    bulletFormat="%s.",
                    bulletFontSize=normal.fontSize,
                )
            )
        else:
            story.append(Paragraph("No news articles found.", normal))
        story.append(PageBreak())

    # This is where the magic happens. I'm building the PDF.
    doc.multiBuild(story)
    console.print(f"[green]PDF exported successfully to {filename}[/green]\n")
