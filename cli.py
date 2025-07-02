#!/usr/bin/env python3
"""
Command-line interface for KSUID library.

This provides a simple CLI for generating and inspecting KSUIDs.
"""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from __init__ import KSUID, generate, from_string
from datetime import datetime


def cmd_generate(args):
    """Generate one or more KSUIDs."""
    for _ in range(args.count):
        ksuid = generate()
        if args.prefix:
            result = f"{args.prefix}_{ksuid}"
        else:
            result = str(ksuid)
            
        if args.verbose:
            if args.prefix:
                print(f"{result} -> {ksuid.datetime} (timestamp: {ksuid.timestamp})")
            else:
                print(f"{ksuid} -> {ksuid.datetime} (timestamp: {ksuid.timestamp})")
        else:
            print(result)


def cmd_inspect(args):
    """Inspect a KSUID and show its components."""
    try:
        ksuid = from_string(args.ksuid)
        
        print(f"KSUID: {ksuid}")
        print(f"Timestamp: {ksuid.timestamp}")
        print(f"Datetime: {ksuid.datetime}")
        print(f"Payload: {ksuid.payload.hex()}")
        print(f"Raw bytes: {ksuid.bytes.hex()}")
        
        # Calculate age
        now = datetime.now(ksuid.datetime.tzinfo)
        age = now - ksuid.datetime
        print(f"Age: {age}")
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_compare(args):
    """Compare two KSUIDs."""
    try:
        ksuid1 = from_string(args.ksuid1)
        ksuid2 = from_string(args.ksuid2)
        
        print(f"KSUID 1: {ksuid1}")
        print(f"  Timestamp: {ksuid1.datetime}")
        print()
        print(f"KSUID 2: {ksuid2}")
        print(f"  Timestamp: {ksuid2.datetime}")
        print()
        
        if ksuid1 == ksuid2:
            print("Result: KSUIDs are identical")
        elif ksuid1 < ksuid2:
            print("Result: KSUID 1 is older than KSUID 2")
            time_diff = ksuid2.datetime - ksuid1.datetime
            print(f"Time difference: {time_diff}")
        else:
            print("Result: KSUID 1 is newer than KSUID 2")
            time_diff = ksuid1.datetime - ksuid2.datetime
            print(f"Time difference: {time_diff}")
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_benchmark(args):
    """Run a simple benchmark."""
    import time
    
    print(f"Benchmarking KSUID generation ({args.count:,} iterations)...")
    
    start_time = time.perf_counter()
    ksuids = [generate() for _ in range(args.count)]
    end_time = time.perf_counter()
    
    total_time = end_time - start_time
    rate = args.count / total_time
    
    print(f"Generated {args.count:,} KSUIDs in {total_time:.4f} seconds")
    print(f"Rate: {rate:,.0f} KSUIDs/second")
    
    # Check uniqueness
    unique_count = len(set(ksuids))
    collision_rate = (args.count - unique_count) / args.count * 100
    print(f"Uniqueness: {unique_count:,} / {args.count:,} ({collision_rate:.6f}% collisions)")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="KSUID command-line tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s generate                    # Generate a single KSUID
  %(prog)s generate -c 5               # Generate 5 KSUIDs
  %(prog)s generate -v                 # Generate with verbose output
  %(prog)s generate -p user            # Generate user_2StGMtcWzRJ8qZqQjbJjGdTkVfv
  %(prog)s generate -p pi -c 3         # Generate 3 Stripe-style payment IDs
  %(prog)s inspect 2StGMtcWzRJ8qZqQjbJjGdTkVfv  # Inspect a KSUID
  %(prog)s compare KSUID1 KSUID2       # Compare two KSUIDs
  %(prog)s benchmark -c 10000          # Benchmark generation
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate KSUIDs')
    gen_parser.add_argument(
        '-c', '--count', 
        type=int, 
        default=1, 
        help='Number of KSUIDs to generate (default: 1)'
    )
    gen_parser.add_argument(
        '-v', '--verbose', 
        action='store_true', 
        help='Show additional information'
    )
    gen_parser.add_argument(
        '-p', '--prefix', 
        type=str, 
        help='Add prefix to KSUID (e.g., user, pi, cus for Stripe-style IDs)'
    )
    gen_parser.set_defaults(func=cmd_generate)
    
    # Inspect command
    inspect_parser = subparsers.add_parser('inspect', help='Inspect a KSUID')
    inspect_parser.add_argument('ksuid', help='KSUID to inspect')
    inspect_parser.set_defaults(func=cmd_inspect)
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', help='Compare two KSUIDs')
    compare_parser.add_argument('ksuid1', help='First KSUID')
    compare_parser.add_argument('ksuid2', help='Second KSUID')
    compare_parser.set_defaults(func=cmd_compare)
    
    # Benchmark command
    bench_parser = subparsers.add_parser('benchmark', help='Run benchmark')
    bench_parser.add_argument(
        '-c', '--count', 
        type=int, 
        default=10000, 
        help='Number of KSUIDs to generate (default: 10000)'
    )
    bench_parser.set_defaults(func=cmd_benchmark)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    args.func(args)


if __name__ == "__main__":
    main() 