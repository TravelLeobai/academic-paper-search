#!/usr/bin/env python3
"""
z-lib.fm Book Search Script

This script searches z-lib.fm for books and downloads them when available.

Usage:
    python zlib_search.py --query "deep learning" --max-results 10
"""

import argparse
import json
import os
import requests
from bs4 import BeautifulSoup
import time

def search_zlib(query, max_results=10):
    """
    Search z-lib.fm for books matching the query.
    
    Note: z-lib.fm may be blocked in some regions. Use VPN if needed.
    """
    results = []
    
    # z-lib.fm search URL (adjust based on actual site structure)
    search_url = "https://z-lib.fm/search"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    params = {
        'q': query,
        'page': 1,
    }
    
    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Parse search results (adjust selectors based on actual z-lib.fm page structure)
        result_items = soup.select('.book-item, .search-result-item')[:max_results]
        
        for item in result_items:
            title_elem = item.select_one('.title, h3')
            authors_elem = item.select_one('.authors, .author')
            year_elem = item.select_one('.year, .publication-year')
            download_link_elem = item.select_one('a[href*="download"], a[href*=".pdf"]')
            
            result = {
                'title': title_elem.get_text(strip=True) if title_elem else '',
                'authors': authors_elem.get_text(strip=True) if authors_elem else '',
                'year': year_elem.get_text(strip=True) if year_elem else '',
                'download_url': '',
                'format': '',  # PDF, EPUB, etc.
            }
            
            # Extract download link
            if download_link_elem and 'href' in download_link_elem.attrs:
                download_url = download_link_elem['href']
                if not download_url.startswith('http'):
                    download_url = 'https://z-lib.fm' + download_url
                result['download_url'] = download_url
                
                # Detect format from URL or file extension
                if '.pdf' in download_url.lower():
                    result['format'] = 'PDF'
                elif '.epub' in download_url.lower():
                    result['format'] = 'EPUB'
            
            results.append(result)
            
    except Exception as e:
        print(f"Error searching z-lib.fm: {e}")
        print("Note: z-lib.fm may be blocked in some regions. Use VPN if needed.")
    
    return results

def download_book(download_url, output_dir, title, format='PDF'):
    """
    Download book from z-lib.fm.
    """
    if not download_url:
        return None
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        response = requests.get(download_url, headers=headers, timeout=60)
        response.raise_for_status()
        
        # Sanitize filename
        safe_title = "".join(c for c in title if c.isalnum() or c in ' -_').strip()
        safe_title = safe_title[:100]  # Limit length
        
        filename = os.path.join(output_dir, f"{safe_title}.{format.lower()}")
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        return filename
            
    except Exception as e:
        print(f"Error downloading book from {download_url}: {e}")
    
    return None

def main():
    parser = argparse.ArgumentParser(description='Search z-lib.fm for books')
    parser.add_argument('--query', required=True, help='Search query')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum number of results')
    parser.add_argument('--output-dir', default='./downloads', help='Directory to save downloads')
    
    args = parser.parse_args()
    
    print(f"Searching z-lib.fm for: {args.query}")
    print("Note: z-lib.fm may be blocked in some regions. Use VPN if needed.")
    
    results = search_zlib(args.query, args.max_results)
    
    # Download books for each result
    for result in results:
        if result['download_url']:
            print(f"Downloading: {result['title'][:50]}...")
            book_path = download_book(
                result['download_url'],
                args.output_dir,
                result['title'],
                result['format'] or 'PDF'
            )
            if book_path:
                result['file_path'] = book_path
                print(f"  Saved to: {book_path}")
    
    # Save results to JSON
    output_file = os.path.join(args.output_dir, f"zlib_results_{hash(args.query) % 10000}.json")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nSearch complete! Results saved to: {output_file}")
    print(f"Total results: {len(results)}")
    print(f"Books downloaded: {sum(1 for r in results if 'file_path' in r)}")
    
    return 0

if __name__ == '__main__':
    exit(main())
