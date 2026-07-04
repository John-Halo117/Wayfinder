# Retrieval Validation

Validation reports issues without repairing indexes silently.

Detected issues include:

- missing indexes
- stale index manifest
- broken index references
- orphaned index entries
- deterministic embedding drift
- missing provenance
- invalid query limits
- empty queries
- document limits

## Ranking

Every retrieval result records per-index ranking contributions and a short reason
for each contribution.

## Reproducibility

Index manifests include a content hash over promoted knowledge projections.
Deleting and rebuilding with the same promotions produces equivalent retrieval
ordering and manifest content hashes.
