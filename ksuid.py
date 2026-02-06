"""
KSUID - K-Sortable Unique Identifier

A Python implementation of KSUID (K-Sortable Unique Identifier).
KSUIDs are 20-byte identifiers that combine a timestamp with random data
to create sortable, unique identifiers.

Usage:
    >>> from ksuid import KSUID
    >>> ksuid = KSUID()
    >>> str(ksuid)
    '2StGMtcWzRJ8qZqQjbJjGdTkVfv'

    >>> # Create from string
    >>> ksuid2 = KSUID.from_string('2StGMtcWzRJ8qZqQjbJjGdTkVfv')

    >>> # Compare KSUIDs (they're sortable)
    >>> ksuid1 < ksuid2
    True
"""

import os
import secrets
import time
from datetime import datetime, timezone
from typing import Optional

__version__ = "2.0.0"
__all__ = [
    "KSUID",
    "generate",
    "generate_lowercase",
    "generate_token",
    "generate_token_lowercase",
    "from_string",
    "from_base36",
    "from_bytes",
]

# KSUID epoch (May 13, 2014 16:53:20 UTC)
EPOCH = 1400000000

# KSUID components
TIMESTAMP_LENGTH = 4  # 4 bytes for timestamp
PAYLOAD_LENGTH = 16  # 16 bytes for random payload
TOTAL_LENGTH = TIMESTAMP_LENGTH + PAYLOAD_LENGTH  # 20 bytes total

# Base62 alphabet for encoding (mixed-case)
BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE62_BASE = len(BASE62_ALPHABET)
_BASE62_STRING_LENGTH = 27  # 20 bytes in base62

# Base36 alphabet for lowercase encoding
BASE36_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"
BASE36_BASE = len(BASE36_ALPHABET)
_BASE36_STRING_LENGTH = 31  # 20 bytes in base36


class KSUID:
    """
    K-Sortable Unique Identifier

    A KSUID is a 20-byte identifier consisting of:
    - 4-byte timestamp (seconds since KSUID epoch)
    - 16-byte random payload

    KSUIDs are naturally sortable by creation time and collision-resistant.
    """

    __slots__ = ("_timestamp", "_payload", "_bytes")

    def __init__(
        self, timestamp: Optional[int] = None, payload: Optional[bytes] = None
    ):
        """
        Create a new KSUID.

        Args:
            timestamp: Unix timestamp (seconds). If None, uses current time.
            payload: 16-byte random payload. If None, generates random bytes.
        """
        if timestamp is None:
            timestamp = int(time.time())

        if payload is None:
            payload = os.urandom(PAYLOAD_LENGTH)
        elif len(payload) != PAYLOAD_LENGTH:
            raise ValueError(f"Payload must be exactly {PAYLOAD_LENGTH} bytes")

        # Convert timestamp to KSUID timestamp (relative to KSUID epoch)
        ksuid_timestamp = timestamp - EPOCH
        if ksuid_timestamp < 0:
            raise ValueError(
                "Timestamp cannot be before KSUID epoch (2014-05-13 16:53:20 UTC)"
            )
        if ksuid_timestamp >= 2**32:
            raise ValueError("Timestamp overflow: too far in the future")

        self._timestamp = ksuid_timestamp
        self._payload = payload
        self._bytes = ksuid_timestamp.to_bytes(TIMESTAMP_LENGTH, "big") + payload

    @classmethod
    def from_string(cls, ksuid_str: str) -> "KSUID":
        """
        Create a KSUID from its string representation.

        Args:
            ksuid_str: Base62-encoded KSUID string

        Returns:
            KSUID instance
        """
        if len(ksuid_str) != _BASE62_STRING_LENGTH:
            raise ValueError(
                f"KSUID string must be exactly {_BASE62_STRING_LENGTH} characters"
            )

        # Decode from base62
        decoded_bytes = _base62_decode(ksuid_str)
        return cls.from_bytes(decoded_bytes)

    @classmethod
    def from_base36(cls, ksuid_str: str) -> "KSUID":
        """
        Create a KSUID from a lowercase base36 string representation.

        Args:
            ksuid_str: Base36-encoded KSUID string (31 characters)

        Returns:
            KSUID instance
        """
        if len(ksuid_str) != _BASE36_STRING_LENGTH:
            raise ValueError(
                f"Base36 KSUID string must be exactly "
                f"{_BASE36_STRING_LENGTH} characters"
            )

        decoded_bytes = _base36_decode(ksuid_str)
        return cls.from_bytes(decoded_bytes)

    def to_base36(self) -> str:
        """Return a lowercase base36-encoded string (31 characters)."""
        return _base36_encode(self._bytes)

    @classmethod
    def from_bytes(cls, data: bytes) -> "KSUID":
        """
        Create a KSUID from raw bytes.

        Args:
            data: 20-byte KSUID data

        Returns:
            KSUID instance
        """
        if len(data) != TOTAL_LENGTH:
            raise ValueError(f"KSUID bytes must be exactly {TOTAL_LENGTH} bytes")

        timestamp_bytes = data[:TIMESTAMP_LENGTH]
        payload = data[TIMESTAMP_LENGTH:]

        ksuid_timestamp = int.from_bytes(timestamp_bytes, "big")
        unix_timestamp = ksuid_timestamp + EPOCH

        return cls(unix_timestamp, payload)

    @property
    def timestamp(self) -> int:
        """Unix timestamp when this KSUID was created."""
        return self._timestamp + EPOCH

    @property
    def datetime(self) -> datetime:
        """Datetime when this KSUID was created (UTC)."""
        return datetime.fromtimestamp(self.timestamp, tz=timezone.utc)

    @property
    def payload(self) -> bytes:
        """16-byte random payload."""
        return self._payload

    @property
    def bytes(self) -> bytes:
        """Raw 20-byte KSUID data."""
        return self._bytes

    def __str__(self) -> str:
        """Base62-encoded string representation."""
        return _base62_encode(self._bytes)

    def __repr__(self) -> str:
        return f"KSUID('{str(self)}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, KSUID):
            return NotImplemented
        return self._bytes == other._bytes

    def __lt__(self, other) -> bool:
        if not isinstance(other, KSUID):
            return NotImplemented
        return self._bytes < other._bytes

    def __le__(self, other) -> bool:
        if not isinstance(other, KSUID):
            return NotImplemented
        return self._bytes <= other._bytes

    def __gt__(self, other) -> bool:
        if not isinstance(other, KSUID):
            return NotImplemented
        return self._bytes > other._bytes

    def __ge__(self, other) -> bool:
        if not isinstance(other, KSUID):
            return NotImplemented
        return self._bytes >= other._bytes

    def __hash__(self) -> int:
        return hash(self._bytes)


