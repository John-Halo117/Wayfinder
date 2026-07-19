# Recursive Factorization Report

| Pattern | Shared portion | Unique portions | Further decomposition observation | Confidence |
| --- | --- | --- | --- | --- |
| Policy surfaces | Rule language, policy evaluation, policy provenance. | Contract docs, service scaffold, legacy runtime evaluator, JSON policy sets. | Separate policy vocabulary, evaluation runtime, storage, and operations use. | High |
| Storage surfaces | Durable persistence boundary, artifact/reference storage, replay support. | Service scaffold, ARK ingestion local storage, legacy Duck/Rust/Python storage. | Separate storage contract, service proof, ARK preservation dependency, legacy backends. | High |
| Event surfaces | Event schema, append/replay, routing. | Event bus service, ARK ingestion events, legacy schemas. | Separate event contract, event service, engine event producers. | High |
| Forge/Foundry surfaces | Engineering change with proof, prompts, runtime artifacts, UI/launcher compatibility. | ARK legacy Forge, Foundry legacy Forge, bootstrap docs, prompts. | Separate alias compatibility, prompt compiler passes, runtime execution, UI launchers. | High |
| Search/retrieval surfaces | Querying derived records and preserving provenance expansion. | Knowledge retrieval engine, Knowledge/search DBs, export mining indexes. | Separate retrieval index, view models, generated graph search, source expansion. | Medium |
| External adapters | Source-specific acquisition and provider boundaries. | ChatGPT Oracle, legacy emitters, legacy integrations, external placeholder. | Separate observation source, compatibility adapter, provider runtime, canonical contract. | Medium |
| Governance artifacts | Validation, drift, promotion, readiness, reports. | Docs/governance, Foundry P0-P3 artifacts, tooling doctor. | Separate human report, machine check, promotion evidence, readiness gate. | Medium |

## Stop Condition

Factorization stops at documented shared/unique boundaries. P3 does not convert
these observations into extraction tasks.
