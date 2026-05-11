---
name: academic-paper-search
description: Multi-source academic paper and book search with automatic PDF download and content summarization. Use when the user requests searching for academic papers, journal articles, conference papers, or books from Chinese or international sources. Supports CNKI (知网) with IP-based authentication via campus network/VPN (飞连), Google Scholar, and z-lib.fm for books. Automatically downloads PDFs when available and provides content summaries.
---

# Academic Paper Search

## Overview

This skill enables searching across multiple academic sources (CNKI, Google Scholar, z-lib.fm), automatically downloading PDFs when available (using IP-based authentication for CNKI), and summarizing paper content for quick understanding.

## When to Use This Skill

Use this skill when the user asks to:
- Search for academic papers or journal articles
- Find books or book chapters
- Download papers from CNKI, Google Scholar, or z-lib.fm
- Summarize paper content or extract key findings
- Search Chinese academic databases (CNKI) with campus network access

## Quick Start

### Search CNKI (知网)

Use `scripts/cnki_search.py` to search CNKI database:

```bash
python scripts/cnki_search.py --query "机器学习" --max-results 10
```

**Requirements:**
- Must be connected to campus network or VPN (飞连) for IP-based authentication
- Downloads PDFs automatically when available

### Search Google Scholar

Use `scripts/google_scholar_search.py` to search Google Scholar:

```bash
python scripts/google_scholar_search.py --query "machine learning" --max-results 10
```

### Search z-lib.fm (Books)

Use `scripts/zlib_search.py` to search for books:

```bash
python scripts/zlib_search.py --query "deep learning" --max-results 10
```

### Download and Summarize PDF

After finding a paper, use `scripts/download_and_summarize.py` to download the PDF and generate a summary:

```bash
python scripts/download_and_summarize.py --url "https://cnki.net/..." --source cnki
```

## Detailed Workflows

### CNKI Search and Download Workflow

1. **Ensure network connection**: Verify you're connected to campus network or VPN (飞连)
2. **Search papers**: Run `python scripts/cnki_search.py --query "关键词"`
3. **Review results**: Script returns paper titles, authors, abstracts, and download links
4. **Download PDF**: Script automatically downloads PDFs using IP authentication
5. **Summarize**: Use `python scripts/summarize_pdf.py --file "paper.pdf"` to extract and summarize content

### Google Scholar Workflow

1. **Search papers**: Run `python scripts/google_scholar_search.py --query "keywords"`
2. **Review results**: Script returns paper titles, authors, years, citation counts, and PDF links
3. **Download PDF**: If PDF link is available, script downloads it
4. **Summarize**: Use PDF summary script to extract key findings

### z-lib.fm Book Search Workflow

1. **Search books**: Run `python scripts/zlib_search.py --query "book title"`
2. **Review results**: Script returns book titles, authors, editions, and download links
3. **Download book**: Script downloads the book file (PDF/EPUB)
4. **Summarize**: For PDF books, extract key chapters or sections

## Script Reference

### `scripts/cnki_search.py`

Searches CNKI database and downloads papers.

**Arguments:**
- `--query`: Search query (required)
- `--max-results`: Maximum number of results (default: 10)
- `--output-dir`: Directory to save downloads (default: ./downloads)

**Output:** JSON file with search results and downloaded PDF paths

### `scripts/google_scholar_search.py`

Searches Google Scholar and extracts paper metadata.

**Arguments:**
- `--query`: Search query (required)
- `--max-results`: Maximum number of results (default: 10)
- `--output-dir`: Directory to save downloads (default: ./downloads)

**Output:** JSON file with search results and available PDF links

### `scripts/zlib_search.py`

Searches z-lib.fm for books.

**Arguments:**
- `--query`: Search query (required)
- `--max-results`: Maximum number of results (default: 10)
- `--output-dir`: Directory to save downloads (default: ./downloads)

**Output:** JSON file with search results and download links

### `scripts/summarize_pdf.py`

Extracts text from PDF and generates a summary.

**Arguments:**
- `--file`: Path to PDF file (required)
- `--max-length`: Maximum summary length in words (default: 500)

**Output:** Summary text printed to stdout

### `scripts/download_and_summarize.py`

Combined script: downloads paper from URL and generates summary.

**Arguments:**
- `--url`: Paper URL or DOI (required)
- `--source`: Source platform (cnki|scholar|zlib) (required)
- `--output-dir`: Directory to save files (default: ./downloads)

**Output:** Downloaded file path and summary text

## Dependencies

These scripts require the following Python packages:

```bash
pip install requests beautifulsoup4 scholarly PyPDF2
```

For CNKI access, ensure:
- Campus network connection OR
- VPN connection (飞连) for IP-based authentication

## Notes

- CNKI requires IP-based authentication (campus network or VPN)
- Google Scholar may trigger CAPTCHA if too many requests are made
- z-lib.fm access may be blocked in some regions (use VPN if needed)
- PDF download availability depends on publisher/open access status

## Resources

### scripts/
Contains all executable Python scripts for searching, downloading, and summarizing.

### references/
(No additional reference files needed at this time)

### assets/
(No additional asset files needed at this time)
