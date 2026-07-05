# 21 Roadmap

This roadmap is incremental. It preserves existing functionality and avoids
rewrites.

## Phase 1: Generated And Legacy Surface Clarity

- Goal: make generated, legacy, canonical, and transitional surfaces obvious.
- Benefit: reduces accidental edits and ownership confusion.
- Risks: documentation drift.
- Required ADRs: ADR-0010.
- Breaking changes: none.
- Compatibility strategy: keep all current paths.
- Rollback: revert docs only.
- Effort: small.

## Phase 2: Storage Service Stage 2 Proof

- Goal: implement minimal backend-neutral Storage service proof.
- Benefit: reduces duplicated persistence semantics.
- Risks: over-abstracting before consumers.
- Required ADRs: ADR-0007.
- Breaking changes: none.
- Compatibility strategy: no consumer rewiring in first proof.
- Rollback: remove service proof; legacy local storage remains.
- Effort: medium.

## Phase 3: Candidate Pages

- Goal: support bounded governance intake at export scale.
- Benefit: reviewability and deterministic replay.
- Risks: page semantics could obscure candidate identity if designed poorly.
- Required ADRs: ADR-0005, ADR-0009.
- Breaking changes: none if existing candidate APIs remain.
- Compatibility strategy: accept both candidates and pages during migration.
- Rollback: disable page intake.
- Effort: medium.

## Phase 4: Configuration Service Stage 2 Proof

- Goal: centralize loading, precedence, validation, and redaction.
- Benefit: reduces duplicated config behavior.
- Risks: accidental secret exposure if redaction is weak.
- Required ADRs: future Configuration proof ADR if behavior changes.
- Breaking changes: none in proof.
- Compatibility strategy: no engine rewiring until parity tests exist.
- Rollback: retain legacy loaders.
- Effort: medium.

## Phase 5: Policy Service Stage 2 Proof

- Goal: centralize deterministic rule evaluation and explanations.
- Benefit: prepares promotion/tool/action gates.
- Risks: policy vocabulary could overlap permissions.
- Required ADRs: future Policy proof ADR.
- Breaking changes: none in proof.
- Compatibility strategy: adapter tests before consumer migration.
- Rollback: keep legacy policy engines.
- Effort: medium.

## Phase 6: Compatibility Layer

- Goal: isolate external integrations and provider SDKs.
- Benefit: preserves replaceability.
- Risks: adapter churn.
- Required ADRs: ADR-0008.
- Breaking changes: none if aliases remain.
- Compatibility strategy: parity tests and legacy shims.
- Rollback: restore legacy entry points.
- Effort: medium-large.

## Phase 7: Media Graph Program

- Goal: unify music, movies, TV, books, games, podcasts, photos, video,
  documents, and GIS as asset/representation/network views.
- Benefit: supports playlists, mixed-media experiences, capsules, timelines,
  collages, and maps.
- Risks: media-specific pipelines could become architecture owners.
- Required ADRs: future Media Graph ADR.
- Breaking changes: none during planning.
- Compatibility strategy: media adapters feed universal ingestion.
- Rollback: keep media-specific adapters without promoting them.
- Effort: large.

## Phase 8: Dependency Linter

- Goal: enforce architecture rules automatically.
- Benefit: catches drift before it becomes debt.
- Risks: false positives if legacy/generated exceptions are not modeled.
- Required ADRs: none unless enforcement blocks CI.
- Breaking changes: initially warning-only.
- Compatibility strategy: classify exceptions.
- Rollback: warning-only mode.
- Effort: small-medium.

## ADR Recommendations

- Accepted/proposed current: ADR-0001 through ADR-0010.
- Future ADRs likely needed:
  - Storage minimal implementation proof.
  - Configuration minimal implementation proof.
  - Policy minimal implementation proof.
  - Media Graph as derived representation network.
  - Dependency linter enforcement policy.

