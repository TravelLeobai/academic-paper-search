#!/usr/bin/env python3
"""
PDF Summarization Script

This script extracts text from PDF and generates a summary.

Usage:
    python summarize_pdf.py --file "paper.pdf" --max-length 500
"""

import argparse
import os
import re
from PyPDF2 import PdfReader

def extract_text_from_pdf(pdf_path):
    """
    Extract text from PDF file.
    """
    text = ""
    
    try:
        reader = PdfReader(pdf_path)
        
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None
    
    return text

def summarize_text(text, max_length=500):
    """
    Generate a simple summary of the text.
    
    This is a basic implementation. For better summaries, consider:
    - Using NLP libraries (e.g., transformers, sumy)
    - Calling external APIs (e.g., OpenAI, Claude)
    - Using the existing pdf skill in QClaw
    """
    # Simple extractive summarization
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Take first N sentences as summary (simple approach)
    summary_sentences = sentences[:min(10, len(sentences))]
    summary = ' '.join(summary_sentences)
    
    # Truncate to max_length words
    words = summary.split()
    if len(words) > max_length:
        summary = ' '.join(words[:max_length]) + '...'
    
    return summary

def extract_key_sections(text):
    """
    Extract key sections from academic paper (abstract, introduction, conclusion).
    """
    sections = {
        'abstract': '',
        'introduction': '',
        'methods': '',
        'results': '',
        'conclusion': '',
    }
    
    # Simple pattern matching for section headers
    patterns = {
        'abstract': r'(?i)abstract[:\s]*(.*?)(?=\n\s*(?:introduction|keywords|1\.))',
        'introduction': r'(?i)introduction[:\s]*(.*?)(?=\n\s*(?:methods|methodology|2\.))',
        'methods': r'(?i)(?:methods|methodology)[:\s]*(.*?)(?=\n\s*(?:results|findings|3\.))',
        'results': r'(?i)(?:results|findings)[:\s]*(.*?)(?=\n\s*(?:discussion|conclusion|4\.))',
        'conclusion': r'(?i)(?:conclusion|conclusions)[:\s]*(.*?)(?=\n\s*(?:references|acknowledgments|$))',
    }
    
    for section, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            sections[section] = match.group(1).strip()[:500]  # Limit section length
    
    return sections

def main():
    parser = argparse.ArgumentParser(description='Summarize PDF content')
    parser.add_argument('--file', required=True, help='Path to PDF file')
    parser.add_argument('--max-length', type=int, default=500, help='Maximum summary length in words')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        return 1
    
    print(f"Extracting text from: {args.file}")
    text = extract_text_from_pdf(args.file)
    
    if not text:
        print("Failed to extract text from PDF")
        return 1
    
    print(f"\nExtracted {len(text)} characters")
    
    # Extract key sections
    print("\n" + "="*60)
    print("KEY SECTIONS")
    print("="*60)
    
    sections = extract_key_sections(text)
    for section, content in sections.items():
        if content:
            print(f"\n{section.upper()}:")
            print(content[:300] + ('...' if len(content) > 300 else ''))
    
    # Generate summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    summary = summarize_text(text, args.max_length)
    print(summary)
    
    # Save summary to file
    output_file = args.file.replace('.pdf', '_summary.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Summary of: {args.file}\n\n")
        f.write("="*60 + "\n")
        f.write("KEY SECTIONS\n")
        f.write("="*60 + "\n\n")
        
        for section, content in sections.items():
            if content:
                f.write(f"{section.upper()}:\n")
                f.write(content + "\n\n")
        
        f.write("="*60 + "\n")
        f.write("SUMMARY\n")
        f.write("="*60 + "\n\n")
        f.write(summary)
    
    print(f"\nSummary saved to: {output_file}")
    
    return 0

if __name__ == '__main__':
    exit(main())
