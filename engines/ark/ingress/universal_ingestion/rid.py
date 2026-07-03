"""Deterministic cSHAKE256 RID generation.

Contract:
- Inputs: domain separation string and canonical payload bytes.
- Outputs: Wayfinder RID strings.
- Runtime constraint: O(len(domain) + len(payload)), bounded by caller config.
- Memory assumption: O(len(domain) + len(payload)).
- Failure cases: empty domain, negative output size, oversized domain by caller policy.
- Determinism: identical domain and payload always produce identical RIDs.
"""

from __future__ import annotations

from hashlib import shake_256

_RATE_BYTES = 136
_DEFAULT_DIGEST_BYTES = 32


def _left_encode(value: int) -> bytes:
    if value < 0:
        raise ValueError("encoded value must be non-negative")
    encoded = value.to_bytes(max(1, (value.bit_length() + 7) // 8), "big")
    return bytes((len(encoded),)) + encoded


def _encode_string(value: bytes) -> bytes:
    return _left_encode(len(value) * 8) + value


def _bytepad(value: bytes, width: int) -> bytes:
    if width <= 0:
        raise ValueError("width must be positive")
    padded = _left_encode(width) + value
    remainder = len(padded) % width
    if remainder:
        padded += b"\x00" * (width - remainder)
    return padded


def cshake256(data: bytes, *, function_name: bytes = b"", customization: bytes = b"", digest_bytes: int = _DEFAULT_DIGEST_BYTES) -> bytes:
    """Return cSHAKE256(data, digest_bytes) per SP 800-185 framing.

    Runtime: O(len(data) + len(function_name) + len(customization)).
    Memory: O(len(data) + len(function_name) + len(customization)).
    Failure: raises ValueError for non-positive digest sizes.
    Deterministic: yes.
    """

    if digest_bytes <= 0:
        raise ValueError("digest_bytes must be positive")
    if not function_name and not customization:
        return shake_256(data).digest(digest_bytes)
    prefix = _bytepad(_encode_string(function_name) + _encode_string(customization), _RATE_BYTES)
    return shake_256(prefix + data + b"\x04").digest(digest_bytes)


def cshake256_rid(domain: str, canonical_payload: bytes, *, digest_bytes: int = _DEFAULT_DIGEST_BYTES) -> str:
    """Return a deterministic Wayfinder RID using cSHAKE256 domain separation.

    Runtime: O(len(domain) + len(canonical_payload)).
    Memory: O(len(domain) + len(canonical_payload)).
    Failure: raises ValueError for empty domain or invalid digest size.
    Deterministic: yes.
    """

    normalized_domain = domain.strip()
    if not normalized_domain:
        raise ValueError("domain is required")
    digest = cshake256(
        canonical_payload,
        function_name=b"WayfinderRID",
        customization=normalized_domain.encode("utf-8"),
        digest_bytes=digest_bytes,
    )
    return f"rid:{normalized_domain}:{digest.hex()}"
