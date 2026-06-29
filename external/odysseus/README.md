# Odysseus Workspace Adapter

Odysseus is integrated as an optional UI/agent workspace adapter. It may receive a bounded prompt from Jarvis-facing code and return a bounded response tagged with a reusable noncanonical `ProvenanceRecord`.

## Allowed

- Check Odysseus availability through `GET /api/health`.
- Send one explicit prompt to Odysseus through `POST /api/chat`.
- Return the response to Jarvis with optional `ProvenanceRecord` where `canonical=false`.
- Remain disabled unless `ODYSSEUS_ENABLED=true`.

## Not Allowed

- Odysseus must not own Wayfinder reality, navigation, inventory, bearings, constitutional logic, or source-of-truth state.
- Odysseus must not write ARK evidence or canonical memory through this adapter.
- Odysseus must not run hidden network calls; only `health()` and `send_prompt()` call the configured base URL.
- Odysseus output is workspace context until another owner explicitly validates and promotes evidence.

## Jarvis Boundary

Jarvis may use the `Odysseus Workspace` capability as a replaceable workspace route. Jarvis remains responsible for navigation decisions and route posture. ARK remains responsible for evidence and observation preservation. Wayfinder remains responsible for reality/navigation architecture.

## Local Run

Clone and start Odysseus separately:

```bash
git clone https://github.com/pewdiepie-archdaemon/odysseus.git
cd odysseus
cp .env.example .env
docker compose up -d --build
```

Then configure Wayfinder:

```bash
ODYSSEUS_ENABLED=true
ODYSSEUS_BASE_URL=http://127.0.0.1:7000
ODYSSEUS_TIMEOUT_SECONDS=5
```

Odysseus chat calls require an existing Odysseus session id. The adapter does not create sessions, mutate memory, or manage Odysseus workspace state beyond the explicit prompt call.
