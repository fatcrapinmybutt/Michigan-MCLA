#!/usr/bin/env python3
"""
Create compressed JSON versions with better compression ratios.
Uses gzip compression and minified JSON for optimal performance.
"""

import json
import gzip
import os
import hashlib
from pathlib import Path
from datetime import datetime, timezone


def create_minified_json():
    """Create minified JSON versions of catalogue files."""
    catalogue_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/catalogue')
    json_dir = catalogue_dir / 'json'
    minified_dir = catalogue_dir / 'minified'
    compressed_dir = catalogue_dir / 'compressed'
    
    # Create directories
    minified_dir.mkdir(exist_ok=True)
    compressed_dir.mkdir(exist_ok=True)
    
    # Process each JSON file
    json_files = sorted(json_dir.glob('*.json'))
    json_files = [f for f in json_files if f.name != 'INDEX.json']
    
    total_original = 0
    total_minified = 0
    total_compressed = 0
    
    for json_file in json_files:
        print(f"Processing {json_file.name}...")
        
        # Read original JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        original_size = os.path.getsize(json_file)
        total_original += original_size
        
        # Create minified JSON (no whitespace)
        minified_file = minified_dir / f"{json_file.stem}.min.json"
        with open(minified_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, separators=(',', ':'), ensure_ascii=False)
        
        minified_size = os.path.getsize(minified_file)
        total_minified += minified_size
        
        # Create gzip compressed JSON
        compressed_file = compressed_dir / f"{json_file.stem}.json.gz"
        with open(json_file, 'rb') as f_in:
            with gzip.open(compressed_file, 'wb') as f_out:
                f_out.write(f_in.read())
        
        compressed_size = os.path.getsize(compressed_file)
        total_compressed += compressed_size
        
        print(f"  Original JSON: {original_size:,} bytes")
        print(f"  Minified JSON: {minified_size:,} bytes ({minified_size/original_size*100:.1f}%)")
        print(f"  Compressed GZ: {compressed_size:,} bytes ({compressed_size/original_size*100:.1f}%)")
    
    # Create summary
    print(f"\n=== Compression Summary ===")
    print(f"Total original JSON: {total_original:,} bytes")
    print(f"Total minified JSON: {total_minified:,} bytes ({total_minified/total_original*100:.1f}%)")
    print(f"Total compressed GZ: {total_compressed:,} bytes ({total_compressed/total_original*100:.1f}%)")
    print(f"Compression ratio: {total_original/total_compressed:.1f}x")
    
    # Create index files
    index_data = {
        'created': datetime.now(timezone.utc).isoformat(),
        'files': []
    }
    
    for json_file in json_files:
        stem = json_file.stem
        index_data['files'].append({
            'name': stem,
            'original': json_file.name,
            'original_size': os.path.getsize(json_file),
            'minified': f"{stem}.min.json",
            'minified_size': os.path.getsize(minified_dir / f"{stem}.min.json"),
            'compressed': f"{stem}.json.gz",
            'compressed_size': os.path.getsize(compressed_dir / f"{stem}.json.gz")
        })
    
    # Write indexes
    with open(minified_dir / 'INDEX.json', 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    with open(compressed_dir / 'INDEX.json', 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nIndexes created in minified/ and compressed/ directories")


def create_bundle():
    """Create a single bundled JSON file with all catalogue content."""
    catalogue_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/catalogue')
    json_dir = catalogue_dir / 'json'
    bundle_dir = catalogue_dir / 'bundle'
    
    bundle_dir.mkdir(exist_ok=True)
    
    # Load all JSON files
    json_files = sorted(json_dir.glob('*.json'))
    json_files = [f for f in json_files if f.name != 'INDEX.json']
    
    bundle = {
        'metadata': {
            'created': datetime.now(timezone.utc).isoformat(),
            'format_version': '1.0',
            'total_files': len(json_files)
        },
        'files': {}
    }
    
    total_sections = 0
    total_size = 0
    
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        stem = json_file.stem
        bundle['files'][stem] = data
        
        # Count sections
        if 'sections' in data:
            total_sections += len(data['sections'])
        
        total_size += os.path.getsize(json_file)
    
    bundle['metadata']['total_sections'] = total_sections
    bundle['metadata']['original_total_size'] = total_size
    
    # Write full bundle
    bundle_file = bundle_dir / 'catalogue_bundle.json'
    with open(bundle_file, 'w', encoding='utf-8') as f:
        json.dump(bundle, f, indent=2, ensure_ascii=False)
    
    full_size = os.path.getsize(bundle_file)
    
    # Write minified bundle
    minified_bundle = bundle_dir / 'catalogue_bundle.min.json'
    with open(minified_bundle, 'w', encoding='utf-8') as f:
        json.dump(bundle, f, separators=(',', ':'), ensure_ascii=False)
    
    minified_size = os.path.getsize(minified_bundle)
    
    # Write compressed bundle
    compressed_bundle = bundle_dir / 'catalogue_bundle.json.gz'
    with open(bundle_file, 'rb') as f_in:
        with gzip.open(compressed_bundle, 'wb') as f_out:
            f_out.write(f_in.read())
    
    compressed_size = os.path.getsize(compressed_bundle)
    
    print(f"\n=== Bundle Created ===")
    print(f"Total files bundled: {len(json_files)}")
    print(f"Total sections: {total_sections}")
    print(f"Original total size: {total_size:,} bytes")
    print(f"Full bundle size: {full_size:,} bytes")
    print(f"Minified bundle size: {minified_size:,} bytes ({minified_size/full_size*100:.1f}%)")
    print(f"Compressed bundle size: {compressed_size:,} bytes ({compressed_size/full_size*100:.1f}%)")
    print(f"Compression ratio: {full_size/compressed_size:.1f}x")


if __name__ == '__main__':
    print("=== Creating Minified and Compressed JSON ===")
    create_minified_json()
    
    print("\n=== Creating Bundle ===")
    create_bundle()
    
    print("\n=== All compression tasks complete! ===")
