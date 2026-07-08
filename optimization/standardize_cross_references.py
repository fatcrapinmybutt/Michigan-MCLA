#!/usr/bin/env python3
"""
Standardize cross-references across all repositories for consistent navigation.
Creates a unified linking system with standardized formats and validation.
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime, timezone


def create_cross_reference_standard():
    """Create a standard for cross-repository references."""
    optimization_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/optimization')
    
    standard = {
        'version': '1.0',
        'created': datetime.now(timezone.utc).isoformat(),
        'purpose': 'Standardize cross-references across all Michigan Legal Knowledge Base repositories',
        'formats': {
            'markdown_link': {
                'description': 'Standard markdown link format for cross-repository references',
                'template': '[{description}]({url})',
                'examples': [
                    '[MCL §600.1415](https://github.com/fatcrapinmybutt/Michigan-MCLA/blob/main/catalogue/01-10.md#15)',
                    '[MCR 2.116](https://github.com/fatcrapinmybutt/CourtRules/blob/main/mcr/02.md#2116)',
                    '[Supreme Court Opinion](https://github.com/fatcrapinmybutt/MICHIGAN-HIGHER-COURTS/blob/main/supreme_court/2024/opinion_12345.md)'
                ]
            },
            'relative_link': {
                'description': 'Relative links within same repository',
                'template': '[{description}](./{path}#{anchor})',
                'examples': [
                    '[Section 15](./01-10.md#15)',
                    '[MCL Chapter 600](../mcl/600.md)',
                    '[Optimization Plan](../OPTIMIZATION_MASTER_PLAN.md)'
                ]
            },
            'json_reference': {
                'description': 'JSON format for programmatic references',
                'template': '{"type": "{type}", "repository": "{repo}", "path": "{path}", "anchor": "{anchor}", "description": "{description}"}',
                'examples': [
                    '{"type": "statute", "repository": "Michigan-MCLA", "path": "catalogue/01-10.md", "anchor": "15", "description": "MCL §600.1415"}',
                    '{"type": "rule", "repository": "CourtRules", "path": "mcr/02.md", "anchor": "2116", "description": "MCR 2.116"}',
                    '{"type": "case", "repository": "MICHIGAN-HIGHER-COURTS", "path": "supreme_court/2024/opinion_12345.md", "description": "Smith v. Jones"}'
                ]
            }
        },
        'link_types': {
            'statute': {
                'description': 'References to Michigan Compiled Laws statutes',
                'prefix': 'MCL',
                'format': '§{chapter}.{section}',
                'example': 'MCL §600.1415',
                'repository': 'Michigan-MCLA',
                'path_template': 'catalogue/{section_file}.md#{section}'
            },
            'court_rule': {
                'description': 'References to Michigan Court Rules',
                'prefix': 'MCR',
                'format': '{chapter}.{rule}',
                'example': 'MCR 2.116',
                'repository': 'CourtRules',
                'path_template': 'mcr/{chapter}.md#{rule}'
            },
            'evidence_rule': {
                'description': 'References to Michigan Rules of Evidence',
                'prefix': 'MRE',
                'format': '{article}.{rule}',
                'example': 'MRE 404',
                'repository': 'CourtRules',
                'path_template': 'mre/{article}.md#{rule}'
            },
            'case': {
                'description': 'References to court opinions',
                'prefix': 'Case',
                'format': '{plaintiff} v. {defendant}',
                'example': 'Smith v. Jones',
                'repository': 'MICHIGAN-HIGHER-COURTS',
                'path_template': '{court}/{year}/{case_file}.md'
            },
            'form': {
                'description': 'References to SCAO forms',
                'prefix': 'Form',
                'format': '{form_number}',
                'example': 'DC 84',
                'repository': 'CourtRules',
                'path_template': 'forms/{form_file}.md'
            },
            'doctrine': {
                'description': 'References to legal doctrine',
                'prefix': 'Doctrine',
                'format': '{doctrine_name}',
                'example': 'Res Judicata',
                'repository': 'fredprime-legal-system',
                'path_template': 'doctrine/{doctrine_file}.md'
            },
            'template': {
                'description': 'References to litigation templates',
                'prefix': 'Template',
                'format': '{template_name}',
                'example': 'Complaint Template',
                'repository': 'LitigationOS',
                'path_template': 'templates/{template_file}.md'
            }
        },
        'repository_mapping': {
            'Michigan-MCLA': {
                'base_url': 'https://github.com/fatcrapinmybutt/Michigan-MCLA/blob/main/',
                'local_path': '/workspace/fatcrapinmybutt__Michigan-MCLA/',
                'content_types': ['catalogue', 'mcl', 'optimization', 'navigation', 'search']
            },
            'MICHIGAN-HIGHER-COURTS': {
                'base_url': 'https://github.com/fatcrapinmybutt/MICHIGAN-HIGHER-COURTS/blob/main/',
                'local_path': '/workspace/fatcrapinmybutt__MICHIGAN-HIGHER-COURTS/',
                'content_types': ['supreme_court', 'court_of_appeals', 'opinions']
            },
            'CourtRules': {
                'base_url': 'https://github.com/fatcrapinmybutt/CourtRules/blob/main/',
                'local_path': '/workspace/fatcrapinmybutt__CourtRules/',
                'content_types': ['mcr', 'mre', 'forms', 'procedures']
            },
            'fredprime-legal-system': {
                'base_url': 'https://github.com/fatcrapinmybutt/fredprime-legal-system/blob/main/',
                'local_path': '/workspace/fatcrapinmybutt__fredprime-legal-system/',
                'content_types': ['architecture', 'doctrine', 'framework']
            },
            'LitigationOS': {
                'base_url': 'https://github.com/fatcrapinmybutt/LitigationOS/blob/main/',
                'local_path': '/workspace/fatcrapinmybutt__LitigationOS/',
                'content_types': ['workflow', 'templates', 'automation']
            },
            'michigancompiledlawsMBP': {
                'base_url': 'https://github.com/fatcrapinmybutt/michigancompiledlawsMBP/blob/main/',
                'local_path': '/workspace/fatcrapinmybutt__michigancompiledlawsMBP/',
                'content_types': ['html_archive', 'mcl_chapters']
            }
        },
        'validation_rules': {
            'required_fields': ['type', 'repository', 'path', 'description'],
            'url_format': 'https://github.com/{owner}/{repo}/blob/{branch}/{path}',
            'branch_default': 'main',
            'description_max_length': 200,
            'path_max_length': 500
        },
        'best_practices': {
            'use_descriptive_text': 'Link text should describe the destination, not just "click here"',
            'prefer_relative_links': 'Use relative links within same repository when possible',
            'include_context': 'Add context in parentheses after link when helpful',
            'consistent_formatting': 'Use consistent formatting for similar link types',
            'anchor_links': 'Use anchor links (#section) for direct access to sections',
            'validate_links': 'Regularly validate that all cross-references are still valid'
        }
    }
    
    # Write standard
    with open(optimization_dir / 'CROSS_REFERENCE_STANDARD.json', 'w', encoding='utf-8') as f:
        json.dump(standard, f, indent=2, ensure_ascii=False)
    
    print(f"Cross-reference standard created: {optimization_dir / 'CROSS_REFERENCE_STANDARD.json'}")
    print(f"File size: {os.path.getsize(optimization_dir / 'CROSS_REFERENCE_STANDARD.json'):,} bytes")
    
    return standard


def create_link_validator():
    """Create a script for validating cross-references."""
    optimization_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/optimization')
    
    validator_script = '''#!/usr/bin/env python3
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
    links = re.findall(r'\[([^\\]]+)\]\(([^\)]+)\)', content)
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
            print(f"\\nFile: {issue['file']}")
            print(f"  Link: [{issue['link_text']}]({issue['url']})")
            for problem in issue['issues']:
                print(f"    - {problem}")
        sys.exit(1)
    else:
        print("All links validated successfully!")
        sys.exit(0)


if __name__ == '__main__':
    main()
'''
    
    # Write validator script
    with open(optimization_dir / 'validate_cross_references.py', 'w', encoding='utf-8') as f:
        f.write(validator_script)
    
    print(f"Link validator script created: {optimization_dir / 'validate_cross_references.py'}")
    print(f"File size: {os.path.getsize(optimization_dir / 'validate_cross_references.py'):,} bytes")


def create_link_generator():
    """Create a script for generating standardized cross-references."""
    optimization_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/optimization')
    
    generator_script = '''#!/usr/bin/env python3
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
    print("\\nStatute Links:")
    print(generate_statute_link('600.1415'))
    print(generate_statute_link('600.5805', 'Revival of Judgment'))
    
    print("\\nCourt Rule Links:")
    print(generate_court_rule_link('2.116'))
    print(generate_court_rule_link('7.215', 'Summary Disposition'))
    
    print("\\nCase Links:")
    print(generate_case_link('Smith v Jones', '2024', 'supreme_court'))
    print(generate_case_link('Doe v City of Detroit', '2023', 'court_of_appeals', 'Municipal Liability'))
    
    print("\\nJSON References:")
    print(generate_json_reference('statute', 'MCL §600.1415', 'Michigan-MCLA', 'catalogue/01-10.md', '600.1415'))


if __name__ == '__main__':
    main()
'''
    
    # Write generator script
    with open(optimization_dir / 'generate_cross_references.py', 'w', encoding='utf-8') as f:
        f.write(generator_script)
    
    print(f"Link generator script created: {optimization_dir / 'generate_cross_references.py'}")
    print(f"File size: {os.path.getsize(optimization_dir / 'generate_cross_references.py'):,} bytes")


def update_readme_with_standards():
    """Update the optimization README with cross-reference standards."""
    optimization_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/optimization')
    
    readme_content = f"""# Optimization Scripts and Standards

