#!/usr/bin/env python3
"""
CNKI (知网) Paper Search and Download Script

This script searches CNKI database and downloads papers when available.
Requires IP-based authentication (campus network or VPN like 飞连).

Usage:
    python cnki_search.py --query "关键词" --max-results 10 --output-dir ./downloads
"""

import argparse
import json
import os
import requests
from bs4 import BeautifulSoup
import time

def search_cnki(query, max_results=10):
    """
    Search CNKI for papers matching the query.
    
    Note: This requires IP-based authentication (campus network or VPN).
    CNKI's search API may change; this is a basic implementation.
    """
    results = []
    
    # CNKI search URL (this is a simplified version; actual CNKI API may differ)
    search_url = "https://search.cnki.net/Search/Result"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    }
    
    params = {
        'content': query,
        'searchType': 'all',
    }
    
    try:
        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Parse search results (this needs to be adjusted based on actual CNKI page structure)
        result_items = soup.select('.result-item')[:max_results]
        
        for item in result_items:
            title_elem = item.select_one('.title')
            authors_elem = item.select_one('.authors')
            abstract_elem = item.select_one('.abstract')
            link_elem = item.select_one('a')
            
            result = {
                'title': title_elem.get_text(strip=True) if title_elem else '',
                'authors': authors_elem.get_text(strip=True) if authors_elem else '',
                'abstract': abstract_elem.get_text(strip=True) if abstract_elem else '',
                'link': link_elem['href'] if link_elem and 'href' in link_elem.attrs else '',
                'pdf_url': '',  # Will be populated if PDF is available
            }
            results.append(result)
            
    except Exception as e:
        print(f"Error searching CNKI: {e}")
        print("Note: Make sure you're connected to campus network or VPN (飞连) for CNKI access")
    
    return results

def download_pdf(paper_url, output_dir):
    """
    Download PDF from CNKI paper page.
    Requires IP-based authentication.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        # First, visit the paper page to get PDF download link
        response = requests.get(paper_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find PDF download link (adjust selector based on actual CNKI page)
        pdf_link = soup.select_one('a[href*=".pdf"]')
        
        if pdf_link and 'href' in pdf_link.attrs:
            pdf_url = pdf_link['href']
            if not pdf_url.startswith('http'):
                pdf_url = 'https://cnki.net' + pdf_url
            
            # Download PDF
            pdf_response = requests.get(pdf_url, headers=headers, timeout=30)
            pdf_response.raise_for_status()
            
            # Save PDF
            filename = os.path.join(output_dir, f"paper_{int(time.time())}.pdf")
            with open(filename, 'wb') as f:
                f.write(pdf_response.content)
            
            return filename
            
    except Exception as e:
        print(f"Error downloading PDF from {paper_url}: {e}")
    
    return None

def main():
    parser = argparse.ArgumentParser(description='Search CNKI and download papers')
    parser.add_argument('--query', required=True, help='Search query')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum number of results')
    parser.add_argument('--output-dir', default='./downloads', help='Directory to save downloads')
    
    args = parser.parse_args()
    
    print(f"Searching CNKI for: {args.query}")
    print("Note: Make sure you're connected to campus network or VPN (飞连)")
    
    results = search_cnki(args.query, args.max_results)
    
    # Download PDFs for each result
    for i, result in enumerate(results):
        if result['link']:
            print(f"Downloading PDF for: {result['title'][:50]}...")
            pdf_path = download_pdf(result['link'], args.output_dir)
            if pdf_path:
                result['pdf_path'] = pdf_path
                print(f"  Saved to: {pdf_path}")
    
    # Save results to JSON
    output_file = os.path.join(args.output_dir, f"cnki_results_{int(time.time())}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nSearch complete! Results saved to: {output_file}")
    print(f"Total results: {len(results)}")
    
    return 0

if __name__ == '__main__':
    exit(main())
