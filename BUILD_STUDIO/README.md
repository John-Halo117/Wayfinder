# Build Bible Studio

Build Bible Studio is the first local engineering IDE for the Build Bible.

The Studio does not own canonical engineering data. It reads Build Bible source
from `BUILD_BIBLE/` and operations source from `BUILD_OPERATIONS/`, builds a
live in-memory index, and exposes explorer, search, graph, validation, review,
compiler, digital twin, and Git views.

P6 evolves the Studio into Aurora Studio's first service-oriented engineering
platform surface. It exposes repository registry, workspace, property,
instantiation, event bus, compiler pipeline, plugin, AI, Jarvis, and Git
interfaces without making the Studio the owner of canonical data.

P7 makes the command-line interface the stable execution contract. The GUI
server invokes Aurora commands and returns their structured results; the
browser renders those results and keeps business logic out of the presentation
layer.

## Run

```bash
python3 BUILD_STUDIO/studio_server.py --host 127.0.0.1 --port 8765
```

Open:

```text
http://127.0.0.1:8765/
```

## Preflight

```bash
python3 BUILD_STUDIO/studio_server.py --check
python3 -m unittest discover -s BUILD_STUDIO/tests
./aurora health --format json
```

## Architecture

- `aurora_core.py`: canonical command contract and command dispatcher.
- `aurora_cli.py`: command-line parser and output renderers.
- `../aurora`: repository-local executable.
- `studio_server.py`: local HTTP server, repository services, and thin API adapter.
- `static/index.html`: IDE shell.
- `static/styles.css`: docked engineering UI.
- `static/app.js`: client-side workspace, search, graph, validation, and views.
- `tests/`: standard-library unit tests.
- `OPERATIONS.md`: local production runbook.

## Boundaries

- Canonical data remains in `BUILD_BIBLE/` and `BUILD_OPERATIONS/`.
- Studio index state is in memory only.
- Compiler outputs are planned manifests in this phase.
- No external services, network APIs, or AI providers are required.
- API errors use the Build Bible structured failure model.
- Document reads are restricted to configured source roots.
- Static serving is restricted to `BUILD_STUDIO/static/`.
- The server emits basic browser security headers.

## Service Model

The command path is:

```text
GUI / REST / scripts / Jarvis
        |
        v
Aurora command contract
        |
        v
Aurora services
        |
        v
Git-backed repositories
```

- Repository Service: reads source files.
- Parser: extracts titles, headings, links, metadata, and text.
- Schema Service: parses JSON schemas.
- Validation Service: checks references, README coverage, schema syntax, and
  basic layer boundaries.
- Knowledge Graph: builds document nodes and relationship edges.
- Search Engine: full-text and lightweight metadata search.
- Compiler: reports future compiler targets and readiness states.
- Git Integration: reads `git status --short`.
- AI Gateway and Plugin Manager: declared as extension surfaces, not provider
  implementations.
- Repository Registry: discovers local repositories and their relationships.
- Workspace Service: describes local workspace layout and preferences.
- Property Service: models property repository object types and navigation.
- Instantiation Service: previews pattern-to-specification workflows without
  writing canonical files.
- Event Bus: records bounded in-memory platform events.
- Jarvis Interface: declares future unprivileged engineering-client APIs.

## CLI

The canonical executable is:

```bash
./aurora
```

Examples:

```bash
./aurora search "Room Spine"
./aurora query "show every wet room"
./aurora validate
./aurora lint
./aurora graph dependencies --format graph
./aurora instantiate BUILD_BIBLE/doctrine/README.md --property property-local
./aurora compile property
./aurora report architecture
./aurora review repository
./aurora property list
./aurora workspace open homestead
```

Supported output modes are `json`, `human`, `yaml`, `markdown`, `table`, and
`graph`. JSON is the stable machine contract for future clients.

## Configuration

```bash
python3 BUILD_STUDIO/studio_server.py \
  --repo-root . \
  --source-root BUILD_BIBLE \
  --source-root BUILD_OPERATIONS \
  --max-files 2500 \
  --max-file-bytes 750000 \
  --cache-ttl 2
```

See [OPERATIONS.md](OPERATIONS.md) for runbook details.

## API Surfaces

- `/api/platform`
- `/api/repositories`
- `/api/workspace`
- `/api/property`
- `/api/instantiate/preview`
- `/api/compiler`
- `/api/compiler/run`
- `/api/digital-twin`
- `/api/plugins`
- `/api/ai`
- `/api/jarvis`
- `/api/events`
- `/api/git/branches`
- `/api/git/log`
- `/api/cli?command=search&query=Room%20Spine`