This directory contains optimization scripts and standards for the Michigan Legal Knowledge Base.

## Cross-Reference Standards

The Michigan Legal Knowledge Base uses standardized cross-references across all repositories to ensure consistent navigation and link validity.

### Standard Formats

1. **Markdown Links**: `[description](url)`
   - Use descriptive text that explains the destination
   - Prefer relative links within same repository
   - Include anchors (#section) for direct access

2. **JSON References**: Structured format for programmatic access
   - Type: statute, court_rule, case, form, doctrine, template
   - Repository: target repository name
   - Path: file path
   - Anchor: section identifier (optional)

### Link Types

- **Statute**: `MCL §600.1415` → Michigan-MCLA repository
- **Court Rule**: `MCR 2.116` → CourtRules repository
- **Evidence Rule**: `MRE 404` → CourtRules repository
- **Case**: `Smith v. Jones` → MICHIGAN-HIGHER-COURTS repository
- **Form**: `DC 84` → CourtRules repository
- **Doctrine**: `Res Judicata` → fredprime-legal-system repository
- **Template**: `Complaint Template` → LitigationOS repository

### Repository Mapping

| Repository | Base URL | Local Path | Content Types |
|------------|----------|------------|---------------|
| Michigan-MCLA | https://github.com/fatcrapinmybutt/Michigan-MCLA/blob/main/ | /workspace/fatcrapinmybutt__Michigan-MCLA/ | catalogue, mcl, optimization, navigation, search |
| MICHIGAN-HIGHER-COURTS | https://github.com/fatcrapinmybutt/MICHIGAN-HIGHER-COURTS/blob/main/ | /workspace/fatcrapinmybutt__MICHIGAN-HIGHER-COURTS/ | supreme_court, court_of_appeals, opinions |
| CourtRules | https://github.com/fatcrapinmybutt/CourtRules/blob/main/ | /workspace/fatcrapinmybutt__CourtRules/ | mcr, mre, forms, procedures |
| fredprime-legal-system | https://github.com/fatcrapinmybutt/fredprime-legal-system/blob/main/ | /workspace/fatcrapinmybutt__fredprime-legal-system/ | architecture, doctrine, framework |
| LitigationOS | https://github.com/fatcrapinmybutt/LitigationOS/blob/main/ | /workspace/fatcrapinmybutt__LitigationOS/ | workflow, templates, automation |
| michigancompiledlawsMBP | https://github.com/fatcrapinmybutt/michigancompiledlawsMBP/blob/main/ | /workspace/fatcrapinmybutt__michigancompiledlawsMBP/ | html_archive, mcl_chapters |

### Scripts

- `CROSS_REFERENCE_STANDARD.json` - Complete standard specification
- `validate_cross_references.py` - Validate all links in a repository
- `generate_cross_references.py` - Generate standardized cross-references
- `split_catalogue_v3.py` - Split large markdown files
- `convert_to_json.py` - Convert markdown to JSON
- `compress_json.py` - Create compressed JSON versions
- `create_navigation.py` - Create navigation system

### Usage

```bash
# Validate all links in current repository
python optimization/validate_cross_references.py .

# Generate a statute link
python optimization/generate_cross_references.py
```

### Best Practices

1. **Descriptive Text**: Link text should describe the destination
2. **Relative Links**: Use relative links within same repository
3. **Context**: Add context in parentheses when helpful
4. **Consistency**: Use consistent formatting for similar link types
5. **Validation**: Regularly validate cross-references
6. **Anchors**: Use anchor links for direct section access

### Authority Hierarchy

All cross-references should respect the Michigan authority hierarchy:

1. **BINDING_MICHIGAN** (Weight: 1.0)
   - Michigan Constitution
   - Michigan Compiled Laws (MCL)
   - Michigan Court Rules (MCR)
   - Michigan Rules of Evidence (MRE)
   - Michigan Supreme Court opinions

2. **PERSUASIVE_MICHIGAN** (Weight: 0.8)
   - Michigan Court of Appeals opinions
   - Federal district court opinions applying Michigan law
   - Michigan Attorney General opinions

3. **SECONDARY_MICHIGAN** (Weight: 0.6)
   - Michigan administrative rules
   - Michigan jury instructions
   - Michigan practice manuals

4. **NON_MICHIGAN** (Weight: 0.4)
   - Federal law (when not preempted)
   - Other state court opinions
   - Legal treatises and law review articles

### Version Information

- Standard Version: 1.0
- Created: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
- Part of: Ω-CONVERGENCE MICHIGAN LEGAL INTELLIGENCE SINGULARITY
"""
    
    # Write README
    with open(optimization_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"Optimization README created: {optimization_dir / 'README.md'}")
    print(f"File size: {os.path.getsize(optimization_dir / 'README.md'):,} bytes")


if __name__ == '__main__':
    print("=== Creating Cross-Reference Standardization System ===")
    
    print("\\n--- Cross-Reference Standard ---")
    standard = create_cross_reference_standard()
    
    print("\\n--- Link Validator ---")
    create_link_validator()
    
    print("\\n--- Link Generator ---")
    create_link_generator()
    
    print("\\n--- Optimization README ---")
    update_readme_with_standards()
    
    print("\\n=== Cross-reference standardization system complete! ===")
    print("Files created in: /workspace/fatcrapinmybutt__Michigan-MCLA/optimization/")
