#!/usr/bin/env python3
"""
Create a comprehensive navigation system for the Michigan Legal Knowledge Base.
Generates HTML navigation, cross-repository links, and quick access indexes.
"""

import json
import re
import os
from pathlib import Path
from datetime import datetime, timezone


def create_html_navigation():
    """Create HTML navigation files for web-based browsing."""
    catalogue_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/catalogue')
    nav_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/navigation')
    
    nav_dir.mkdir(exist_ok=True)
    
    # Create main navigation index
    html_index = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Michigan Legal Knowledge Base - Navigation</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        h1 {{
            color: #003366;
            border-bottom: 2px solid #003366;
            padding-bottom: 10px;
        }}
        .section {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #003366;
            margin-top: 0;
        }}
        .section ul {{
            list-style: none;
            padding: 0;
        }}
        .section li {{
            padding: 8px 0;
            border-bottom: 1px solid #eee;
        }}
        .section li:last-child {{
            border-bottom: none;
        }}
        .section a {{
            color: #0066cc;
            text-decoration: none;
        }}
        .section a:hover {{
            text-decoration: underline;
        }}
        .stats {{
            background: #e8f4f8;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .quick-links {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .quick-link {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .quick-link a {{
            color: #003366;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>📚 Michigan Legal Knowledge Base</h1>
    
    <div class="stats">
        <strong>Statistics:</strong> 51 sections across 6 files, 84,298+ words, 546,898+ characters
    </div>
    
    <div class="quick-links">
        <div class="quick-link">
            <a href="#catalogue">📖 Catalogue</a>
            <div>Sections 1-52</div>
        </div>
        <div class="quick-link">
            <a href="#mcl">📜 MCL</a>
            <div>Michigan Compiled Laws</div>
        </div>
        <div class="quick-link">
            <a href="#mcr">⚖️ MCR</a>
            <div>Michigan Court Rules</div>
        </div>
        <div class="quick-link">
            <a href="#forms">📋 Forms</a>
            <div>SCAO Forms</div>
        </div>
    </div>
    
    <div class="section">
        <h2 id="catalogue">📖 Catalogue Navigation</h2>
        <p>The catalogue contains 51 sections organized into 6 files for optimal performance.</p>
        <ul>
"""
    
    # Add catalogue file links
    md_files = sorted(catalogue_dir.glob('*.md'))
    md_files = [f for f in md_files if f.name != 'INDEX.md']
    
    for md_file in md_files:
        stem = md_file.stem
        size = os.path.getsize(md_file)
        
        # Extract section range from filename
        if '-' in stem:
            start, end = stem.split('-')
            section_range = f"Sections {start}-{end}"
        else:
            section_range = f"Section {stem}"
        
        html_index += f"""            <li>
                <a href="{md_file.name}">{section_range}</a> 
                <span style="color: #666; font-size: 0.9em;">({size:,} bytes)</span>
            </li>
"""
    
    html_index += """        </ul>
    </div>
    
    <div class="section">
        <h2 id="mcl">📜 Michigan Compiled Laws (MCL)</h2>
        <p>Access MCL chapters and sections with direct links to official sources.</p>
        <ul>
            <li><a href="https://www.legislature.mi.gov/Laws/MCL">Official MCL Website</a></li>
            <li><a href="../michigancompiledlawsMBP/README.md">Local MCL Archive</a></li>
        </ul>
    </div>
    
    <div class="section">
        <h2 id="mcr">⚖️ Michigan Court Rules (MCR)</h2>
        <p>Access Michigan Court Rules organized by chapter.</p>
        <ul>
            <li><a href="https://www.courts.michigan.gov/rules-courts/">Official Court Rules</a></li>
        </ul>
    </div>
    
    <div class="section">
        <h2 id="forms">📋 SCAO Forms</h2>
        <p>State Court Administrative Office forms for all Michigan court procedures.</p>
        <ul>
            <li><a href="https://www.courts.michigan.gov/forms/">Official SCAO Forms</a></li>
        </ul>
    </div>
    
    <div class="section">
        <h2>🔍 Search & Indexes</h2>
        <ul>
            <li><a href="../search/catalogue_search_index.json">Search Index (JSON)</a></li>
            <li><a href="../catalogue/json/INDEX.json">JSON Index</a></li>
            <li><a href="../catalogue/bundle/catalogue_bundle.json">Full Bundle</a></li>
        </ul>
    </div>
    
    <div class="section">
        <h2>🚀 Optimization</h2>
        <ul>
            <li><a href="../OPTIMIZATION_MASTER_PLAN.md">Optimization Master Plan</a></li>
            <li><a href="../optimization/">Optimization Scripts</a></li>
        </ul>
    </div>
    
    <div class="section">
        <h2>📋 Development Roadmap</h2>
        <ul>
            <li><a href="../TODO_MASTER_INDEX.md">Master TODO Index</a></li>
            <li><a href="../TODO_MICHIGAN_TORTS.md">Torts Development</a></li>
            <li><a href="../TODO_COMPLAINTS_CLAIMS_LAWSUITS.md">Complaints & Claims</a></li>
            <li><a href="../TODO_DOCTRINE_CASELAW_SUPREME_COURT.md">Doctrine & Case Law</a></li>
        </ul>
    </div>
    
    <div class="section">
        <h2>🔗 Cross-Repository Navigation</h2>
        <p>Navigate across all Michigan Legal Knowledge Base repositories:</p>
        <ul>
            <li><strong>Michigan-MCLA:</strong> This repository - Catalogue, MCL, optimization</li>
            <li><a href="https://github.com/fatcrapinmybutt/MICHIGAN-HIGHER-COURTS">MICHIGAN-HIGHER-COURTS</a> - Supreme Court, COA, case law</li>
            <li><a href="https://github.com/fatcrapinmybutt/CourtRules">CourtRules</a> - Michigan Court Rules, forms, procedures</li>
            <li><a href="https://github.com/fatcrapinmybutt/fredprime-legal-system">fredprime-legal-system</a> - Core legal system architecture</li>
            <li><a href="https://github.com/fatcrapinmybutt/LitigationOS">LitigationOS</a> - Litigation operating system</li>
            <li><a href="https://github.com/fatcrapinmybutt/michigancompiledlawsMBP">michigancompiledlawsMBP</a> - MCL HTML archive</li>
        </ul>
    </div>
    
    <div class="section" style="text-align: center; color: #666;">
        <p>Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
        <p>Part of the Ω-CONVERGENCE MICHIGAN LEGAL INTELLIGENCE SINGULARITY</p>
    </div>
</body>
</html>"""
    
    # Write HTML index
    with open(nav_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html_index)
    
    print(f"HTML navigation index created: {nav_dir / 'index.html'}")
    print(f"File size: {os.path.getsize(nav_dir / 'index.html'):,} bytes")


def create_cross_repository_index():
    """Create a JSON index for cross-repository navigation."""
    nav_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/navigation')
    
    cross_repo_index = {
        'version': '1.0',
        'created': datetime.now(timezone.utc).isoformat(),
        'repositories': {
            'Michigan-MCLA': {
                'description': 'Primary repository with catalogue, MCL, optimization',
                'url': 'https://github.com/fatcrapinmybutt/Michigan-MCLA',
                'local_path': '/workspace/fatcrapinmybutt__Michigan-MCLA',
                'content': {
                    'catalogue': {
                        'description': '51 sections of Michigan legal catalogue',
                        'files': 6,
                        'path': 'catalogue/',
                        'formats': ['markdown', 'json', 'minified', 'compressed', 'bundle']
                    },
                    'mcl': {
                        'description': 'Michigan Compiled Laws archive',
                        'path': 'michigancompiledlawsMBP/',
                        'format': 'HTML'
                    },
                    'optimization': {
                        'description': 'Optimization scripts and plans',
                        'path': 'optimization/',
                        'scripts': ['split_catalogue_v3.py', 'convert_to_json.py', 'compress_json.py', 'create_navigation.py']
                    },
                    'navigation': {
                        'description': 'Navigation system',
                        'path': 'navigation/',
                        'files': ['index.html']
                    },
                    'search': {
                        'description': 'Search indexes',
                        'path': 'search/',
                        'files': ['catalogue_search_index.json']
                    }
                },
                'size_mb': 179,
                'files_count': 546
            },
            'MICHIGAN-HIGHER-COURTS': {
                'description': 'Michigan Supreme Court and Court of Appeals cases',
                'url': 'https://github.com/fatcrapinmybutt/MICHIGAN-HIGHER-COURTS',
                'local_path': '/workspace/fatcrapinmybutt__MICHIGAN-HIGHER-COURTS',
                'content': {
                    'supreme_court': {
                        'description': 'Michigan Supreme Court opinions and orders',
                        'path': 'supreme_court/',
                        'coverage': '2020-2024'
                    },
                    'court_of_appeals': {
                        'description': 'Michigan Court of Appeals opinions',
                        'path': 'court_of_appeals/',
                        'coverage': '2020-2024'
                    }
                }
            },
            'CourtRules': {
                'description': 'Michigan Court Rules and SCAO forms',
                'url': 'https://github.com/fatcrapinmybutt/CourtRules',
                'local_path': '/workspace/fatcrapinmybutt__CourtRules',
                'content': {
                    'mcr': {
                        'description': 'Michigan Court Rules',
                        'chapters': 8
                    },
                    'mre': {
                        'description': 'Michigan Rules of Evidence',
                        'articles': 11
                    },
                    'forms': {
                        'description': 'SCAO forms and templates',
                        'count': '100+'
                    }
                }
            },
            'fredprime-legal-system': {
                'description': 'Core legal system architecture',
                'url': 'https://github.com/fatcrapinmybutt/fredprime-legal-system',
                'local_path': '/workspace/fatcrapinmybutt__fredprime-legal-system',
                'content': {
                    'architecture': {
                        'description': 'Legal reasoning engine architecture'
                    },
                    'doctrine': {
                        'description': 'Legal doctrine framework'
                    }
                }
            },
            'LitigationOS': {
                'description': 'Litigation operating system',
                'url': 'https://github.com/fatcrapinmybutt/LitigationOS',
                'local_path': '/workspace/fatcrapinmybutt__LitigationOS',
                'content': {
                    'workflow': {
                        'description': 'Litigation workflow automation'
                    },
                    'templates': {
                        'description': 'Legal document templates'
                    }
                }
            },
            'michigancompiledlawsMBP': {
                'description': 'MCL HTML archive',
                'url': 'https://github.com/fatcrapinmybutt/michigancompiledlawsMBP',
                'local_path': '/workspace/fatcrapinmybutt__michigancompiledlawsMBP',
                'content': {
                    'html_archive': {
                        'description': 'Complete MCL in HTML format',
                        'chapters': '100+'
                    }
                }
            }
        },
        'navigation': {
            'by_topic': {
                'torts': {
                    'repositories': ['Michigan-MCLA', 'MICHIGAN-HIGHER-COURTS'],
                    'todo': '../TODO_MICHIGAN_TORTS.md'
                },
                'complaints_claims': {
                    'repositories': ['Michigan-MCLA', 'CourtRules'],
                    'todo': '../TODO_COMPLAINTS_CLAIMS_LAWSUITS.md'
                },
                'doctrine_caselaw': {
                    'repositories': ['MICHIGAN-HIGHER-COURTS', 'fredprime-legal-system'],
                    'todo': '../TODO_DOCTRINE_CASELAW_SUPREME_COURT.md'
                },
                'court_rules': {
                    'repositories': ['CourtRules', 'Michigan-MCLA'],
                    'primary': 'CourtRules'
                },
                'forms': {
                    'repositories': ['CourtRules', 'LitigationOS'],
                    'primary': 'CourtRules'
                }
            },
            'by_authority': {
                'binding': {
                    'description': 'BINDING_MICHIGAN authority level',
                    'sources': ['MCL', 'MCR', 'MRE', 'Michigan Supreme Court opinions']
                },
                'persuasive': {
                    'description': 'PERSUASIVE_MICHIGAN authority level',
                    'sources': ['Court of Appeals opinions', 'Federal district court opinions']
                },
                'secondary': {
                    'description': 'SECONDARY_MICHIGAN authority level',
                    'sources': ['AG opinions', 'Administrative rules']
                },
                'non_michigan': {
                    'description': 'NON_MICHIGAN authority level',
                    'sources': ['Federal law', 'Other state law']
                }
            }
        },
        'statistics': {
            'total_repositories': 6,
            'total_size_mb': 179,
            'total_files': 546,
            'total_documents': 9621,
            'catalogue_sections': 51,
            'catalogue_words': 84298,
            'catalogue_characters': 546898
        }
    }
    
    # Write cross-repository index
    with open(nav_dir / 'cross_repository_index.json', 'w', encoding='utf-8') as f:
        json.dump(cross_repo_index, f, indent=2, ensure_ascii=False)
    
    print(f"Cross-repository index created: {nav_dir / 'cross_repository_index.json'}")
    print(f"File size: {os.path.getsize(nav_dir / 'cross_repository_index.json'):,} bytes")


def create_quick_access_index():
    """Create a quick access index for common legal research tasks."""
    nav_dir = Path('/workspace/fatcrapinmybutt__Michigan-MCLA/navigation')
    
    quick_access = {
        'version': '1.0',
        'created': datetime.now(timezone.utc).isoformat(),
        'quick_start': {
            'new_case_research': {
                'description': 'Starting research for a new Michigan case',
                'steps': [
                    {
                        'step': 1,
                        'action': 'Identify jurisdiction and court type',
                        'resources': [
                            'CourtRules for procedural rules',
                            'MICHIGAN-HIGHER-COURTS for appellate cases'
                        ]
                    },
                    {
                        'step': 2,
                        'action': 'Research applicable statutes',
                        'resources': [
                            'Michigan-MCLA/catalogue for MCL sections',
                            'michigancompiledlawsMBP for HTML versions'
                        ]
                    },
                    {
                        'step': 3,
                        'action': 'Find relevant case law',
                        'resources': [
                            'MICHIGAN-HIGHER-COURTS for Supreme Court and COA opinions',
                            'TODO_DOCTRINE_CASELAW_SUPREME_COURT.md for case law database'
                        ]
                    },
                    {
                        'step': 4,
                        'action': 'Review court forms and procedures',
                        'resources': [
                            'CourtRules for SCAO forms',
                            'LitigationOS for templates'
                        ]
                    }
                ]
            },
            'tort_law_research': {
                'description': 'Researching Michigan tort law',
                'steps': [
                    {
                        'step': 1,
                        'action': 'Review tort law catalogue',
                        'resources': ['Michigan-MCLA/catalogue for existing sections']
                    },
                    {
                        'step': 2,
                        'action': 'Check TODO_MICHIGAN_TORTS.md for development plan',
                        'resources': ['TODO_MICHIGAN_TORTS.md']
                    },
                    {
                        'step': 3,
                        'action': 'Research specific tort types',
                        'resources': [
                            'MCL chapters on torts',
                            'Case law from MICHIGAN-HIGHER-COURTS'
                        ]
                    }
                ]
            },
            'complaint_drafting': {
                'description': 'Drafting a complaint or claim',
                'steps': [
                    {
                        'step': 1,
                        'action': 'Review complaint templates',
                        'resources': ['LitigationOS for templates']
                    },
                    {
                        'step': 2,
                        'action': 'Check SCAO forms requirements',
                        'resources': ['CourtRules for official forms']
                    },
                    {
                        'step': 3,
                        'action': 'Research applicable law',
                        'resources': [
                            'Michigan-MCLA for statutes',
                            'MICHIGAN-HIGHER-COURTS for case law'
                        ]
                    }
                ]
            }
        },
        'common_queries': {
            'find_statute': {
                'description': 'Find a specific Michigan statute',
                'methods': [
                    'Use catalogue sections for organized access',
                    'Search michigancompiledlawsMBP HTML archive',
                    'Check official MCL website'
                ],
                'links': [
                    '../catalogue/INDEX.md',
                    '../michigancompiledlawsMBP/README.md',
                    'https://www.legislature.mi.gov/Laws/MCL'
                ]
            },
            'find_case_law': {
                'description': 'Find Michigan case law on a topic',
                'methods': [
                    'Search MICHIGAN-HIGHER-COURTS repository',
                    'Use TODO_DOCTRINE_CASELAW_SUPREME_COURT.md for organized access',
                    'Check official court websites'
                ],
                'links': [
                    'https://github.com/fatcrapinmybutt/MICHIGAN-HIGHER-COURTS',
                    '../TODO_DOCTRINE_CASELAW_SUPREME_COURT.md',
                    'https://www.courts.michigan.gov/opinions_orders/'
                ]
            },
            'find_court_rule': {
                'description': 'Find a specific Michigan Court Rule',
                'methods': [
                    'Check CourtRules repository',
                    'Use official court rules website',
                    'Review MCR chapters'
                ],
                'links': [
                    'https://github.com/fatcrapinmybutt/CourtRules',
                    'https://www.courts.michigan.gov/rules-courts/'
                ]
            },
            'find_form': {
                'description': 'Find a specific SCAO form',
                'methods': [
                    'Check CourtRules repository forms directory',
                    'Use official SCAO forms website',
                    'Review LitigationOS templates'
                ],
                'links': [
                    'https://github.com/fatcrapinmybutt/CourtRules',
                    'https://www.courts.michigan.gov/forms/',
                    'https://github.com/fatcrapinmybutt/LitigationOS'
                ]
            }
        },
        'authority_hierarchy': {
            'level_1_binding': {
                'description': 'BINDING_MICHIGAN - Highest authority',
                'sources': [
                    'Michigan Constitution',
                    'Michigan Compiled Laws (MCL)',
                    'Michigan Court Rules (MCR)',
                    'Michigan Rules of Evidence (MRE)',
                    'Michigan Supreme Court opinions'
                ],
                'weight': 1.0
            },
            'level_2_persuasive': {
                'description': 'PERSUASIVE_MICHIGAN - Strong persuasive authority',
                'sources': [
                    'Michigan Court of Appeals opinions',
                    'Federal district court opinions applying Michigan law',
                    'Michigan Attorney General opinions'
                ],
                'weight': 0.8
            },
            'level_3_secondary': {
                'description': 'SECONDARY_MICHIGAN - Secondary authority',
                'sources': [
                    'Michigan administrative rules',
                    'Michigan jury instructions',
                    'Michigan practice manuals'
                ],
                'weight': 0.6
            },
            'level_4_non_michigan': {
                'description': 'NON_MICHIGAN - Non-binding authority',
                'sources': [
                    'Federal law (when not preempted)',
                    'Other state court opinions',
                    'Legal treatises and law review articles'
                ],
                'weight': 0.4
            }
        }
    }
    
    # Write quick access index
    with open(nav_dir / 'quick_access_index.json', 'w', encoding='utf-8') as f:
        json.dump(quick_access, f, indent=2, ensure_ascii=False)
    
    print(f"Quick access index created: {nav_dir / 'quick_access_index.json'}")
    print(f"File size: {os.path.getsize(nav_dir / 'quick_access_index.json'):,} bytes")


if __name__ == '__main__':
    print("=== Creating Navigation System ===")
    
    print("\n--- HTML Navigation ---")
    create_html_navigation()
    
    print("\n--- Cross-Repository Index ---")
    create_cross_repository_index()
    
    print("\n--- Quick Access Index ---")
    create_quick_access_index()
    
    print("\n=== Navigation system complete! ===")
    print("Files created in: /workspace/fatcrapinmybutt__Michigan-MCLA/navigation/")
