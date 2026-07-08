#!/usr/bin/env python3
"""
Validate all cross-references in markdown files to ensure they are still valid.
"""

import re
import json
import os
from pathlib import Path
from urllib.parse import urlparse


def extract_markdown_links(file_path):
    """Extract all markdown links from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all markdown links [text](url)
    links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
    return links


def validate_link(link_text, url):
    """Validate a single markdown link."""
    issues = []
    
    # Check if URL is valid
    try:
        parsed = urlparse(url)
        if not parsed.scheme and not parsed.path.startswith('/'):
            # Relative link - check if file exists
            if not os.path.exists(url):
                issues.append(f"Relative path does not exist: {url}")
        elif parsed.scheme not in ['http', 'https']:
            issues.append(f"Invalid URL scheme: {parsed.scheme}")
        elif 'github.com' in url:
            # GitHub link - we can't validate without API, but check format
            if '/blob/' not in url and '/tree/' not in url:
                issues.append(f"GitHub link should use /blob/ or /tree/: {url}")
    except Exception as e:
        issues.append(f"Error parsing URL: {e}")
    
    # Check link text length
    if len(link_text) > 200:
        issues.append(f"Link text too long ({len(link_text)} chars)")
    
    return issues


def validate_file(file_path):
    """Validate all links in a file."""
    links = extract_markdown_links(file_path)
    issues = []
    
    for link_text, url in links:
        link_issues = validate_link(link_text, url)
        if link_issues:
            issues.append({
                'file': str(file_path),
                'link_text': link_text,
                'url': url,
                'issues': link_issues
            })
    
    return issues


def validate_repository(repo_path):
    """Validate all markdown files in a repository."""
    repo_path = Path(repo_path)
    all_issues = []
    
    # Find all markdown files
    md_files = list(repo_path.rglob('*.md'))
    
    for md_file in md_files:
        file_issues = validate_file(md_file)
        all_issues.extend(file_issues)
    
    return all_issues


def main():
    """Main validation function."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python validate_links.py <repository_path>")
        return
    
    repo_path = sys.argv[1]
    issues = validate_repository(repo_path)
    
    if issues:
        print(f"Found {len(issues)} link validation issues:")
        for issue in issues:
            print(f"\nFile: {issue['file']}")
            print(f"  Link: [{issue['link_text']}]({issue['url']})")
            for problem in issue['issues']:
                print(f"    - {problem}")
        sys.exit(1)
    else:
        print("All links validated successfully!")
        sys.exit(0)


if __name__ == '__main__':
    main()
