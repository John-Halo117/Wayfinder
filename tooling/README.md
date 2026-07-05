# Tooling

Tooling is for developer tooling only.

Examples include scaffolding, code generation, SDKs, plugins, migration tools,
benchmarking, profiling, formatting, and linting.

## Architecture Intelligence

Run repository governance diagnostics with:

```bash
./wf doctor --write
./wf architecture check --write
```

The command scans tracked repository evidence, reports architectural drift,
generates Mermaid and Graphviz architecture graphs, and writes governance
dashboards under `docs/governance/`.
