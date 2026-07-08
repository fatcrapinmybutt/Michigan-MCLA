#!/usr/bin/env python3
"""
Convert catalogue markdown files to compressed JSON format for better performance.
This script processes all catalogue/*.md files and creates corresponding JSON versions.
"""

import json
import re
import os
import hashlib
from pathlib import Path
from datetime import datetime


def markdown_to_json(markdown_content, file_path):
    """Convert markdown content to structured JSON."""
    lines = markdown_content.split('\n')
    
    # Extract metadata
    metadata = {
        'source_file': os.path.basename(file_path),
        'conversion_date': datetime.utcnow().isoformat() + 'Z',
        'format_version': '1.0',
        'checksum': hashlib.sha256(markdown_content.encode()).hexdigest()
    }
    
    # Parse sections
    sections = []
    current_section = None
    current_subsection = None
    
    for line in lines:
        # Main section headers (## 1. Title)
        if line.startswith('## '):
            match = re.match(r'## (\d+)\. (.*)', line)
            if match:
                if current_section:
                    sections.append(current_section)
                current_section = {
                    'type': 'section',
                    'number': int(match.group(1)),
                    'title': match.group(2),
                    'content': [],
                    'subsections': []
                }
                current_subsection = None
            continue
        
        # Subsection headers (### 1.1 Title)
        if line.startswith('### '):
            match = re.match(r'### (\d+\.\d+)\.? (.*)', line)
            if match and current_section:
                if current_subsection:
                    current_section['subsections'].append(current_subsection)
                current_subsection = {
                    'type': 'subsection',
                    'number': match.group(1),
                    'title': match.group(2),
                    'content': []
                }
            continue
        
        # Content lines
        if line.strip():
            if current_subsection:
                current_subsection['content'].append(line)
            elif current_section:
                current_section['content'].append(line)
    
    # Add the last section
    if current_section:
        if current_subsection:
            current_section['subsections'].append(current_subsection)
        sections.append(current_section)
    
    return {
        'metadata': metadata,
        'sections': sections
    }


def compress_content(content):
    """Compress content by removing redundant whitespace and normalizing."""
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in content if line.strip()]
    return '\n'.join(lines)


def process_catalogue_files():
    """Process all catalogue markdown files and create JSON versions."""
    catalogue_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/catalogue')
    json_dir = catalogue_dir / 'json'
    
    # Create JSON directory
    json_dir.mkdir(exist_ok=True)
    
    # Process each markdown file
    md_files = sorted(catalogue_dir.glob('*.md'))
    md_files = [f for f in md_files if f.name != 'INDEX.md']  # Skip INDEX
    
    total_original_size = 0
    total_json_size = 0
    
    for md_file in md_files:
        print(f"Processing {md_file.name}...")
        
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        original_size = len(markdown_content.encode('utf-8'))
        total_original_size += original_size
        
        # Convert to JSON
        json_data = markdown_to_json(markdown_content, str(md_file))
        
        # Write JSON file
        json_file = json_dir / f"{md_file.stem}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        json_size = os.path.getsize(json_file)
        total_json_size += json_size
        
        compression_ratio = (1 - json_size / original_size) * 100
        print(f"  Original: {original_size:,} bytes, JSON: {json_size:,} bytes, "
              f"Ratio: {compression_ratio:.1f}%")
    
    # Create JSON index
    json_index = {
        'metadata': {
            'created': datetime.utcnow().isoformat() + 'Z',
            'total_files': len(md_files),
            'total_original_size': total_original_size,
            'total_json_size': total_json_size,
            'compression_ratio': (1 - total_json_size / total_original_size) * 100
        },
        'files': []
    }
    
    for md_file in md_files:
        json_file = json_dir / f"{md_file.stem}.json"
        json_index['files'].append({
            'markdown': md_file.name,
            'json': json_file.name,
            'size_md': os.path.getsize(md_file),
            'size_json': os.path.getsize(json_file)
        })
    
    # Write JSON index
    with open(json_dir / 'INDEX.json', 'w', encoding='utf-8') as f:
        json.dump(json_index, f, indent=2, ensure_ascii=False)
    
    print(f"\nJSON conversion complete!")
    print(f"Total original size: {total_original_size:,} bytes")
    print(f"Total JSON size: {total_json_size:,} bytes")
    print(f"Overall compression: {(1 - total_json_size / total_original_size) * 100:.1f}%")
    print(f"Files processed: {len(md_files)}")
    print(f"JSON files created in: {json_dir}")


def create_search_index():
    """Create a search index from all catalogue content."""
    catalogue_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/catalogue')
    search_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/search')
    search_dir.mkdir(exist_ok=True)
    
    search_index = {
        'version': '1.0',
        'created': datetime.utcnow().isoformat() + 'Z',
        'documents': [],
        'statistics': {
            'total_sections': 0,
            'total_words': 0,
            'total_characters': 0
        }
    }
    
    # Process all catalogue files
    md_files = sorted(catalogue_dir.glob('*.md'))
    md_files = [f for f in md_files if f.name != 'INDEX.md']
    
    section_counter = 0
    word_counter = 0
    char_counter = 0
    
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract sections
        sections = re.split(r'\n(## \d+\. .*?)\n', content)
        header = sections[0]
        
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                heading = sections[i]
                section_content = sections[i + 1]
                
                # Extract section number and title
                match = re.match(r'## (\d+)\. (.*)', heading)
                if match:
                    section_num = match.group(1)
                    section_title = match.group(2)
                    
                    # Create search document
                    doc = {
                        'id': f"{md_file.stem}_{section_num}",
                        'source_file': md_file.name,
                        'section_number': section_num,
                        'title': section_title,
                        'content': section_content.strip(),
                        'file_path': str(md_file.relative_to(catalogue_dir)),
                        'word_count': len(section_content.split()),
                        'char_count': len(section_content)
                    }
                    
                    search_index['documents'].append(doc)
                    section_counter += 1
                    word_counter += doc['word_count']
                    char_counter += doc['char_count']
    
    search_index['statistics'] = {
        'total_sections': section_counter,
        'total_words': word_counter,
        'total_characters': char_counter,
        'total_documents': len(search_index['documents'])
    }
    
    # Write search index
    search_file = search_dir / 'catalogue_search_index.json'
    with open(search_file, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, indent=2, ensure_ascii=False)
    
    print(f"\nSearch index created!")
    print(f"Total sections indexed: {section_counter}")
    print(f"Total words: {word_counter:,}")
    print(f"Total characters: {char_counter:,}")
    print(f"Search index file: {search_file}")
    print(f"Index size: {os.path.getsize(search_file):,} bytes")


if __name__ == '__main__':
    print("=== Converting Catalogue to JSON ===")
    process_catalogue_files()
    
    print("\n=== Creating Search Index ===")
    create_search_index()
    
    print("\n=== All JSON conversions complete! ===")
