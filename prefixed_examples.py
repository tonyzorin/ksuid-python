#!/usr/bin/env python3
"""
Prefixed KSUID Examples - Stripe-Style Implementation

This module demonstrates how to implement Stripe-style prefixed identifiers
using KSUIDs for better developer experience and type safety.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from __init__ import KSUID, generate, from_string
from typing import Dict, Optional, Tuple
import re


class PrefixedKSUID:
    """
    A utility class for creating and managing prefixed KSUIDs like Stripe's API keys.
    
    Examples:
        user_2StGMtcWzRJ8qZqQjbJjGdTkVfv
        pi_2StGMtcWzRJ8qZqQjbJjGdTkVfv
        cus_2StGMtcWzRJ8qZqQjbJjGdTkVfv
    """
    
    # Common prefix patterns used by various companies
    ENTITY_PREFIXES = {
        # User-related
        'user': 'user',     # Users
        'admin': 'adm',     # Administrators
        'guest': 'gst',     # Guest users
        
        # Payment-related (Stripe-style)
        'payment_intent': 'pi',
        'payment_method': 'pm',
        'customer': 'cus',
        'charge': 'ch',
        'refund': 're',
        'invoice': 'in',
        'subscription': 'sub',
        'product': 'prod',
        'price': 'price',
        
        # API-related
        'secret_key': 'sk',
        'public_key': 'pk',
        'api_key': 'ak',
        'token': 'tok',
        'session': 'sess',
        
        # Business entities
        'order': 'ord',
        'transaction': 'txn',
        'shipment': 'ship',
        'warehouse': 'wh',
        'inventory': 'inv',
        
        # Content-related
        'post': 'post',
        'comment': 'comm',
        'file': 'file',
        'upload': 'up',
        'download': 'dl',
        
        # System-related
        'log': 'log',
        'event': 'evt',
        'notification': 'notif',
        'webhook': 'whk',
        'job': 'job',
        'task': 'task'
    }
    
    @classmethod
    def create(cls, prefix: str) -> str:
        """
        Create a prefixed KSUID.
        
        Args:
            prefix: The prefix to use (e.g., 'user', 'pi', 'cus')
            
        Returns:
            Prefixed KSUID string (e.g., 'user_2StGMtcWzRJ8qZqQjbJjGdTkVfv')
        """
        if not prefix:
            raise ValueError("Prefix cannot be empty")
        
        # Validate prefix format (alphanumeric and underscores only)
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', prefix):
            raise ValueError("Prefix must start with a letter and contain only alphanumeric characters and underscores")
        
        return f"{prefix}_{generate()}"
    
    @classmethod
    def parse(cls, prefixed_id: str) -> Tuple[str, KSUID]:
        """
        Parse a prefixed KSUID into its components.
        
        Args:
            prefixed_id: The prefixed KSUID string
            
        Returns:
            Tuple of (prefix, KSUID object)
            
        Raises:
            ValueError: If the format is invalid
        """
        if not prefixed_id or '_' not in prefixed_id:
            raise ValueError("Invalid prefixed KSUID format")
        
        parts = prefixed_id.split('_', 1)
        if len(parts) != 2:
            raise ValueError("Invalid prefixed KSUID format")
        
        prefix, ksuid_str = parts
        
        if not prefix:
            raise ValueError("Prefix cannot be empty")
        
        try:
            ksuid = from_string(ksuid_str)
            return prefix, ksuid
        except Exception as e:
            raise ValueError(f"Invalid KSUID part: {e}")
    
    @classmethod
    def validate(cls, prefixed_id: str, expected_prefix: Optional[str] = None) -> bool:
        """
        Validate a prefixed KSUID.
        
        Args:
            prefixed_id: The prefixed KSUID to validate
            expected_prefix: Optional prefix to validate against
            
        Returns:
            True if valid, False otherwise
        """
        try:
            prefix, ksuid = cls.parse(prefixed_id)
            
            if expected_prefix and prefix != expected_prefix:
                return False
            
            return True
        except ValueError:
            return False
    
    @classmethod
    def get_prefix(cls, prefixed_id: str) -> str:
        """
        Extract just the prefix from a prefixed KSUID.
        
        Args:
            prefixed_id: The prefixed KSUID string
            
        Returns:
            The prefix part
        """
        prefix, _ = cls.parse(prefixed_id)
        return prefix
    
    @classmethod
    def get_ksuid(cls, prefixed_id: str) -> KSUID:
        """
        Extract just the KSUID from a prefixed KSUID.
        
        Args:
            prefixed_id: The prefixed KSUID string
            
        Returns:
            The KSUID object
        """
        _, ksuid = cls.parse(prefixed_id)
        return ksuid


# Convenience functions for common entity types
def create_user_id() -> str:
    """Create a user ID: user_..."""
    return PrefixedKSUID.create('user')

def create_payment_intent_id() -> str:
    """Create a payment intent ID: pi_..."""
    return PrefixedKSUID.create('pi')

def create_customer_id() -> str:
    """Create a customer ID: cus_..."""
    return PrefixedKSUID.create('cus')

def create_order_id() -> str:
    """Create an order ID: ord_..."""
    return PrefixedKSUID.create('ord')

def create_api_key() -> str:
    """Create an API key: ak_..."""
    return PrefixedKSUID.create('ak')

def create_session_id() -> str:
    """Create a session ID: sess_..."""
    return PrefixedKSUID.create('sess')


def demo_basic_usage():
    """Demonstrate basic prefixed KSUID usage."""
    print("=== Basic Prefixed KSUID Usage ===")
    
    # Create various types of IDs
    user_id = create_user_id()
    payment_id = create_payment_intent_id()
    customer_id = create_customer_id()
    order_id = create_order_id()
    
    print(f"User ID: {user_id}")
    print(f"Payment ID: {payment_id}")
    print(f"Customer ID: {customer_id}")
    print(f"Order ID: {order_id}")
    print()
    
    # Parse IDs
    print("Parsing IDs:")
    for prefixed_id in [user_id, payment_id, customer_id, order_id]:
        prefix, ksuid = PrefixedKSUID.parse(prefixed_id)
        print(f"  {prefixed_id} -> Prefix: '{prefix}', Timestamp: {ksuid.datetime}")
    print()


def demo_validation():
    """Demonstrate ID validation."""
    print("=== ID Validation ===")
    
    user_id = create_user_id()
    payment_id = create_payment_intent_id()
    
    # Valid cases
    print(f"Is '{user_id}' a valid user ID? {PrefixedKSUID.validate(user_id, 'user')}")
    print(f"Is '{payment_id}' a valid payment ID? {PrefixedKSUID.validate(payment_id, 'pi')}")
    
    # Invalid cases
    print(f"Is '{user_id}' a valid payment ID? {PrefixedKSUID.validate(user_id, 'pi')}")
    print(f"Is 'invalid_id' valid? {PrefixedKSUID.validate('invalid_id')}")
    print(f"Is 'user_invalid_ksuid' valid? {PrefixedKSUID.validate('user_invalid_ksuid')}")
    print()


def demo_api_usage():
    """Demonstrate API-style usage."""
    print("=== API Usage Example ===")
    
    # Simulate API endpoints
    def create_user_endpoint(name: str, email: str) -> Dict:
        user_id = create_user_id()
        return {
            'id': user_id,
            'name': name,
            'email': email,
            'created_at': PrefixedKSUID.get_ksuid(user_id).datetime.isoformat()
        }
    
    def create_payment_endpoint(user_id: str, amount: int) -> Dict:
        # Validate user ID
        if not PrefixedKSUID.validate(user_id, 'user'):
            raise ValueError("Invalid user ID")
        
        payment_id = create_payment_intent_id()
        return {
            'id': payment_id,
            'user_id': user_id,
            'amount': amount,
            'status': 'pending',
            'created_at': PrefixedKSUID.get_ksuid(payment_id).datetime.isoformat()
        }
    
    # Create user
    user = create_user_endpoint("John Doe", "john@example.com")
    print(f"Created user: {user}")
    
    # Create payment for user
    payment = create_payment_endpoint(user['id'], 1000)
    print(f"Created payment: {payment}")
    
    # Show chronological ordering
    user_ksuid = PrefixedKSUID.get_ksuid(user['id'])
    payment_ksuid = PrefixedKSUID.get_ksuid(payment['id'])
    print(f"User created before payment? {user_ksuid < payment_ksuid}")
    print()


def demo_database_patterns():
    """Demonstrate database usage patterns."""
    print("=== Database Usage Patterns ===")
    
    # Simulate database records
    records = []
    
    # Create mixed entity types
    for i in range(5):
        if i % 2 == 0:
            record_id = create_user_id()
            record_type = 'user'
        else:
            record_id = create_order_id()
            record_type = 'order'
        
        records.append({
            'id': record_id,
            'type': record_type,
            'data': f'Sample {record_type} {i}'
        })
    
    print("Created records:")
    for record in records:
        ksuid = PrefixedKSUID.get_ksuid(record['id'])
        print(f"  {record['id']} ({record['type']}) - {ksuid.datetime}")
    
    # Sort by creation time (KSUID natural ordering)
    sorted_records = sorted(records, key=lambda r: PrefixedKSUID.get_ksuid(r['id']))
    
    print("\nSorted by creation time:")
    for record in sorted_records:
        ksuid = PrefixedKSUID.get_ksuid(record['id'])
        print(f"  {record['id']} ({record['type']}) - {ksuid.datetime}")
    
    # Filter by entity type
    user_records = [r for r in records if PrefixedKSUID.get_prefix(r['id']) == 'user']
    order_records = [r for r in records if PrefixedKSUID.get_prefix(r['id']) == 'ord']
    
    print(f"\nUser records: {len(user_records)}")
    print(f"Order records: {len(order_records)}")
    print()


def demo_error_handling():
    """Demonstrate error handling."""
    print("=== Error Handling ===")
    
    test_cases = [
        ("", "Empty string"),
        ("no_underscore", "No underscore"),
        ("_missing_prefix", "Missing prefix"),
        ("user_", "Missing KSUID"),
        ("user_invalid_ksuid", "Invalid KSUID"),
        ("123_valid_ksuid", "Invalid prefix (starts with number)"),
        ("user-invalid_valid_ksuid", "Invalid prefix (contains hyphen)")
    ]
    
    for test_input, description in test_cases:
        try:
            prefix, ksuid = PrefixedKSUID.parse(test_input)
            print(f"✅ {description}: Parsed successfully")
        except ValueError as e:
            print(f"❌ {description}: {e}")
    print()


def main():
    """Run all demonstrations."""
    print("Prefixed KSUID Examples - Stripe-Style Implementation")
    print("=" * 60)
    print()
    
    demo_basic_usage()
    demo_validation()
    demo_api_usage()
    demo_database_patterns()
    demo_error_handling()
    
    print("=== Summary ===")
    print("Prefixed KSUIDs provide:")
    print("✅ Type safety through prefixes")
    print("✅ Chronological ordering")
    print("✅ URL-safe identifiers")
    print("✅ Easy validation and parsing")
    print("✅ Database-friendly design")
    print("✅ Developer-friendly APIs")
    print("✅ Industry-standard patterns")


if __name__ == "__main__":
    main() 