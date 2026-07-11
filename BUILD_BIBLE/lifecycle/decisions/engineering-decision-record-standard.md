# Engineering Decision Record Standard

Engineering Decision Records preserve why a major physical design choice was
made.

## Required Questions

- What problem does this solve?
- Why this solution?
- What alternatives were considered?
- What tradeoffs were accepted?
- What assumptions support the decision?
- What future events should trigger reevaluation?

## Required Fields

- EDR ID
- date
- affected scope IDs
- problem
- decision
- alternatives considered
- tradeoffs
- assumptions
- optionality preserved
- optionality spent
- reevaluation triggers
- verification method

## Revisit Triggers

Examples include code changes, technology changes, repeated failures,
maintenance burden, replacement constraints, capacity exhaustion, and new
observed reality.

## Relationships

- Parent lifecycle: [Decisions](README.md)
- Schema: [decision-record.schema.json](../../schemas/decision-record.schema.json)
- Template: [Engineering Decision Record Template](../../templates/engineering-decision-record.md)
- Related governance: [Stable Principle Promotion](../../governance/stable-principle-promotion.md)
- Generated artifacts: decision indexes, traceability reports, review packets

