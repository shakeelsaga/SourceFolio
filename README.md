# SourceFolio (v1)

SourceFolio is an automated research data collector that fetches information from multiple sources like **Wikipedia**, **OpenLibrary**, and **NewsAPI** based on user-provided keywords. This is the **initial version (v1)** of the project.

## 📌 Features (v1)
- Accepts multiple keywords for research (comma-separated).
- Fetches:
  - **Wikipedia**: Summary or full details (user choice).
  - **OpenLibrary**: Books and authors related to the keyword.
  - **NewsAPI**: Latest news articles related to the keyword.
- Displays a **data preview** in the terminal.
- Exports results into a **PDF** file with structured formatting.

## 🚀 Usage
Run the script from the project root:

```bash
python src/main.py
```

Follow the prompts to enter keywords, choose data mode, and view/export results.

## 📂 Project Structure
```
src/
├── fetchers/
│   ├── wikipedia_function.py
│   ├── openlibrary_api.py
│   └── news_api.py
├── processing/
│   ├── keyword_data_structure.txt
│   ├── pdf_exporter.py
│   ├── ui.py
│   └── utils.py
├── tests/
│   └── test_log.md
└── main.py
```

## 🛠️ Tech Stack
- **Python 3**
- [wikipedia](https://pypi.org/project/wikipedia/) (for Wikipedia content)
- [OpenLibrary API](https://openlibrary.org/developers/api)
- [NewsAPI](https://newsapi.org/)
- [ReportLab](https://pypi.org/project/reportlab/) (for PDF generation)

## 📈 Project Roadmap
This is the first working version. Planned enhancements include:
- Improved CLI interface with Rich/InquirerPy.
- Real-time progress bars during data fetching.
- More polished PDF exports (with TOC, watermark, styling).
- Additional export formats (CSV).
- Packaging for distribution (`pip install sourcefolio`).

## 🙌 Acknowledgements
- [Wikipedia](https://www.wikipedia.org/)
- [OpenLibrary](https://openlibrary.org/)
- [NewsAPI](https://newsapi.org/)
- [ReportLab](https://www.reportlab.com/)
