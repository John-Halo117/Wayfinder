# First Contact Consolidation Validation Report

Date: 2026-07-03
Branch: `validation/chatgpt-export-first-contact`
Milestone: `v0.2-first-contact`

## Scope

Validation covered Phase 8C constitutional, ontology, glossary, contract,
documentation, ADR, and additive provenance-schema changes.

## Commands

```bash
python3 -m pytest -s engines/ark/tests/test_chatgpt_oracle.py engines/ark/tests/test_reality_ingestion.py engines/interpretation/tests/test_knowledge_compiler.py engines/interpretation/tests/test_knowledge_governance.py engines/views/tests/test_knowledge_retrieval.py engines/views/tests/test_knowledge_views.py services/identity/tests/test_identity_service.py services/event-bus/tests/test_event_bus_service.py
python3 -m compileall engines/ark/ingress/chatgpt_oracle engines/ark/ingress/reality_ingestion engines/interpretation engines/views services/identity services/event-bus
python3 - <<'PY'
from pathlib import Path
import re, sys
missing=[]
for path in Path('.').rglob('*.md'):
    s=path.as_posix()
    if s.startswith('.git/') or s.startswith('.wayfinder-validation/') or '/legacy/' in s or '/docs/source/' in s:
        continue
    text=path.read_text(encoding='utf-8', errors='replace')
    for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)', text):
        target=match.group(1).split('#',1)[0]
        if not target or re.match(r'^[a-z]+:', target) or target.startswith('mailto:') or target.startswith('/'):
            continue
        if not (path.parent / target).resolve().exists():
            missing.append((s, target))
if missing:
    for item in missing:
        print(f'{item[0]} -> {item[1]}')
    sys.exit(1)
print('markdown_links_ok')
PY
```

## Results

| Check | Result |
| --- | --- |
| Focused tests | 47 passed |
| Compile validation | Passed |
| Markdown link validation | `markdown_links_ok` |
| Raw private validation outputs committed | No |
| Runtime behavior changed | Additive provenance fields only |

## Residual Risk

- Markdown link validation intentionally skipped legacy folders and folded
  source docs.
- Candidate paging and streamable event publication remain documented future
  work, not implemented behavior.
- `v0.2-first-contact` should point at the clean Phase 8C consolidation
  checkpoint.
