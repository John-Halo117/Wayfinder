"""Archive substrate canonical interface.

Contract:
- Inputs: Archive source files mapped by future adapters.
- Outputs: canonical substrate objects that map into Wayfinder observations.
- Runtime constraint: future adapters must be bounded by IngestionConfig.
- Memory assumption: future adapters must be bounded by IngestionConfig.
- Failure cases: unsupported format, malformed source, and cap exhaustion.
- Determinism: identical source bytes must produce identical substrate objects.
"""

from __future__ import annotations

SUBSTRATE = "archive"
