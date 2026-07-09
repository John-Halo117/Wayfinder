# Bootstrap Migration Summary

## Summary

Foundry now has a deterministic bootstrap entry point.

The boot specification makes bootstrap the canonical source of Foundry's
worldview. Prompts consume bootstrap artifacts instead of carrying
constitutional context directly.

## Added

- `engines/foundry/bootstrap/bootstrap.yaml`
- `engines/foundry/bootstrap/bootstrap.lock`
- Bootstrap validation report
- Bootstrap migration summary
- Bootstrap redundancy report

## Updated

- Prompt dependency graph now starts at Bootstrap.
- P0 and P1 prompts explicitly require bootstrap.
- Prompt standard remains artifact-first and nine-section-only.

## Preserved

- Constitutional doctrine.
- Engineering intent.
- Runtime behavior.
- Existing bootstrap documents.
- Existing P0/P1 discovery artifacts.

## Migration Effect

Bootstrap becomes the first read path for Foundry sessions. Later phases inherit
bootstrap artifacts and should not rediscover constitutional, vocabulary,
architecture, roadmap, engineering, or prompt-standard material.
