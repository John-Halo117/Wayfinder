# Repository Health Dashboard

Status: `pass`
Architecture Health Score: `55`

## Health Summary

| Metric | Value |
| --- | --- |
| Dependency | `8` fields |
| Repository | `10` fields |
| Documentation | `10` fields |
| Capability | `9` fields |
| Oracle | `3` fields |
| Reality | `2` fields |
| Representation | `6` fields |
| Knowledge | `5` fields |
| Mission | `4` fields |
| Navigation | `4` fields |
| Views | `5` fields |
| Actions | `5` fields |

## Findings

| Severity | Code | Path | Message |
| --- | --- | --- | --- |
| warning | `ARCHITECTURAL_DRIFT_LAYER_BYPASS` | `` | New or existing modules bypass canonical layer direction. |
| warning | `DUPLICATE_HASH_GROUPS` | `` | Duplicate tracked file hashes detected. |
| warning | `LAYER_SHORTCUT` | `engines/interpretation/knowledge_governance/engine.py` | Upstream layer imports downstream layer. |
| warning | `LAYER_SHORTCUT` | `engines/interpretation/knowledge_governance/models.py` | Upstream layer imports downstream layer. |
| warning | `LAYER_SHORTCUT` | `engines/interpretation/knowledge_governance/repository.py` | Upstream layer imports downstream layer. |
| warning | `LAYER_SHORTCUT` | `engines/interpretation/tests/test_knowledge_governance.py` | Upstream layer imports downstream layer. |
| warning | `LAYER_SHORTCUT` | `engines/views/knowledge_retrieval/store.py` | Upstream layer imports downstream layer. |
| warning | `LAYER_SHORTCUT` | `engines/views/tests/test_knowledge_retrieval.py` | Upstream layer imports downstream layer. |
| warning | `LAYER_SHORTCUT` | `engines/views/tests/test_knowledge_retrieval.py` | Upstream layer imports downstream layer. |
