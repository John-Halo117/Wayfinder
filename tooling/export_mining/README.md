# Export Mining Tooling

`mine_wayfinder_export.py` deterministically mines historical ChatGPT export
JSON into a provenance-backed Wayfinder knowledge base.

It is archival tooling, not a new engine. The tool does not summarize with AI,
generate embeddings, perform retrieval, promote facts into governance, or copy
raw export payloads into the repository.

## Outputs

- `Knowledge/manifest.json`: deterministic import inventory and source hashes.
- `Knowledge/Graph/facts/index.json`: extracted facts with conversation/message provenance.
- `Knowledge/Graph/concepts.json`: stable concept nodes.
- `Knowledge/Graph/relationships/index.json`: evidence-backed graph edges.
- `Knowledge/*/README.md`: concise generated documentation views.

## Low-Token Reruns

Put source paths in a text file and pass it with `--input-manifest`:

```bash
python3 -m tooling.export_mining.mine_wayfinder_export \
  --input-manifest .wayfinder-validation/export-mining/source-files.txt \
  --output Knowledge
```

Graph records are written in chunks so large exports do not create a single
huge JSON file.

## Privacy Boundary

Generated source inventories include file names, sizes, artifact classes, and
hashes. They intentionally omit absolute local source paths.
