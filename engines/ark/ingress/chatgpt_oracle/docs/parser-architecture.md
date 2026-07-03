# Parser Architecture

## Parser Inventory

The initial parser is `chatgpt-export-oracle` version `1.0.0`.

It is deterministic and emits:

- export inventory
- artifact inventory
- parser inventory
- observation stream
- relationship stream
- import report
- validation report
- unknown artifact report

## Parser Strategy

The Oracle uses Python standard-library parsers:

- `json.loads` for JSON artifacts.
- `zipfile.ZipFile` for zipped exports.
- `mimetypes.guess_type` for media type hints.

No custom inference is performed. JSON structure is preserved even when the
Oracle does not understand the domain meaning of a field.

## Idempotence

IDs are derived from canonical JSON, source paths, source hashes, conversation
IDs, message IDs, attachment IDs, and parser version. The default import
timestamp is stable. Reusing the same export and import timestamp produces the
same streams.

## Unsupported Artifacts

Unsupported artifacts are never dropped. They are:

- classified as `Unknown`
- included in inventories
- preserved by hash
- reported as validation warnings
