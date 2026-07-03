# Artifact Promotion

Artifact promotion is a membrane between runtime output and durable truth.

`create_candidate_from_runtime_response(...)` can convert a noncanonical Execution Runtime response into a `CandidateArtifact` for review. It requires provenance and rejects canonical provenance because runtime output is workspace material, not ARK evidence.

`create_candidate_from_host_response(...)` remains as a compatibility wrapper.

`review_candidate(...)` records a review decision: `accepted`, `rejected`, or `needs_review`.

Acceptance is not persistence. An accepted `PromotionDecision` does not create an observation, does not write ARK, and does not make content canonical. ARK admission will be a later separate step with its own evidence and observation rules.

This package performs no autonomous execution, no network calls, and no storage writes.
