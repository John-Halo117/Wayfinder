# 10 Capability Registry

Capabilities are stable architectural verbs; implementations are replaceable.
The Capability Registry is the future inventory of available providers,
implementations, constraints, and proofs for those verbs.

## Owns

- Capability names.
- Provider options.
- Availability evidence.
- Capability dependency graph.

## Does Not Own

- Navigation decisions.
- Provider-specific adapters.
- Engine-specific implementation behavior.

## Capability Health

Current state:

- `capabilities/README.md` exists.
- `contracts/capabilities/README.md` exists.
- NOMAD is named as discovery owner.
- No mature executable Capability Registry is present.

Risks:

- Capability language can drift into ARK mesh routing or Jarvis navigation.
- Providers and plugins need a Compatibility Layer boundary.

Migration:

1. Define capability records and ownership.
2. Inventory legacy capability/provider concepts.
3. Prove one provider option through NOMAD or Compatibility Layer.
4. Keep Jarvis as consumer, not owner, of capability availability.

