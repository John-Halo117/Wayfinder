# Governance Validation Rules

Knowledge Governance reports validation issues instead of silently repairing
state.

Detected issues include:

- missing provenance
- duplicate promotions
- invalid review transitions
- missing review history
- invalid promotion targets
- orphaned candidates
- broken supersession references
- promotion loops
- missing reviewer
- missing rationale
- missing rollback
- repository limits
- target repository mismatch

## Events

Governance emits deterministic event records:

- CandidateCreated
- CandidateUpdated
- CandidateGrouped
- CandidateApproved
- CandidateRejected
- CandidateDeferred
- CandidateMerged
- CandidatePromoted
- CandidateSuperseded

Events are audit records in this phase. They do not perform side effects beyond
the in-memory proof repository.
