# ADR-0004: Keep Private Validation Outputs Local

Status: Accepted

Date: 2026-07-03

## Context

First Contact generated large source-derived outputs, including preserved
artifacts, observation streams, relationship streams, replay outputs, and
reports. These may contain private source material.

## Decision

Private validation outputs stay local and are ignored by Git. Only
privacy-safe aggregate reports belong in the repository.

## Consequences

- `.wayfinder-validation/` remains ignored.
- Reports under `docs/` must avoid raw private content and generated payloads.
- Future validation work must preserve local-first and privacy-first defaults.

## Evidence

- `.gitignore` includes `.wayfinder-validation/`.
- First Contact Oracle output directory was about 1.3 GB and included raw
  preserved export artifacts.

## Rollback

Rollback only if a future repository policy defines a secure encrypted artifact
store with explicit consent and retention rules.
