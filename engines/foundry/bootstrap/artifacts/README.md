# Bootstrap Artifacts

Bootstrap artifacts are immutable within a Foundry session. Later phases inherit
them instead of rediscovering or restating their content.

## Artifact Set

| Artifact | Source pass |
| --- | --- |
| Constitutional Model | `02_CONSTITUTION` |
| Concept Inventory | `02_CONSTITUTION`, `04_VOCABULARY` |
| Vocabulary | `04_VOCABULARY` |
| Layer Model | `05_ARCHITECTURE` |
| Dependency Model | `05_ARCHITECTURE`, `06_ROADMAP` |
| Traceability Model | `07_ENGINEERING` |
| Engineering Rules | `07_ENGINEERING` |
| Prompt Rules | `08_PROMPT_STANDARD` |
| Confidence Report | All bootstrap passes |
