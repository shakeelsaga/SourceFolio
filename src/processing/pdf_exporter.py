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


class ReportDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, **kw)
        frame = Frame(
            cm, cm, self.pagesize[0] - 2 * cm, self.pagesize[1] - 2 * cm, id="normal"
        )
        self.addPageTemplates([PageTemplate("Normal", frame, onPage=self._add_footer)])
        self.styles = getSampleStyleSheet()
        self.current_keyword = None

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph):
            text = flowable.getPlainText()
            style_name = flowable.style.name
            if style_name == "Heading1":
                self.notify("TOCEntry", (0, text, self.page))
            elif style_name == "Heading2":
                self.notify("TOCEntry", (1, text, self.page))

    def _add_footer(self, canvas, doc):
        canvas.saveState()
        footer_text = "Powered by sourcefolio"
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(self.pagesize[0] - cm, cm / 2, footer_text)
        canvas.restoreState()


def export_to_pdf(data, filename="research_output.pdf"):
    doc = ReportDocTemplate(filename, pagesize=A4)
    styles = doc.styles
    h1 = styles["Heading1"]
    h2 = styles["Heading2"]
    normal = styles["Normal"]

    story = []

    # Table of Contents
    toc = TableOfContents()
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

    # Content for each keyword
    for i, (key, sections) in enumerate(data.items(), start=1):
        doc.current_keyword = key
        story.append(Paragraph(f"{i}. {key}", h1))
        story.append(Spacer(1, 6))

        # Summary / Details
        story.append(
            Paragraph(
                f"Full Details" if sections["wiki"]["is_detailed"] else "Summary", h2
            )
        )
        if sections["wiki"]["data"]:
            wiki = sections["wiki"]["data"]
            # story.append(Paragraph(f"<b>Title:</b> {wiki.get('title','N/A')}", normal))
            content = wiki.get("content", "N/A")
            if content and isinstance(content, str):
                for para in content.split("\n\n"):
                    para = para.strip().replace("\n", "<br/>")
                    if para:
                        story.append(Paragraph(para, normal))
                        story.append(Spacer(1, 6))
            else:
                story.append(Paragraph("N/A", normal))
            url = wiki.get("url", "N/A")
            story.append(
                Paragraph(
                    f'\n<b>Page Link:</b> <link href="{url}">{url}</link>', normal
                )
            )
        else:
            story.append(Paragraph("No Wikipedia data available.", normal))
        story.append(Spacer(1, 12))

        # Books
        # Books
        story.append(Paragraph("Books to Refer", h2))
        if sections["olib"]:
            books_list = []
            for b in sections["olib"][:5]:
                # Choose the best available link for the book
                book_link = b.get("edition_link") or b.get("link", "")
                book_text = f"<b>{b.get('title')}</b> by {utils.format_author(b.get('author'))} ({b.get('first_publish_year')})"

                # If a link exists, wrap the text in a hyperlink tag
                if book_link:
                    book_text = f'<link href="{book_link}">{book_text}</link>'

                books_list.append(ListItem(Paragraph(book_text, normal)))

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

        # News
        # News
        story.append(Paragraph("Recent News", h2))
        if sections["news"]:
            news_list = []
            for a in sections["news"][:5]:
                headline = a.get("title", "N/A")
                source = a.get("source", "Unknown")
                desc = a.get("description", "")
                news_url = a.get("url", "")

                text = f"<b>{headline}</b> ({source})"
                if desc:
                    text += f" - {desc}"

                # If a URL exists, wrap the text in a hyperlink tag
                if news_url:
                    text = f'<link href="{news_url}">{text}</link>'

                news_list.append(ListItem(Paragraph(text, normal)))
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

    doc.multiBuild(story)
    console.print(f"[bold green]✅ PDF exported successfully:[/bold green] {filename}")
