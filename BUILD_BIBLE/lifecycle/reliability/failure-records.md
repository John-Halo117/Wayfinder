# Failure Records

Failure records are reusable descriptions of expected failures.

## Required Fields

- failure ID
- affected scope or capability class
- failure class
- causes
- symptoms
- detection method
- isolation method
- repair method
- recovery method
- fallback behavior
- failure propagation
- verification after repair
- digital twin update

## Canonical Examples

- PEX leak
- mini-split failure
- UPS battery aging
- roof penetration leak
- drain clog
- fiber cut
- door lock failure

## Rule

Do not wait for a specific property to fail before modeling expected failure
modes for common systems.

## Relationships

- Parent reliability: [Reliability](README.md)
- Related schema: [reliability-record.schema.json](../../schemas/reliability-record.schema.json)
- Related template: [Reliability Record Template](../../templates/reliability-record.md)
- Generated artifacts: troubleshooting guides, recovery checklists, inspection
  plans

