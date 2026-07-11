# Internal Applications

Internal applications are owned by Wayfinder.

Examples include API, CLI, desktop, mobile, web, workers, and automation.

Applications depend on domains, engines, services, and contracts through
explicit interfaces.

## Foundry

Foundry is the canonical Wayfinder engineering app surface. It is exposed from
the root `wf` launcher:

- `./wf foundry` starts the browser app.
- `./wf foundry --status` checks whether the app is running.
- `./wf foundry --stop` stops the recorded app process.
- `./wf foundry-cli` runs the preserved engineering runtime directly.

The current implementation delegates to the preserved Foundry legacy runtime
under `engines/foundry/legacy/` while keeping Forge-named files as compatibility
aliases only.
