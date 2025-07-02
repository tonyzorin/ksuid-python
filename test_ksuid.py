"""
Test suite for KSUID library.
"""

import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pytest
from datetime import datetime, timezone
from __init__ import KSUID, generate, from_string, from_bytes, EPOCH


class TestKSUID:
    """Test cases for KSUID class."""
    
    def test_generate_ksuid(self):
        """Test basic KSUID generation."""
        ksuid = KSUID()
        
        # Check string representation length
        assert len(str(ksuid)) == 27
        
        # Check bytes length
        assert len(ksuid.bytes) == 20
        
        # Check payload length
        assert len(ksuid.payload) == 16
        
        # Check timestamp is reasonable (within last minute)
        now = int(time.time())
        assert abs(ksuid.timestamp - now) < 60
    
    def test_ksuid_with_custom_timestamp(self):
        """Test KSUID creation with custom timestamp."""
        custom_timestamp = 1609459200  # 2021-01-01 00:00:00 UTC
        ksuid = KSUID(timestamp=custom_timestamp)
        
        assert ksuid.timestamp == custom_timestamp
        
        # Check datetime conversion
        expected_dt = datetime.fromtimestamp(custom_timestamp, tz=timezone.utc)
        assert ksuid.datetime == expected_dt
    
    def test_ksuid_with_custom_payload(self):
        """Test KSUID creation with custom payload."""
        payload = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10'
        ksuid = KSUID(payload=payload)
        
        assert ksuid.payload == payload
    
    def test_invalid_payload_length(self):
        """Test that invalid payload length raises error."""
        with pytest.raises(ValueError, match="Payload must be exactly 16 bytes"):
            KSUID(payload=b'\x01\x02\x03')  # Too short
        
        with pytest.raises(ValueError, match="Payload must be exactly 16 bytes"):
            KSUID(payload=b'\x01' * 20)  # Too long
    
    def test_timestamp_before_epoch(self):
        """Test that timestamp before KSUID epoch raises error."""
        with pytest.raises(ValueError, match="Timestamp cannot be before KSUID epoch"):
            KSUID(timestamp=EPOCH - 1)
    
    def test_timestamp_overflow(self):
        """Test that timestamp too far in future raises error."""
        with pytest.raises(ValueError, match="Timestamp overflow"):
            KSUID(timestamp=EPOCH + 2**32)
    
    def test_from_string(self):
        """Test creating KSUID from string representation."""
        ksuid1 = KSUID()
        ksuid_str = str(ksuid1)
        ksuid2 = KSUID.from_string(ksuid_str)
        
        assert ksuid1 == ksuid2
        assert ksuid1.timestamp == ksuid2.timestamp
        assert ksuid1.payload == ksuid2.payload
    
    def test_from_string_invalid_length(self):
        """Test that invalid string length raises error."""
        with pytest.raises(ValueError, match="KSUID string must be exactly 27 characters"):
            KSUID.from_string("too_short")
        
        with pytest.raises(ValueError, match="KSUID string must be exactly 27 characters"):
            KSUID.from_string("a" * 30)  # Too long
    
    def test_from_string_invalid_characters(self):
        """Test that invalid base62 characters raise error."""
        with pytest.raises(ValueError, match="Invalid base62 character"):
            KSUID.from_string("!" * 27)  # Invalid character
    
    def test_from_bytes(self):
        """Test creating KSUID from bytes."""
        ksuid1 = KSUID()
        ksuid_bytes = ksuid1.bytes
        ksuid2 = KSUID.from_bytes(ksuid_bytes)
        
        assert ksuid1 == ksuid2
        assert ksuid1.timestamp == ksuid2.timestamp
        assert ksuid1.payload == ksuid2.payload
    
    def test_from_bytes_invalid_length(self):
        """Test that invalid bytes length raises error."""
        with pytest.raises(ValueError, match="KSUID bytes must be exactly 20 bytes"):
            KSUID.from_bytes(b'\x01\x02\x03')  # Too short
        
        with pytest.raises(ValueError, match="KSUID bytes must be exactly 20 bytes"):
            KSUID.from_bytes(b'\x01' * 25)  # Too long
    
    def test_sortability(self):
        """Test that KSUIDs are sortable by creation time."""
        # Create KSUIDs with different timestamps
        ksuid1 = KSUID(timestamp=1609459200)  # 2021-01-01
        ksuid2 = KSUID(timestamp=1609459201)  # 2021-01-01 + 1 second
        ksuid3 = KSUID(timestamp=1609459202)  # 2021-01-01 + 2 seconds
        
        # Test all comparison operators
        assert ksuid1 < ksuid2 < ksuid3
        assert ksuid1 <= ksuid2 <= ksuid3
        assert ksuid3 > ksuid2 > ksuid1
        assert ksuid3 >= ksuid2 >= ksuid1
        
        # Test sorting
        ksuids = [ksuid3, ksuid1, ksuid2]
        sorted_ksuids = sorted(ksuids)
        assert sorted_ksuids == [ksuid1, ksuid2, ksuid3]
    
    def test_equality(self):
        """Test KSUID equality."""
        # Same timestamp and payload should be equal
        timestamp = 1609459200
        payload = b'\x01' * 16
        ksuid1 = KSUID(timestamp=timestamp, payload=payload)
        ksuid2 = KSUID(timestamp=timestamp, payload=payload)
        
        assert ksuid1 == ksuid2
        assert hash(ksuid1) == hash(ksuid2)
        
        # Different payload should not be equal
        ksuid3 = KSUID(timestamp=timestamp, payload=b'\x02' * 16)
        assert ksuid1 != ksuid3
    
    def test_string_representation(self):
        """Test string and repr methods."""
        ksuid = KSUID()
        ksuid_str = str(ksuid)
        
        # String should be 27 characters
        assert len(ksuid_str) == 27
        
        # Repr should contain the string
        assert ksuid_str in repr(ksuid)
        assert "KSUID" in repr(ksuid)
    
    def test_round_trip_conversion(self):
        """Test that string/bytes conversions are reversible."""
        ksuid1 = KSUID()
        
        # String round trip
        ksuid_str = str(ksuid1)
        ksuid2 = KSUID.from_string(ksuid_str)
        assert ksuid1 == ksuid2
        
        # Bytes round trip
        ksuid_bytes = ksuid1.bytes
        ksuid3 = KSUID.from_bytes(ksuid_bytes)
        assert ksuid1 == ksuid3
    
    def test_datetime_property(self):
        """Test datetime property conversion."""
        timestamp = 1609459200  # 2021-01-01 00:00:00 UTC
        ksuid = KSUID(timestamp=timestamp)
        
        expected_dt = datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        assert ksuid.datetime == expected_dt


