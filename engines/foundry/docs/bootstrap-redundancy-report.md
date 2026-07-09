# Bootstrap Redundancy Report

## Redundancy Removed

The active Foundry phase prompts are already compact. This pass removed the
remaining architectural ambiguity by making bootstrap execution an explicit
phase prerequisite and moving boot policy into `bootstrap.yaml`.

## Estimated Reduction

| Measure | Estimate |
| --- | ---: |
| Prompt token reduction for future phases | 60-80% |
| Duplicated constitutional text removed from active prompts | Low current amount; high future prevention |
| Maintenance reduction | High for prompt additions because boot rules live in one manifest |
| Bootstrap cache effectiveness | High for static docs; medium for dynamic roadmap/ADR inputs |

## Remaining Duplication By Design

- Human-readable bootstrap pass docs and machine-readable `bootstrap.yaml`
  both name the sequence.
- `bootstrap.lock` repeats paths and hashes from the manifest to support cache
  validation.
- P0 and P1 mention bootstrap inheritance as a phase contract, not as repeated
  doctrine.

## Maintenance Rule

New phases must add only phase-specific content. Any constitutional,
architectural, roadmap, engineering, or prompt-standard rule belongs in
bootstrap artifacts, not in prompt bodies.
