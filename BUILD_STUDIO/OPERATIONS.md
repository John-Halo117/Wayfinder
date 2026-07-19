# Build Bible Studio Operations

## Production Posture

Build Bible Studio is a local-first engineering IDE. It should normally bind to
`127.0.0.1` and read canonical source from the local Git workspace.

## Start

```bash
python3 BUILD_STUDIO/studio_server.py --host 127.0.0.1 --port 8765
```

## Health Check

```bash
python3 - <<'PY'
from urllib.request import urlopen
print(urlopen("http://127.0.0.1:8765/api/health").read().decode())
PY
```

## Platform Check

```bash
python3 - <<'PY'
from urllib.request import urlopen
print(urlopen("http://127.0.0.1:8765/api/platform").read().decode()[:1000])
PY
```

## Preflight

```bash
python3 BUILD_STUDIO/studio_server.py --check
python3 -m unittest discover -s BUILD_STUDIO/tests
./aurora validate --format json
```

## CLI Contract Check

```bash
./aurora catalog --format table
./aurora search "Room Spine" --format json
./aurora graph dependencies --format graph
```

## Configuration

The server accepts:

- `--repo-root`: repository root to index.
- `--source-root`: source root to index; repeatable.
- `--max-files`: maximum indexed text files.
- `--max-file-bytes`: maximum bytes read per file.
- `--max-search-results`: maximum returned search results.
- `--max-graph-nodes`: maximum graph nodes.
- `--cache-ttl`: index cache TTL in seconds.
- `--debug`: include traceback context in structured API errors.

## Data Ownership

- Canonical engineering source remains in `BUILD_BIBLE/` and
  `BUILD_OPERATIONS/`.
- Property repositories remain independent Git repositories when added.
- Studio cache is in memory only.
- Studio does not write canonical files in this version.
- Git remains the history and review mechanism.

## P6 Service Boundaries

- RepositoryService discovers repositories; it does not merge them.
- WorkspaceService stores only layout and preferences.
- InstantiationService previews pattern instantiation; it does not write files.
- CompilerService orchestrates pipeline stages; backends are replaceable.
- AIService exposes provider-independent slots; no provider is active by
  default.
- Jarvis uses public Studio APIs as an unprivileged engineering client.
- PluginService exposes stable extension slots; plugins receive no privileged
  access.

## P7 CLI-Over-GUI Boundary

- `aurora_core.py` owns command dispatch.
- `aurora_cli.py` owns command-line parsing and output rendering.
- `studio_server.py` adapts HTTP routes to Aurora commands.
- Browser code renders command results and manages presentation state.
- Future clients should call the CLI contract instead of duplicating
  engineering logic.

## Failure Model

API failures use:

```json
{
  "status": "error",
  "error_code": "STRING",
  "reason": "STRING",
  "context": {},
  "recoverable": true
}
```

## Security Boundary

- Static files are served only from `BUILD_STUDIO/static/`.
- Document reads are restricted to configured source roots.
- Content Security Policy, `nosniff`, and `no-referrer` headers are emitted.
- No external network API is required.
