# ADR-0005: Page Governance Candidate Intake

Status: Accepted

Date: 2026-07-03

## Context

First Contact produced 250,000 compiler candidates and hit the configured
compiler cap. Governance then rejected intake because the repository cap was
100,000 candidates.

## Decision

Governance intake for real export-scale compiler output must be bounded by
Candidate Pages or equivalent grouped pages. Paging must preserve candidate
identity, provenance, confidence, uncertainty, and deterministic replay.

## Consequences

- The Knowledge Compiler remains proposal-only.
- Knowledge Governance remains human-reviewed and bounded.
- Future implementation work should add page intake before larger private
  review workflows.

## Evidence

- Compiler candidate cap reached at 250,000.
- Governance candidate cap reached at 100,000.
- `docs/first-contact/evidence-assimilation.md`.

## Rollback

Rollback only if compiler precision improvements reduce real export candidate
volume below bounded governance intake limits.
