#!/usr/bin/env python3
"""
Google Scholar Search Script

This script searches Google Scholar and extracts paper metadata.

Usage:
    python google_scholar_search.py --query "machine learning" --max-results 10
"""

import argparse
import json
import os
from scholarly import scholarly

def search_google_scholar(query, max_results=10):
    """
    Search Google Scholar for papers matching the query.
    """
    results = []
    
    try:
        # Search Google Scholar
        search_query = scholarly.search_pubs(query)
        
        for i, paper in enumerate(search_query):
            if i >= max_results:
                break
            
            result = {
                'title': paper.get('bib', {}).get('title', ''),
                'authors': ', '.join(paper.get('bib', {}).get('author', [])),
                'year': paper.get('bib', {}).get('year', ''),
                'venue': paper.get('bib', {}).get('venue', ''),
                'citations': paper.get('num_citations', 0),
                'url': paper.get('pub_url', ''),
                'pdf_url': paper.get('eprint_url', ''),  # Open access PDF if available
                'abstract': paper.get('bib', {}).get('abstract', ''),
            }
            results.append(result)
            
    except Exception as e:
        print(f"Error searching Google Scholar: {e}")
        print("Note: Google Scholar may trigger CAPTCHA if too many requests are made")
        print("Consider adding delays or using proxies if this error persists")
    
    return results

def download_pdf(pdf_url, output_dir, title):
    """
    Download PDF from URL.
    """
    if not pdf_url:
        return None
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    try:
        import requests
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
        
        response = requests.get(pdf_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Sanitize filename
        safe_title = "".join(c for c in title if c.isalnum() or c in ' -_').strip()
        safe_title = safe_title[:100]  # Limit length
        
        filename = os.path.join(output_dir, f"{safe_title}.pdf")
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        return filename
            
    except Exception as e:
        print(f"Error downloading PDF from {pdf_url}: {e}")
    
    return None

def main():
    parser = argparse.ArgumentParser(description='Search Google Scholar')
    parser.add_argument('--query', required=True, help='Search query')
    parser.add_argument('--max-results', type=int, default=10, help='Maximum number of results')
    parser.add_argument('--output-dir', default='./downloads', help='Directory to save downloads')
    
    args = parser.parse_args()
    
    print(f"Searching Google Scholar for: {args.query}")
    
    results = search_google_scholar(args.query, args.max_results)
    
    # Download PDFs if available
    for result in results:
        if result['pdf_url']:
            print(f"Downloading PDF for: {result['title'][:50]}...")
            pdf_path = download_pdf(result['pdf_url'], args.output_dir, result['title'])
            if pdf_path:
                result['pdf_path'] = pdf_path
                print(f"  Saved to: {pdf_path}")
    
    # Save results to JSON
    output_file = os.path.join(args.output_dir, f"scholar_results_{hash(args.query) % 10000}.json")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\nSearch complete! Results saved to: {output_file}")
    print(f"Total results: {len(results)}")
    print(f"PDFs downloaded: {sum(1 for r in results if 'pdf_path' in r)}")
    
    return 0

if __name__ == '__main__':
    exit(main())
