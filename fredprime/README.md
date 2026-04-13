# fredprime – Python Legal Automation Toolkit

This directory contains the Python legal automation toolkit originally developed
in the **fredprime-legal-system** repository. It has been merged into this
unified Michigan-MCLA repository to consolidate all Michigan court-related
tooling in one place.

## Contents

| File | Description |
|---|---|
| `forms_manifest.json` | Manifest of court forms with associated rules, statutes, and benchbook references |
| `benchbook_loader.py` | Utility for extracting text from benchbook PDFs (requires `pypdf`) |
| `complaint_generator.py` | Federal complaint DOCX generator (requires `python-docx`) |
| `motion_generators.py` | Michigan motion DOCX generators (requires `python-docx`) |
