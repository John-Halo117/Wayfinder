# Knowledge Compiler Architecture

## Boundary

The Knowledge Compiler belongs to Interpretation. It consumes ARK-preserved
observations and emits candidate knowledge artifacts.

It does not:

- ingest external source files
- preserve reality
- mutate observations
- mutate provenance
- generate RIDs
- update LVR
- promote truth
- search, embed, navigate, or build a knowledge graph

## Pipeline

```text
Preserved Observation
  -> contract validation
  -> text extraction from preserved raw observation payloads
  -> deterministic rule families
  -> novelty / duplicate / contradiction checks
  -> confidence and uncertainty assignment
  -> candidate artifacts with provenance
```

## Inputs

- `PreservedObservationRecord` from ARK reality ingestion
- mapping-shaped equivalents of preserved ARK records
- optional preserved explicit relationships
- optional known-term, deprecated-term, and ownership baselines

## Outputs

- `CompilerResult`
- proposed `CandidateArtifact` records
- `CompilerValidationIssue` records

All outputs are proposed and reviewable. None are canonical truth.

## First Contact Intake Boundary

The compiler may produce more candidates than one governance repository can
accept. Candidate output must therefore be treated as a bounded stream or set
of Candidate Pages before governance intake. Grouping and paging are
presentation and intake controls only; they must not alter candidate meaning or
provenance.
