#!/usr/bin/env python3
"""
Catalogue Splitter Script v2
Splits the large catalogue.md file into logical sections for better performance.
Fixed version that properly handles section ranges.
"""

import re
from pathlib import Path

def extract_sections(content):
    """Extract all sections from the catalogue content."""
    # Split by top-level headings (##)
    parts = re.split(r'\n(## \d+\. .*?)\n', content)
    
    # The first part is the header (before first ##)
    header = parts[0]
    
    # Recombine: [header, heading1, content1, heading2, content2, ...]
    sections = []
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            heading = parts[i]
            section_content = parts[i + 1]
            
            # Extract section number
            match = re.match(r'## (\d+)\.', heading)
            if match:
                section_num = int(match.group(1))
                sections.append({
                    'number': section_num,
                    'heading': heading,
                    'content': section_content
                })
    
    return header, sections

def split_catalogue(input_file, output_dir):
    """
    Split catalogue.md into sections based on natural breaks.
    
    Args:
        input_file: Path to the input catalogue.md file
        output_dir: Directory to save split files
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract sections
    header, sections = extract_sections(content)
    
    # Define section ranges (each range becomes a file)
    section_ranges = [
        (1, 10, '01-10'),
        (11, 20, '11-20'),
        (21, 30, '21-30'),
        (31, 42, '31-42'),
        (43, 60, '43-60')
    ]
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Group sections by range
    current_range_index = 0
    current_sections = []
    
    for section in sections:
        section_num = section['number']
        
        # Check if we need to start a new range
        while current_range_index < len(section_ranges):
            range_start, range_end, filename = section_ranges[current_range_index]
            
            if section_num < range_start:
                # This section is before the current range, skip
                current_range_index += 1
                continue
            
            if range_start <= section_num <= range_end:
                # This section belongs to the current range
                current_sections.append(section)
                break
            
            if section_num > range_end:
                # We've passed the current range, save it and move to next
                if current_sections:
                    # Save the current range
                    range_start, range_end, filename = section_ranges[current_range_index]
                    full_content = header + '\n\n' + '\n\n'.join(
                        [s['heading'] + '\n\n' + s['content'] for s in current_sections]
                    )
                    output_path = Path(output_dir) / f"{filename}.md"
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(full_content)
                    print(f"✅ Written: {output_path} ({len(full_content):,} bytes, sections {current_sections[0]['number']}-{current_sections[-1]['number']})")
                
                # Reset for next range
                current_sections = []
                current_range_index += 1
    
    # Save the last range
    if current_sections and current_range_index < len(section_ranges):
        range_start, range_end, filename = section_ranges[current_range_index]
        full_content = header + '\n\n' + '\n\n'.join(
            [s['heading'] + '\n\n' + s['content'] for s in current_sections]
        )
        output_path = Path(output_dir) / f"{filename}.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        print(f"✅ Written: {output_path} ({len(full_content):,} bytes, sections {current_sections[0]['number']}-{current_sections[-1]['number']})")
    
    # Create an index file
    index_content = "# Catalogue Index\n\n"
    index_content += "This directory contains the split catalogue sections for better performance and faster loading.\n\n"
    index_content += "> **Note:** The original combined file is still available at [catalogue.md](../catalogue.md)\n\n"
    index_content += "## Split Sections\n\n"
    
    for range_start, range_end, filename in section_ranges:
        index_content += f"- [Sections {range_start}-{range_end}]({filename}.md) - Covers sections {range_start} through {range_end}\n"
    
    index_content += "\n## Quick Navigation\n\n"
    index_content += "- **Family Law:** Sections 5-6, 24, 29, 31\n"
    index_content += "- **Tort Law:** Sections 26, 34-38\n"
    index_content += "- **Criminal Law:** Sections 19, 23\n"
    index_content += "- **Appellate:** Sections 27, 34, 37\n"
    index_content += "- **Procedure:** Sections 1-4, 8, 11, 20\n"
    
    index_content += "\n## Statistics\n\n"
    index_content += f"- **Total Sections:** {len(sections)}\n"
    index_content += f"- **Split Into:** {len(section_ranges)} files\n"
    index_content += f"- **Average Size:** ~{len(content) // len(section_ranges) // 1024}KB per file\n"
    
    with open(Path(output_dir) / "INDEX.md", 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"\n✅ Written: {output_dir}/INDEX.md")
    
    # Return statistics
    return {
        'total_sections': len(sections),
        'files_created': len(section_ranges),
        'original_size': len(content),
        'section_numbers': [s['number'] for s in sections]
    }

if __name__ == "__main__":
    input_file = '/workspace/fatcrapinmybutt__Michigan-MCLA/catalogue.md'
    output_dir = '/workspace/fatcrapinmybutt__Michigan-MCLA/catalogue'
    
    print("🔄 Splitting catalogue.md into optimized sections...")
    print(f"📄 Input: {input_file}")
    print(f"📁 Output: {output_dir}")
    print()
    
    stats = split_catalogue(input_file, output_dir)
    
    print(f"\n📊 Statistics:")
    print(f"   Total sections extracted: {stats['total_sections']}")
    print(f"   Files created: {stats['files_created']}")
    print(f"   Original size: {stats['original_size']:,} bytes ({stats['original_size']//1024:,} KB)")
    print(f"   Section numbers: {stats['section_numbers']}")
    
    print("\n✅ Catalogue splitting complete!")
