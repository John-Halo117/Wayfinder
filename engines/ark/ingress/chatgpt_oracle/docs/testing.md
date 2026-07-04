# Parser Test Suite

## Current Tests

The test suite lives at:

`engines/ark/tests/test_chatgpt_oracle.py`

It verifies:

- deterministic repeated directory imports
- conversation/message/attachment/project relationships
- corrupt JSON reporting
- unknown artifact reporting
- required output file emission
- artifact preservation
- zip export parity with directory export

## Verification Command

```bash
python3 -m pytest -s engines/ark/tests/test_chatgpt_oracle.py
```

## Non-Tested Future Cases

- Real ChatGPT export variants not represented by the synthetic fixture.
- Very large exports near configured caps.
- Byte-offset provenance for streaming parsers.
