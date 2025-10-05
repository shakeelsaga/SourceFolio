# SourceFolio

SourceFolio is a CLI tool that automates research by fetching information from multiple sources like **Wikipedia**, **OpenLibrary**, and **NewsAPI** based on user-provided keywords. It provides a seamless experience for collecting and exporting data into clean, readable formats.

##  Features

- **Interactive Session**: A guided, step-by-step process for users who prefer a prompted workflow.
- **Multiple Data Sources**: Gathers data from:
  - **Wikipedia**: Summary or full-page content.
  - **OpenLibrary**: Related books and authors.
  - **NewsAPI**: Recent news articles.
- **Smart API Key Handling**: Automatically prompts for and securely stores your NewsAPI key on the first run.
- **Data Preview**: Displays a summary of collected data directly in the terminal before export.
- **Multiple Export Formats**: Exports comprehensive reports to **PDF** and **CSV**.
- **Rich Terminal UI**: Uses modern, interactive prompts and progress bars for a better user experience.

##  Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/shakeelsaga/SourceFolio.git
    cd SourceFolio
    ```
2.  Install the package using pip:
    ```bash
    pip install .
    ```

This will install the `sourcefolio` command on your system.

## 🛠️ Configuration

SourceFolio requires a free API key from [newsapi.org](https://newsapi.org) to fetch news articles.

The first time you run the application, it will automatically guide you through a one-time setup:

1.  You will be prompted to enter your NewsAPI key.
2.  The application will validate the key to ensure it's working.
3.  Your key will be securely saved in a configuration file in your home directory (`~/.sourcefolio/config.json`) for all future sessions.

On subsequent runs, the application will confirm your saved key and give you the option to continue using it, change it, or remove it.

##  Usage

Once installed, you can run the tool directly from your terminal.

To start the guided, interactive session, simply run:

```bash
sourcefolio
```

Follow the on-screen prompts to enter keywords, choose the level of detail, and export your research report.

##  Project Structure

```
.
├── fetchers/                # data fetching fucntions
├── processing/              # supporting functions
├── tests/                   # Test files
├── main.py                  # Main function
├── pyproject.toml           # Project metadata and dependencies
├── README.md
└── setup.py                 # Setuptools configuration
```

##  Tech Stack 
- Python 3 
- wikipedia (for Wikipedia content) 
- OpenLibrary API 
- NewsAPI 
- ReportLab (for PDF generation)

##  Project Roadmap

 This is the first working version. Planned enhancements include:
 - Improved CLI interface with Rich/InquirerPy. 
 - Real-time progress bars during data fetching. 
 - More polished PDF exports (with TOC, watermark, styling). 
 - Additional export formats (CSV). 
 - Packaging for distribution (pip install sourcefolio).


##  Acknowledgements

- [Wikipedia](https://www.wikipedia.org/)
- [OpenLibrary](https://openlibrary.org/)
- [NewsAPI](https://newsapi.org/)
- [Rich](https://github.com/Textualize/rich), [InquirerPy](https://github.com/kazhala/InquirerPy), and [ReportLab](https://www.reportlab.com/)