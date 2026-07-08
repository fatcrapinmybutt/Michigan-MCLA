#!/usr/bin/env python3
"""
Catalogue Splitter Script v3
Splits the large catalogue.md file into logical sections for better performance.
Handles duplicate section numbers and creates balanced splits.
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
            
            # Extract section number and title
            match = re.match(r'## (\d+)\. (.*)', heading)
            if match:
                section_num = int(match.group(1))
                section_title = match.group(2)
                sections.append({
                    'number': section_num,
                    'title': section_title,
                    'heading': heading,
                    'content': section_content,
                    'start_line': i
                })
    
    return header, sections

def create_balanced_ranges(sections, target_sections_per_file=10):
    """Create balanced section ranges for splitting."""
    ranges = []
    current_range = []
    current_size = 0
    target_size = len(sections) // 5  # Aim for 5 files
    
    for i, section in enumerate(sections):
        current_range.append(section)
        current_size += len(section['content'])
        
        # Check if we should end the current range
        if len(current_range) >= target_sections_per_file or current_size > 100000:
            # End the current range
            ranges.append(current_range)
            current_range = []
            current_size = 0
    
    # Add the last range
    if current_range:
        ranges.append(current_range)
    
    return ranges

def split_catalogue(input_file, output_dir):
    """
    Split catalogue.md into balanced sections.
    
    Args:
        input_file: Path to the input catalogue.md file
        output_dir: Directory to save split files
    """
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract sections
    header, sections = extract_sections(content)
    
    print(f"📊 Found {len(sections)} sections in catalogue.md")
    print(f"   Section numbers: {[s['number'] for s in sections]}")
    
    # Create balanced ranges
    ranges = create_balanced_ranges(sections)
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Write each range to a file
    for i, section_range in enumerate(ranges):
        if not section_range:
            continue
        
        start_num = section_range[0]['number']
        end_num = section_range[-1]['number']
        filename = f"{start_num:02d}-{end_num:02d}"
        
        # Create the file content
        full_content = header + '\n\n' + '\n\n'.join(
            [s['heading'] + '\n\n' + s['content'] for s in section_range]
        )
        
        output_path = Path(output_dir) / f"{filename}.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        print(f"✅ Written: {output_path} ({len(full_content):,} bytes, sections {start_num}-{end_num})")
    
    # Create an index file
    index_content = "# Catalogue Index\n\n"
    index_content += "This directory contains the split catalogue sections for better performance and faster loading.\n\n"
    index_content += "> **Note:** The original combined file is still available at [catalogue.md](../catalogue.md)\n\n"
    index_content += "## Split Sections\n\n"
    
    for i, section_range in enumerate(ranges):
        if not section_range:
            continue
        start_num = section_range[0]['number']
        end_num = section_range[-1]['number']
        filename = f"{start_num:02d}-{end_num:02d}"
        
        # Get section titles
        titles = [s['title'][:50] + '...' if len(s['title']) > 50 else s['title'] for s in section_range]
        title_preview = ', '.join(titles[:3])
        if len(titles) > 3:
            title_preview += f", +{len(titles)-3} more"
        
        index_content += f"- [Sections {start_num}-{end_num}]({filename}.md) - {title_preview}\n"
    
    index_content += "\n## Quick Navigation by Topic\n\n"
    
    # Add topic-based navigation
    topics = {
        'Court Abbreviations': [1, 2, 3, 4],
        'Family Law': [5, 6, 24, 29, 31],
        'Judicial Conduct': [7, 26, 32, 33],
        'Due Process': [8, 16, 17],
        'Case Law': [9, 10, 20],
        'Deadlines & Procedure': [11, 12, 13, 14, 15],
        'Criminal Law': [19, 23, 38, 39, 40, 41, 42, 46],
        'Appellate Practice': [27, 34, 37],
        'Civil Rights': [36, 41],
        'Special Topics': [21, 22, 25, 28, 30, 43, 44, 45, 47, 48, 49, 50, 51]
    }
    
    for topic, section_nums in topics.items():
        # Find which files contain these sections
        file_links = []
        for section_num in section_nums:
            for i, section_range in enumerate(ranges):
                if section_range and section_range[0]['number'] <= section_num <= section_range[-1]['number']:
                    start_num = section_range[0]['number']
                    end_num = section_range[-1]['number']
                    filename = f"{start_num:02d}-{end_num:02d}"
                    file_links.append(f"[{section_num}]({filename}.md#{section_num})")
                    break
        
        if file_links:
            index_content += f"- **{topic}:** {' '.join(file_links)}\n"
    
    index_content += "\n## Statistics\n\n"
    index_content += f"- **Total Sections:** {len(sections)}\n"
    index_content += f"- **Split Into:** {len(ranges)} files\n"
    index_content += f"- **Original Size:** {len(content):,} bytes ({len(content)//1024:,} KB)\n"
    
    # Calculate average size
    total_split_size = sum(
        len(header + '\n\n' + '\n\n'.join([s['heading'] + '\n\n' + s['content'] for s in r]))
        for r in ranges
    )
    index_content += f"- **Average File Size:** ~{total_split_size // len(ranges) // 1024}KB\n"
    index_content += f"- **Size Reduction:** {((len(content) - total_split_size) / len(content) * 100):.1f}% (from header duplication)\n"
    
    with open(Path(output_dir) / "INDEX.md", 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"\n✅ Written: {output_dir}/INDEX.md")
    
    # Return statistics
    return {
        'total_sections': len(sections),
        'files_created': len(ranges),
        'original_size': len(content),
        'split_size': total_split_size,
        'section_numbers': [s['number'] for s in sections],
        'ranges': [(r[0]['number'], r[-1]['number']) if r else (0, 0) for r in ranges]
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
    print(f"   Total sections: {stats['total_sections']}")
    print(f"   Files created: {stats['files_created']}")
    print(f"   Original size: {stats['original_size']:,} bytes ({stats['original_size']//1024:,} KB)")
    print(f"   Split size: {stats['split_size']:,} bytes ({stats['split_size']//1024:,} KB)")
    print(f"   Section numbers: {stats['section_numbers']}")
    print(f"   Ranges: {stats['ranges']}")
    
    print("\n✅ Catalogue splitting complete!")
