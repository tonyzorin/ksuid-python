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
import time
from datetime import datetime, timezone
from typing import Union, Optional

__version__ = "1.0.0"
__all__ = ["KSUID", "generate", "from_string", "from_bytes"]

# KSUID epoch (January 1, 2014 UTC)
EPOCH = 1400000000

# KSUID components
TIMESTAMP_LENGTH = 4  # 4 bytes for timestamp
PAYLOAD_LENGTH = 16   # 16 bytes for random payload
TOTAL_LENGTH = TIMESTAMP_LENGTH + PAYLOAD_LENGTH  # 20 bytes total

# Base62 alphabet for encoding
BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE62_BASE = len(BASE62_ALPHABET)


class KSUID:
    """
    K-Sortable Unique Identifier
    
    A KSUID is a 20-byte identifier consisting of:
    - 4-byte timestamp (seconds since KSUID epoch)
    - 16-byte random payload
    
    KSUIDs are naturally sortable by creation time and collision-resistant.
    """
    
    def __init__(self, timestamp: Optional[int] = None, payload: Optional[bytes] = None):
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
            raise ValueError("Timestamp cannot be before KSUID epoch (2014-05-13 16:53:20 UTC)")
        if ksuid_timestamp >= 2**32:
            raise ValueError("Timestamp overflow: too far in the future")
        
        self._timestamp = ksuid_timestamp
        self._payload = payload
        self._bytes = ksuid_timestamp.to_bytes(TIMESTAMP_LENGTH, 'big') + payload
    
    @classmethod
    def from_string(cls, ksuid_str: str) -> 'KSUID':
        """
        Create a KSUID from its string representation.
        
        Args:
            ksuid_str: Base62-encoded KSUID string
            
        Returns:
            KSUID instance
        """
        if len(ksuid_str) != 27:
            raise ValueError("KSUID string must be exactly 27 characters")
        
        # Decode from base62
        decoded_bytes = _base62_decode(ksuid_str)
        return cls.from_bytes(decoded_bytes)
    
    @classmethod
    def from_bytes(cls, data: bytes) -> 'KSUID':
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
        
        ksuid_timestamp = int.from_bytes(timestamp_bytes, 'big')
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
            return False
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
    num = int.from_bytes(data, 'big')
    
    if num == 0:
        return BASE62_ALPHABET[0]
    
    result = []
    while num > 0:
        num, remainder = divmod(num, BASE62_BASE)
        result.append(BASE62_ALPHABET[remainder])
    
    # Pad to 27 characters for KSUID
    result.reverse()
    encoded = ''.join(result)
    return encoded.zfill(27)


def _base62_decode(s: str) -> bytes:
    """Decode base62 string to bytes."""
    if not s:
        return b""
    
    num = 0
    for char in s:
        if char not in BASE62_ALPHABET:
            raise ValueError(f"Invalid base62 character: {char}")
        num = num * BASE62_BASE + BASE62_ALPHABET.index(char)
    
    # Convert to bytes (20 bytes for KSUID)
    return num.to_bytes(TOTAL_LENGTH, 'big')


# Convenience functions
def generate() -> KSUID:
    """Generate a new KSUID."""
    return KSUID()


def from_string(ksuid_str: str) -> KSUID:
    """Create a KSUID from its string representation."""
    return KSUID.from_string(ksuid_str)


def from_bytes(data: bytes) -> KSUID:
    """Create a KSUID from raw bytes."""
    return KSUID.from_bytes(data) 