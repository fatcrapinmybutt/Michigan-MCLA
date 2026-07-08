# Optimization Scripts and Standards

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
- Created: 2026-07-08 20:26:35 UTC
- Part of: Ω-CONVERGENCE MICHIGAN LEGAL INTELLIGENCE SINGULARITY
