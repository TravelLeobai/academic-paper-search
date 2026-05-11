#!/usr/bin/env python3
"""
Download and Summarize Script

Combined script: downloads paper/book from URL and generates summary.

Usage:
    python download_and_summarize.py --url "https://..." --source cnki
"""

import argparse
import os
import sys
import subprocess

def download_from_cnki(url, output_dir):
    """Download paper from CNKI."""
    # Reuse logic from cnki_search.py
    import requests
    from bs4 import BeautifulSoup
    import time
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        # Visit paper page to get PDF link
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find PDF download link
        pdf_link = soup.select_one('a[href*=".pdf"]')
        
        if pdf_link and 'href' in pdf_link.attrs:
            pdf_url = pdf_link['href']
            if not pdf_url.startswith('http'):
                pdf_url = 'https://cnki.net' + pdf_url
            
            # Download PDF
            pdf_response = requests.get(pdf_url, headers=headers, timeout=30)
            pdf_response.raise_for_status()
            
            filename = os.path.join(output_dir, f"cnki_paper_{int(time.time())}.pdf")
            with open(filename, 'wb') as f:
                f.write(pdf_response.content)
            
            return filename
            
    except Exception as e:
        print(f"Error downloading from CNKI: {e}")
    
    return None

def download_from_scholar(url, output_dir, title='scholar_paper'):
    """Download paper from Google Scholar."""
    if not url:
        return None
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        import requests
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Sanitize filename
        safe_title = "".join(c for c in title if c.isalnum() or c in ' -_').strip()
        safe_title = safe_title[:100]
        
        filename = os.path.join(output_dir, f"{safe_title}.pdf")
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        return filename
            
    except Exception as e:
        print(f"Error downloading from Google Scholar: {e}")
    
    return None

def download_from_zlib(url, output_dir, title='book', format='PDF'):
    """Download book from z-lib.fm."""
    if not url:
        return None
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        import requests
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        response = requests.get(url, headers=headers, timeout=60)
        response.raise_for_status()
        
        # Sanitize filename
        safe_title = "".join(c for c in title if c.isalnum() or c in ' -_').strip()
        safe_title = safe_title[:100]
        
        filename = os.path.join(output_dir, f"{safe_title}.{format.lower()}")
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        return filename
            
    except Exception as e:
        print(f"Error downloading from z-lib.fm: {e}")
    
    return None

def summarize_pdf(pdf_path):
    """Summarize PDF using summarize_pdf.py script."""
    try:
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        summarize_script = os.path.join(script_dir, 'summarize_pdf.py')
        
        # Run summarize_pdf.py
        result = subprocess.run(
            ['python', summarize_script, '--file', pdf_path],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        return result.stdout
        
    except Exception as e:
        print(f"Error summarizing PDF: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Download and summarize paper/book')
    parser.add_argument('--url', required=True, help='Paper/book URL')
    parser.add_argument('--source', required=True, choices=['cnki', 'scholar', 'zlib'], help='Source platform')
    parser.add_argument('--output-dir', default='./downloads', help='Directory to save files')
    parser.add_argument('--title', default='paper', help='Title for filename (optional)')
    
    args = parser.parse_args()
    
    print(f"Downloading from {args.source}: {args.url}")
    
    # Download based on source
    downloaded_file = None
    
    if args.source == 'cnki':
        downloaded_file = download_from_cnki(args.url, args.output_dir)
    elif args.source == 'scholar':
        downloaded_file = download_from_scholar(args.url, args.output_dir, args.title)
    elif args.source == 'zlib':
        downloaded_file = download_from_zlib(args.url, args.output_dir, args.title)
    
    if not downloaded_file:
        print("Download failed!")
        return 1
    
    print(f"\nDownloaded to: {downloaded_file}")
    
    # Summarize if it's a PDF
    if downloaded_file.lower().endswith('.pdf'):
        print("\nGenerating summary...")
        summary = summarize_pdf(downloaded_file)
        
        if summary:
            print("\n" + "="*60)
            print("SUMMARY")
            print("="*60)
            print(summary)
            
            # Save summary to file
            summary_file = downloaded_file.replace('.pdf', '_summary.txt')
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            print(f"\nSummary saved to: {summary_file}")
    
    return 0

if __name__ == '__main__':
    exit(main())
