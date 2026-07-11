# Change Control

Physical-world changes are recorded before, during, and after implementation.

## Change Types

- Intent change: modifies what should exist.
- Reality change: records what physically changed.
- Interface change: adds, removes, or changes a connection between scopes.
- Capacity change: changes available reserve or load.
- Maintenance change: changes an obligation or procedure.
- Retirement change: removes or decommissions a scope.

## Required Record

Every material change must include:

- affected scope IDs
- reason
- decision or observation source
- expected impact
- rollback or recovery path when practical
- verification method

## History Rule

Do not delete history to make current reality simpler. Supersede records with
explicit links.