def _base62_encode(data: bytes) -> str:
    """Encode bytes to base62 string."""
    if not data:
        return ""

    # Convert bytes to integer
    num = int.from_bytes(data, "big")

    result = []
    while num > 0:
        num, remainder = divmod(num, BASE62_BASE)
        result.append(BASE62_ALPHABET[remainder])

    # Pad to fixed width for KSUID
    result.reverse()
    encoded = "".join(result)
    return encoded.zfill(_BASE62_STRING_LENGTH)


_BASE62_LOOKUP = {c: i for i, c in enumerate(BASE62_ALPHABET)}

# Maximum integer value that fits in TOTAL_LENGTH bytes
_MAX_ENCODED = (1 << (TOTAL_LENGTH * 8)) - 1


def _base62_decode(s: str) -> bytes:
    """Decode base62 string to bytes."""
    if not s:
        return b""

    num = 0
    for char in s:
        val = _BASE62_LOOKUP.get(char)
        if val is None:
            raise ValueError(f"Invalid base62 character: {char}")
        num = num * BASE62_BASE + val

    if num > _MAX_ENCODED:
        raise ValueError("Base62 value exceeds maximum for KSUID")

    # Convert to bytes (20 bytes for KSUID)
    return num.to_bytes(TOTAL_LENGTH, "big")


# --- Base36 (lowercase) encoding ---------------------------------------------------

_BASE36_LOOKUP = {c: i for i, c in enumerate(BASE36_ALPHABET)}


def _base36_encode(data: bytes) -> str:
    """Encode bytes to lowercase base36 string."""
    if not data:
        return ""

    num = int.from_bytes(data, "big")

    result = []
    while num > 0:
        num, remainder = divmod(num, BASE36_BASE)
        result.append(BASE36_ALPHABET[remainder])

    result.reverse()
    encoded = "".join(result)
    return encoded.zfill(_BASE36_STRING_LENGTH)


def _base36_decode(s: str) -> bytes:
    """Decode lowercase base36 string to bytes."""
    if not s:
        return b""

    num = 0
    for char in s:
        val = _BASE36_LOOKUP.get(char)
        if val is None:
            raise ValueError(f"Invalid base36 character: {char!r}")
        num = num * BASE36_BASE + val

    if num > _MAX_ENCODED:
        raise ValueError("Base36 value exceeds maximum for KSUID")

    return num.to_bytes(TOTAL_LENGTH, "big")


# Convenience functions
def generate() -> KSUID:
    """Generate a new KSUID."""
    return KSUID()


def generate_token() -> str:
    """Generate a cryptographically secure opaque token as a base62 string.

    Unlike KSUIDs, tokens use 20 bytes (160 bits) of pure random data from
    ``secrets.token_bytes`` with no embedded timestamp.  This makes them
    suitable for API keys, session secrets, and other security-sensitive
    values where the creation time should not be leaked.

    Returns:
        A 27-character base62 string with 160 bits of entropy.
    """
    return _base62_encode(secrets.token_bytes(TOTAL_LENGTH))


def generate_lowercase() -> str:
    """Generate a new KSUID and return it as a lowercase base36 string.

    The returned 31-character string uses only ``0-9a-z`` and preserves
    the KSUID's timestamp + random-payload structure (sortable).

    Returns:
        A 31-character lowercase base36 string.
    """
    return KSUID().to_base36()


def generate_token_lowercase() -> str:
    """Generate a cryptographically secure opaque token as a lowercase string.

    Uses 20 bytes (160 bits) of pure random data (no timestamp) encoded
    in base36 (``0-9a-z`` only).

    Returns:
        A 31-character lowercase base36 string with 160 bits of entropy.
    """
    return _base36_encode(secrets.token_bytes(TOTAL_LENGTH))


def from_string(ksuid_str: str) -> KSUID:
    """Create a KSUID from its string representation."""
    return KSUID.from_string(ksuid_str)


def from_base36(ksuid_str: str) -> KSUID:
    """Create a KSUID from a lowercase base36 string representation."""
    return KSUID.from_base36(ksuid_str)


def from_bytes(data: bytes) -> KSUID:
    """Create a KSUID from raw bytes."""
    return KSUID.from_bytes(data)
