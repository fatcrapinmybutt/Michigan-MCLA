#!/usr/bin/env python3
"""
Generate standardized cross-references for Michigan Legal Knowledge Base.
"""

import json
import os
from pathlib import Path


def load_standard():
    """Load the cross-reference standard."""
    standard_path = Path(__file__).parent / 'CROSS_REFERENCE_STANDARD.json'
    with open(standard_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_markdown_link(link_type, description, repository, path, anchor=None, use_github=True):
    """Generate a standardized markdown link."""
    standard = load_standard()
    
    # Get repository info
    repo_info = standard['repository_mapping'].get(repository)
    if not repo_info:
        raise ValueError(f"Unknown repository: {repository}")
    
    # Build URL
    if use_github:
        base_url = repo_info['base_url']
        if anchor:
            url = f"{base_url}{path}#{anchor}"
        else:
            url = f"{base_url}{path}"
    else:
        # Relative path
        if anchor:
            url = f"./{path}#{anchor}"
        else:
            url = f"./{path}"
    
    # Create link
    return f"[{description}]({url})"


def generate_json_reference(link_type, description, repository, path, anchor=None):
    """Generate a standardized JSON reference."""
    ref = {
        'type': link_type,
        'repository': repository,
        'path': path,
        'description': description
    }
    if anchor:
        ref['anchor'] = anchor
    
    return json.dumps(ref, indent=2, ensure_ascii=False)


def generate_statute_link(section, description=None):
    """Generate a link to a specific MCL statute."""
    if not description:
        description = f"MCL §{section}"
    
    # Determine which file contains this section
    chapter = section.split('.')[0]
    section_num = section.split('.')[1]
    
    # Map to catalogue file (simplified - would need actual mapping)
    if int(chapter) <= 600:
        catalogue_file = '01-10.md'
    elif int(chapter) <= 1000:
        catalogue_file = '11-20.md'
    else:
        catalogue_file = '21-30.md'
    
    return generate_markdown_link(
        'statute',
        description,
        'Michigan-MCLA',
        f'catalogue/{catalogue_file}',
        anchor=section
    )


def generate_court_rule_link(rule, description=None):
    """Generate a link to a specific MCR rule."""
    if not description:
        description = f"MCR {rule}"
    
    chapter = rule.split('.')[0]
    return generate_markdown_link(
        'court_rule',
        description,
        'CourtRules',
        f'mcr/{chapter}.md',
        anchor=rule
    )


def generate_case_link(case_name, year, court, description=None):
    """Generate a link to a specific case."""
    if not description:
        description = case_name
    
    # Clean case name for filename
    clean_name = case_name.replace(' ', '_').replace('v.', 'v')
    filename = f"{year}_{clean_name}.md"
    
    return generate_markdown_link(
        'case',
        description,
        'MICHIGAN-HIGHER-COURTS',
        f'{court}/{year}/{filename}'
    )


def main():
    """Main function with examples."""
    print("Cross-Reference Generator")
    print("=" * 50)
    
    # Examples
    print("\nStatute Links:")
    print(generate_statute_link('600.1415'))
    print(generate_statute_link('600.5805', 'Revival of Judgment'))
    
    print("\nCourt Rule Links:")
    print(generate_court_rule_link('2.116'))
    print(generate_court_rule_link('7.215', 'Summary Disposition'))
    
    print("\nCase Links:")
    print(generate_case_link('Smith v Jones', '2024', 'supreme_court'))
    print(generate_case_link('Doe v City of Detroit', '2023', 'court_of_appeals', 'Municipal Liability'))
    
    print("\nJSON References:")
    print(generate_json_reference('statute', 'MCL §600.1415', 'Michigan-MCLA', 'catalogue/01-10.md', '600.1415'))


if __name__ == '__main__':
    main()
