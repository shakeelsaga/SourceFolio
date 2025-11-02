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

**Tip:** You can exit the application at any point by pressing `Ctrl+C`.

##  Project Structure

```
.
├── fetchers/                # Data fetching functions
│   ├── news_api.py
│   ├── openlibrary_api.py
│   └── wikipedia_function.py
├── processing/              # Supporting functions
│   ├── config.py
│   ├── csv_exporter.py
│   ├── pdf_exporter.py
│   ├── ui.py
│   └── utils.py
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

This is the first public version of SourceFolio. I am planning on continuing to include more features in the future. Some of the planned enhancements include:

- **More Data Sources:** Integration with additional data sources such as academic journals and social media.
- **Selective Data Output:** Users will be able to choose which data sources to include in the final output.
- **Command-Line Flags:** The ability to use the tool directly from the command line with flags, bypassing the interactive mode.


##  Contributing

SourceFolio is an open-source project, and contributions are always welcome! Whether you're interested in fixing bugs, adding new features, or improving documentation, your help is appreciated.

If you'd like to contribute, please feel free to:

-   Fork the repository and submit a pull request.
-   Open an issue to report bugs or suggest improvements.

Every contribution, no matter how small, helps make this project better.

##  Acknowledgements

- [Wikipedia](https://www.wikipedia.org/)
- [OpenLibrary](https://openlibrary.org/)
- [NewsAPI](https://newsapi.org/)
- [Rich](https://github.com/Textualize/rich), [InquirerPy](https://github.com/kazhala/InquirerPy), and [ReportLab](https://www.reportlab.com/)