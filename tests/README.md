# Testing Organization

This directory is reserved for future validation tests.

Expected future validation areas:

- mission and ownership conformance;
- semantic artifact compatibility;
- dependency vocabulary;
- no runtime dependency on ecosystem repositories;
- no consumer semantic forks;
- Commons publication handoff;
- ARK evidence boundary;
- Observatory telemetry boundary;
- governance and ADR/RFC traceability.

No executable tests are present in this skeleton.

## Workspace Membrane

`tests/integration/test_workspace_membrane.py` verifies the complete
noncanonical workspace pipeline:

```text
JarvisHostShellBridge
→ HostShellRegistry
→ OdysseusHostShellProvider (mocked)
→ HostShellResponse
→ CandidateArtifact
→ PromotionDecision
→ AdmissionCandidate
```

The membrane test proves that workspace output can move into review contracts
without becoming canonical reality, creating observations, writing ARK, opening
persistence handles, or contacting a live Odysseus instance.
