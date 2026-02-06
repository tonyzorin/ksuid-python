#!/usr/bin/env python3
"""
Example usage of the KSUID library.

This script demonstrates various features of the KSUID library including
generation, parsing, sorting, and practical usage patterns.
"""

import time

from datetime import datetime, timezone
from ksuid import KSUID, generate, from_string


def basic_usage():
    """Demonstrate basic KSUID operations."""
    print("=== Basic KSUID Usage ===")

    # Generate a new KSUID
    ksuid1 = generate()
    print(f"Generated KSUID: {ksuid1}")
    print(f"Length: {len(str(ksuid1))} characters")
    print(f"Timestamp: {ksuid1.datetime}")
    print(f"Unix timestamp: {ksuid1.timestamp}")
    print(f"Payload length: {len(ksuid1.payload)} bytes")
    print()

    # Create KSUID from string
    ksuid_str = str(ksuid1)
    ksuid2 = from_string(ksuid_str)
    print(f"Recreated from string: {ksuid2}")
    print(f"Are they equal? {ksuid1 == ksuid2}")
    print()


def sortability_demo():
    """Demonstrate KSUID sortability."""
    print("=== KSUID Sortability Demo ===")

    # Generate KSUIDs with small time gaps
    ksuids = []
    for i in range(5):
        ksuid = generate()
        ksuids.append(ksuid)
        print(
            f"KSUID {i+1}: {ksuid} "
            f"(created at {ksuid.datetime.strftime('%H:%M:%S.%f')})"
        )
        time.sleep(0.001)  # 1ms delay

    print("\nSorting KSUIDs...")
    sorted_ksuids = sorted(ksuids)

    print("Sorted order:")
    for i, ksuid in enumerate(sorted_ksuids):
        print(f"  {i+1}. {ksuid}")

    # Verify they're in chronological order
    is_sorted = ksuids == sorted_ksuids
    print(f"\nAre they naturally sorted? {is_sorted}")
    print()


def custom_timestamp_demo():
    """Demonstrate KSUIDs with custom timestamps."""
    print("=== Custom Timestamp Demo ===")

    # Create KSUIDs for specific dates
    dates = [
        datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        datetime(2022, 6, 15, 12, 30, 0, tzinfo=timezone.utc),
        datetime(2023, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
    ]

    historical_ksuids = []
    for date in dates:
        timestamp = int(date.timestamp())
        ksuid = KSUID(timestamp=timestamp)
        historical_ksuids.append(ksuid)
        print(f"KSUID for {date}: {ksuid}")

    print("\nSorting historical KSUIDs:")
    for ksuid in sorted(historical_ksuids):
        print(f"  {ksuid} -> {ksuid.datetime}")
    print()


def performance_demo():
    """Demonstrate KSUID performance."""
    print("=== Performance Demo ===")

    # Time KSUID generation
    start_time = time.perf_counter()
    count = 10000

    ksuids = [generate() for _ in range(count)]

    end_time = time.perf_counter()
    total_time = end_time - start_time

    print(f"Generated {count:,} KSUIDs in {total_time:.4f} seconds")
    print(f"Rate: {count/total_time:,.0f} KSUIDs/second")
    print(f"Average time per KSUID: {(total_time/count)*1_000_000:.2f} microseconds")

    # Verify uniqueness
    unique_ksuids = set(ksuids)
    print(f"Unique KSUIDs: {len(unique_ksuids):,} / {count:,}")
    print(f"Collision rate: {(count - len(unique_ksuids))/count*100:.6f}%")
    print()


def database_simulation():
    """Simulate database usage with KSUIDs."""
    print("=== Database Simulation ===")

    # Simulate user records with KSUID primary keys
    users = []

    user_names = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

    for name in user_names:
        user_id = generate()
        user = {
            "id": str(user_id),
            "name": name,
            "created_at": user_id.datetime,
            "ksuid_obj": user_id,  # Keep KSUID object for sorting
        }
        users.append(user)
        time.sleep(0.001)  # Simulate time between user creations

    print("Created users:")
    for user in users:
        print(
            f"  ID: {user['id']}, Name: {user['name']}, Created: {user['created_at']}"
        )

    # Sort by creation time using KSUID
    print("\nUsers sorted by creation time (using KSUID sorting):")
    sorted_users = sorted(users, key=lambda u: u["ksuid_obj"])
    for user in sorted_users:
        print(f"  {user['name']} -> {user['created_at'].strftime('%H:%M:%S.%f')}")

    # Demonstrate range queries
    print("\nSimulating range query (users created in last 10ms):")
    now = generate()
    cutoff_time = now.datetime.timestamp() - 0.01  # 10ms ago

    recent_users = [user for user in users if user["ksuid_obj"].timestamp > cutoff_time]

    print(f"Found {len(recent_users)} recent users")
    print()


def format_conversion_demo():
    """Demonstrate format conversions."""
    print("=== Format Conversion Demo ===")

    ksuid = generate()

    print(f"Original KSUID: {ksuid}")
    print(f"String representation: {str(ksuid)}")
    print(f"Bytes representation: {ksuid.bytes.hex()}")
    print(f"Timestamp: {ksuid.timestamp}")
    print(f"Datetime: {ksuid.datetime}")
    print(f"Payload: {ksuid.payload.hex()}")

    # Round-trip conversions
    print("\nRound-trip conversions:")

    # String round-trip
    ksuid_from_string = from_string(str(ksuid))
    print(f"From string: {ksuid == ksuid_from_string}")

    # Bytes round-trip
    ksuid_from_bytes = KSUID.from_bytes(ksuid.bytes)
    print(f"From bytes: {ksuid == ksuid_from_bytes}")

    # Timestamp + payload round-trip
    ksuid_reconstructed = KSUID(timestamp=ksuid.timestamp, payload=ksuid.payload)
    print(f"Reconstructed: {ksuid == ksuid_reconstructed}")
    print()


def main():
    """Run all demonstrations."""
    print("KSUID Library Demonstration")
    print("=" * 50)
    print()

    basic_usage()
    sortability_demo()
    custom_timestamp_demo()
    performance_demo()
    database_simulation()
    format_conversion_demo()

    print("=== Summary ===")
    print("KSUIDs provide:")
    print("[+] Sortable unique identifiers")
    print("[+] Compact 27-character representation")
    print("[+] URL-safe base62 encoding")
    print("[+] Embedded timestamp for debugging")
    print("[+] High performance and collision resistance")
    print("[+] Perfect for distributed systems and databases")


if __name__ == "__main__":
    main()
