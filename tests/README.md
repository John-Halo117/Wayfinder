# Tests

Repository-level tests validate architectural integrity, dependency direction,
contract compatibility, failure paths, and proof-promotion boundaries.

Engine-specific tests live inside each engine.

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
