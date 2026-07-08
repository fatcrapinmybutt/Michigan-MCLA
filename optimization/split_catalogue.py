#!/usr/bin/env python3
"""
Catalogue Splitter Script
Splits the large catalogue.md file into logical sections for better performance.
"""

import re
import os
from pathlib import Path

def split_catalogue(input_file, output_dir, section_ranges):
    """
    Split catalogue.md into sections based on heading levels.
    
    Args:
        input_file: Path to the input catalogue.md file
        output_dir: Directory to save split files
        section_ranges: Dict mapping section ranges to output filenames
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by top-level headings (##)
    sections = re.split(r'\n(## .*?)\n', content)
    
    # The first section is the header (before first ##)
    header = sections[0]
    
    # Recombine sections: [header, heading1, content1, heading2, content2, ...]
    combined_sections = []
    for i in range(1, len(sections), 2):
        if i + 1 < len(sections):
            heading = sections[i]
            content_part = sections[i + 1]
            combined_sections.append((heading, content_part))
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Write each section to its file
    current_section = []
    current_start = 1
    
    for heading, content_part in combined_sections:
        # Extract section number from heading
        match = re.match(r'## (\d+)\.', heading)
        if match:
            section_num = int(match.group(1))
            
            # If we've moved to a new section range, write the previous one
            for range_key, filename in section_ranges.items():
                range_start, range_end = map(int, range_key.split('-'))
                if section_num > range_end and current_section:
                    # Write the accumulated content
                    full_content = header + '\n\n' + '\n\n'.join(current_section)
                    output_path = Path(output_dir) / f"{filename}.md"
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(full_content)
                    print(f"Written: {output_path} ({len(full_content)} bytes)")
                    current_section = []
                    current_start = section_num
                    break
            
            # Add the heading and content to current section
            current_section.append(heading)
            current_section.append(content_part)
    
    # Write the last accumulated section
    if current_section:
        full_content = header + '\n\n' + '\n\n'.join(current_section)
        # Find the appropriate filename for the last range
        last_range = list(section_ranges.keys())[-1]
        last_filename = section_ranges[last_range]
        output_path = Path(output_dir) / f"{last_filename}.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        print(f"Written: {output_path} ({len(full_content)} bytes)")
    
    # Create an index file
    index_content = "# Catalogue Index\n\n"
    index_content += "This directory contains the split catalogue sections for better performance.\n\n"
    index_content += "## Sections\n\n"
    
    for range_key, filename in section_ranges.items():
        range_start, range_end = range_key.split('-')
        index_content += f"- [Sections {range_start}-{range_end}]({filename}.md) - {range_start}-{range_end}\n"
    
    index_content += "\n## Original File\n\n"
    index_content += f"- [Complete Catalogue](../catalogue.md) - All sections combined\n"
    
    with open(Path(output_dir) / "INDEX.md", 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"Written: {output_dir}/INDEX.md")
    print(f"\nTotal: Split catalogue.md into {len(section_ranges)} sections")

if __name__ == "__main__":
    # Define section ranges and output filenames
    section_ranges = {
        '1-10': '01-10',
        '11-20': '11-20', 
        '21-30': '21-30',
        '31-42': '31-42',
        '43-60': '43-60'
    }
    
    input_file = '/workspace/fatcrapinmybutt__Michigan-MCLA/catalogue.md'
    output_dir = '/workspace/fatcrapinmybutt__Michigan-MCLA/catalogue'
    
    split_catalogue(input_file, output_dir, section_ranges)
    
    print("\n✅ Catalogue splitting complete!")
