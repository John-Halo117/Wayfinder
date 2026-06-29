# Host Shell

Host Shell owns interaction runtime routing. It decides which local workspace provider receives an explicit interaction request, then returns the provider response to the caller.

Host Shell does not own truth. It does not write ARK observations, mutate canonical memory, manage inventory, decide bearings, or define constitutional logic. Provider output returns a `ProvenanceRecord` with `canonical=False` and remains non-canonical unless another owner validates and promotes it through the proper evidence path.

Host Shell responses are not candidate observations or candidate artifacts. Promotion must go through `artifact_promotion.CandidateArtifact` and a later explicit promotion decision. This package performs no ARK writes.

## Adapter vs Provider

`external/odysseus` is the low-level reversible adapter. It knows how to call an Odysseus server safely.

`host_shell/providers/odysseus.py` is the Host Shell provider. It maps `HostShellRequest` to `OdysseusPromptRequest`, delegates to the adapter, preserves the reusable `ProvenanceRecord`, and keeps `canonical=False`.

This distinction keeps Odysseus replaceable. Odysseus is the first Host Shell provider, not a permanent Wayfinder dependency.

## Configuration

```bash
HOST_SHELL=none
```

disables Host Shell network use.

```bash
HOST_SHELL=odysseus
ODYSSEUS_ENABLED=true
ODYSSEUS_BASE_URL=http://127.0.0.1:7000
ODYSSEUS_TIMEOUT_SECONDS=5
```

selects Odysseus as the provider. No network call happens during provider construction. Network calls only occur when `health()` or `send()` is invoked, and those calls are delegated through the Odysseus adapter.