class TestConvenienceFunctions:
    """Test convenience functions."""
    
    def test_generate(self):
        """Test generate() function."""
        ksuid = generate()
        assert isinstance(ksuid, KSUID)
        assert len(str(ksuid)) == 27
    
    def test_from_string_function(self):
        """Test from_string() function."""
        ksuid1 = generate()
        ksuid_str = str(ksuid1)
        ksuid2 = from_string(ksuid_str)
        
        assert ksuid1 == ksuid2
    
    def test_from_bytes_function(self):
        """Test from_bytes() function."""
        ksuid1 = generate()
        ksuid_bytes = ksuid1.bytes
        ksuid2 = from_bytes(ksuid_bytes)
        
        assert ksuid1 == ksuid2


class TestKSUIDProperties:
    """Test KSUID properties and edge cases."""
    
    def test_multiple_ksuids_different(self):
        """Test that multiple KSUIDs generated quickly are different."""
        ksuids = [generate() for _ in range(100)]
        
        # All should be unique
        assert len(set(ksuids)) == 100
        
        # All should be sortable (no exceptions)
        sorted_ksuids = sorted(ksuids)
        assert len(sorted_ksuids) == 100
    
    def test_ksuid_ordering_with_same_timestamp(self):
        """Test KSUID ordering when timestamps are the same."""
        timestamp = 1609459200
        
        # Create KSUIDs with same timestamp but different payloads
        ksuid1 = KSUID(timestamp=timestamp, payload=b'\x00' * 16)
        ksuid2 = KSUID(timestamp=timestamp, payload=b'\x01' * 16)
        
        # They should still be comparable (by payload)
        assert ksuid1 < ksuid2
    
    def test_base62_encoding_properties(self):
        """Test properties of base62 encoding."""
        ksuid = generate()
        ksuid_str = str(ksuid)
        
        # Should only contain base62 characters
        valid_chars = set("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
        assert all(c in valid_chars for c in ksuid_str)
        
        # Should be exactly 27 characters
        assert len(ksuid_str) == 27


if __name__ == "__main__":
    # Run tests if script is executed directly
    import sys
    
    # Basic smoke test
    print("Running basic KSUID tests...")
    
    # Test generation
    ksuid1 = generate()
    print(f"Generated KSUID: {ksuid1}")
    print(f"Timestamp: {ksuid1.datetime}")
    
    # Test round-trip
    ksuid2 = from_string(str(ksuid1))
    assert ksuid1 == ksuid2
    print("Round-trip test passed!")
    
    # Test sortability
    import time
    time.sleep(0.001)  # Ensure different timestamp
    ksuid3 = generate()
    assert ksuid1 < ksuid3
    print("Sortability test passed!")
    
    print("\nAll basic tests passed! Run with pytest for comprehensive testing.") 