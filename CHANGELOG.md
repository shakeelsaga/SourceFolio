# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added
- (Empty for now)

### Changed
- (Empty for now)

### Fixed
- (Empty for now)

## [1.0.10] - 2025-12-12

### Fixed
- **Critical (Stability):** Resolved an issue where the application would hang and fail to close completely if the user tried to exit (or pressed `Ctrl+C`) during a network delay.
- **Stability:** Enforced a strict timeout on all data fetchers. The application now correctly detects when a server is unresponsive and prompts to retry, rather than the progress bar loading indefinitely.

## [1.0.9] - 2025-12-12

### Changed
- **UX Improvement:** Connection failure messages are now cleaner and user-friendly, replacing raw error tracebacks with clear status notifications.

### Fixed
- **Stability:** Implemented robust retry and exit mechanisms for all network operations (Wikipedia, OpenLibrary, NewsAPI). If the internet connection is lost, the application now pauses and allows the user to retry the connection instead of crashing.

## [1.0.8] - 2025-12-12

### Fixed
- **Critical (Stability):** Fixed a fatal crash where network errors were being re-raised instead of handled gracefully. The application now reports "failed" on the progress bar and continues running.
- **Improved:** `NewsAPI` validation now distinguishes between "Invalid Key" and "Network Error," preventing false negatives when the user is offline.

## [1.0.7] - 2025-11-05

### Added
- Added a comprehensive troubleshooting guide to `README.md` for all Windows `PATH` errors (e.g., `pip`, `python`, and `sourcefolio` not recognized).
- Added a troubleshooting guide to the `README.md` for the Linux `PATH` issue (`sourcefolio: command not found`).

## [1.0.6] - 2025-11-04

### Added
- Added a professional banner to the `README.md` file.
- Added the project's official logo to the PyPI page.

## [1.0.5] - 2025-11-04

This is the first stable public release. It includes numerous bug fixes and stability improvements found during testing.

### Added
- Added clickable links to the Wikipedia titles in the terminal data preview.
- Added an official `LICENSE` file.

### Changed
- Polished the welcome splash screen with clearer instructions and universal links.
- Updated the `README.md` file with better installation instructions and troubleshooting.
- Standardized the success messages for PDF and CSV exports.

### Fixed
- **Critical (Packaging):** Fixed a `ModuleNotFoundError` by removing the legacy `setup.py` and consolidating all package configuration into `pyproject.toml`. This ensures `fetchers` and `processing` are installed correctly.
- **Critical (PDF Export):** Fixed a `KeyError` that would cause the application to crash if the PDF exporter tried to create a report for a keyword that had no Wikipedia data.
- **Critical (Linux/Python 3.8):** Fixed a `TypeError` that occurred on older Python versions (like 3.8) due to incompatible type hinting in `processing/ui.py`.
- Fixed a minor text casing issue in the PDF footer.