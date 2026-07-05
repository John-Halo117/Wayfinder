# Repository Governance Guide

Run architecture diagnostics before architecture-sensitive changes:

```bash
./wf doctor --write
./wf architecture check --write --fail-on-violations
```

Governance rules:

- Architecture docs define the canonical model.
- ADRs define evidence-backed decisions and must cite architecture sections.
- Code implements architecture and must not bypass canonical layers.
- Generated knowledge remains derived evidence.
- Candidate Pages require human review and are never auto-promoted.
- CI should run the architecture check in warning mode until legacy exceptions
  are intentionally classified.
