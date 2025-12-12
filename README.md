<p align="center">
  <a href="https://github.com/shakeelsaga/SourceFolio">
    <img src="https://cdn.jsdelivr.net/gh/shakeelsaga/SourceFolio@main/.assets/SourceFolio-Banner.png" alt="SourceFolio Banner">
  </a>
</p>


# SourceFolio

[![PyPI Version](https://img.shields.io/pypi/v/sourcefolio.svg)](https://pypi.org/project/sourcefolio/)
[![Python Versions](https://img.shields.io/pypi/pyversions/sourcefolio.svg)](https://pypi.org/project/sourcefolio/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

SourceFolio is a CLI tool that automates research by fetching information from multiple sources like **Wikipedia**, **OpenLibrary**, and **NewsAPI** based on user-provided keywords. It provides a seamless experience for collecting and exporting data into clean, readable formats.

## Features

- **Interactive Session**: A guided, step-by-step process for users who prefer a prompted workflow.
- **Multiple Data Sources**: Gathers data from:
  - **Wikipedia**: Summary or full-page content.
  - **OpenLibrary**: Related books and authors.
  - **NewsAPI**: Recent news articles.
- **Smart API Key Handling**: Automatically prompts for and securely stores your NewsAPI key on the first run.
- **Data Preview**: Displays a summary of collected data directly in the terminal before export.
- **Multiple Export Formats**: Exports comprehensive reports to **PDF** (with clickable links) and **CSV**.
- **Rich Terminal UI**: Uses modern, interactive prompts and progress bars for a better user experience.

## Installation

SourceFolio is available on the Python Package Index (PyPI). You can install it directly using `pip`:

```bash
pip install sourcefolio
```

To upgrade to the latest version, run:

```bash
pip install --upgrade sourcefolio
```

## Configuration

SourceFolio requires a free API key from [newsapi.org](https://newsapi.org) to fetch news articles.

The first time you run the application, it will automatically guide you through a one-time setup:

1.  You will be prompted to enter your NewsAPI key.
2.  The application will validate the key to ensure it's working.
3.  Your key will be securely saved in a configuration file in your home directory (`~/.sourcefolio/config.json`) for all future sessions.

On subsequent runs, the application will confirm your saved key and give you the option to continue using it, change it, or remove it.

## Usage

Once installed, you can run the tool directly from your terminal.

To start the guided, interactive session, simply run:

```bash
sourcefolio
```

Follow the on-screen prompts to enter keywords, choose the level of detail, and export your research report.

**Tip:** You can exit the application at any point by pressing `Ctrl+C`.

## Troubleshooting

### ISSUE: Windows: `python`, `py`, `pip`, or `sourcefolio` is not recognized...

This is a very common issue on Windows, and all these errors point to the **same single problem**: your Python installation is not added to your system's `PATH`.

The fix is to manually find your Python installation and `Scripts` folders and add them to your Windows Environment Variables. This guide will fix all of those errors at once.

#### **Solution (The Manual Fix)**

**Step 1. Find Your Python Paths**

Since the `python` command doesn't work, we must find the path manually.

1.  Press the **Windows Key** to open the Start Menu.
2.  Type **`python`**.
3.  Right-click on the "Python" app (e.g., "Python 3.11") in the search results and select **"Open file location"**.
4.  This may open a folder with a *shortcut*. If it is a shortcut, right-click the shortcut and select **"Open file location"** *again*.
5.  You should now be in the main Python installation folder (you'll see `python.exe`). Click in the address bar at the top of the File Explorer to copy this path.

You now have the **two paths** you need:
* **Path 1 (Main Folder):** The path you just copied (e.g., `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311`)
* **Path 2 (Scripts Folder):** The exact same path, but with `\Scripts` added to the end (e.g., `C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\Scripts`)

**Step 2. Add Both Paths to Environment Variables**

1.  Press the **Windows Key**, type **`env`**, and select **"Edit the system environment variables"**.
2.  In the window that opens, click the **"Environment Variables..."** button.
3.  In the **top box** ("User variables..."), find the variable named **`Path`**. Click on it, then click **"Edit..."**.
4.  Click the **"New"** button and paste in **Path 1** (the main folder).
5.  Click **"New"** again and paste in **Path 2** (the `Scripts` folder).
6.  Click "OK" on all three windows to save and close everything.

**Step 3. Restart Your Terminal**

* This is the most important step. **Completely close and re-open** your PowerShell or CMD window.
* To confirm it worked, type `pip --version`. You should see the version number.
* You can now successfully run `pip install sourcefolio`.

---
**Still confused?**
[Here is a short YouTube video](https://www.youtube.com/watch?v=dj5oOPaeIqI) that walks you through this exact process.

### ISSUE: Linux (Ubuntu/Debian): `sourcefolio: command not found`

This is a common issue on many Linux distributions. When you install a package with `pip` as a user, it places the command in `~/.local/bin`. This folder is often not in your shell's `PATH` by default.

#### **Solution (The One-Liner Fix)**

You only need to run these two commands in your terminal.

**Step 1. Add the Path to Your Shell Configuration**

This command adds the user-level `bin` folder to your `PATH` permanently.

```bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
```
(Note: If you are using Zsh (like on modern macOS or some custom Linux setups) instead of Bash, you would use `~/.zshrc` instead of `~/.bashrc`)

#### Step 2. Refresh Your Terminal ####

This command applies the change immediately to your current session.

```bash
source ~/.bashrc
```
After this, the `sourcefolio` command will work.

## Project Structure

```
SourceFolio/
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
├── CHANGELOG.md             # Log of all version changes
├── LICENSE                  # MIT License file
├── main.py                  # Main application script
├── pyproject.toml           # Project metadata and dependencies
└── README.md                # This file
```

## Tech Stack

  - Python 3
  - [rich](https://github.com/Textualize/rich)
  - [InquirerPy](https://github.com/kazhala/InquirerPy)
  - [ReportLab](https://www.reportlab.com/)
  - [wikipedia](https://pypi.org/project/wikipedia/)
  - [requests](https://pypi.org/project/requests/)

## Project Roadmap

This is the first public version of SourceFolio. I am planning on continuing to include more features in the future. Some of the planned enhancements include:

  - **More Data Sources:** Integration with additional data sources such as academic journals and social media.
  - **Selective Data Output:** Users will be able to choose which data sources to include in the final output.
  - **Command-Line Flags:** The ability to use the tool directly from the command line with flags, bypassing the interactive mode.

## Contributing

SourceFolio is an open-source project, and contributions are always welcome\! Whether you're interested in fixing bugs, adding new features, or improving documentation, your help is appreciated.

If you'd like to contribute, please feel free to:

  - Fork the repository and submit a pull request.
  - Open an issue to report bugs or suggest improvements.

Every contribution, no matter how small, helps make this project better.

## Acknowledgements

  - [Wikipedia](https://www.wikipedia.org/)
  - [OpenLibrary](https://openlibrary.org/)
  - [NewsAPI](https://newsapi.org/)

