# Host Groundskeeper Engine

## Responsibility

Host Groundskeeper provides the initial host observation reference behavior for Wayfinder.

## Lifecycle

The Windows adapter runs bounded observation passes through PowerShell and Task Scheduler. It writes every material decision to Windows Event Log and publishes JSONL observations for the Wayfinder telemetry pipeline to ingest.

This layer does not optimize CPU, GPU, power plans, applications, storage, or memory. It preserves host reality only.

## Health

The engine exposes `HostGroundskeeperModule.health()`, which reports lifecycle state, registered plugin count, registered subscription count, and metric status.

## Windows Reference Adapter

`scheduler/HostGroundskeeper.Observer.ps1` supports:

- `-Mode Install`
- `-Mode RunOnce`
- `-Mode Uninstall`

The script observes CPU, GPU counters when available, memory, storage free space, foreground process, process snapshot deltas, active power plan, and Windows state placeholders without modifying system configuration.

## Recommendation Engine

`core/recommendations.py` consumes bounded `HostObservation` batches and emits advisory-only `HostRecommendation` records. Recommendations include ID, confidence, estimated benefit, estimated cost, supporting observations, expected capability impact, and explanation.

The engine does not execute recommendations, change Windows settings, modify power plans, schedule work, optimize resources, or learn from history.
