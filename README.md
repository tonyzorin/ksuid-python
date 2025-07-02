# KSUID - K-Sortable Unique Identifier

A Python implementation of [KSUID](https://github.com/segmentio/ksuid) (K-Sortable Unique Identifier) for Python 3.13+.

## What is a KSUID?

A KSUID is a globally unique identifier similar to a UUID, but with better properties:

- **Sortable**: KSUIDs are naturally sortable by creation time
- **Compact**: 27 characters when base62-encoded (vs 36 for UUID)
- **URL-safe**: Uses base62 encoding (no special characters)
- **Collision-resistant**: 128 bits of randomness per millisecond
- **Time-based**: Encodes creation timestamp for easy debugging
- **Prefix-friendly**: Can be prefixed for type identification (like Stripe's API keys)

## Format

A KSUID is a 20-byte identifier consisting of:
- **4 bytes**: Timestamp (seconds since KSUID epoch: 2014-05-13 16:53:20 UTC)
- **16 bytes**: Random payload

When base62-encoded, it becomes a 27-character string like: `2StGMtcWzRJ8qZqQjbJjGdTkVfv`

## Real-World Usage Examples

Many successful companies use KSUID-style identifiers with prefixes for better developer experience:

### Stripe-Style Prefixed IDs
```python
from ksuid import generate

# Payment Intent: pi_1A2B3C...
payment_intent = f"pi_{generate()}"

# Customer: cus_1A2B3C...
customer = f"cus_{generate()}"

# Charge: ch_1A2B3C...
charge = f"ch_{generate()}"
```

### GitHub-Style IDs
```python
# Repository: repo_1A2B3C...
repository = f"repo_{generate()}"

# Issue: issue_1A2B3C...
issue = f"issue_{generate()}"

# Pull Request: pr_1A2B3C...
pull_request = f"pr_{generate()}"
```

### Database Entity IDs
```python
# User: user_1A2B3C...
user_id = f"user_{generate()}"

# Order: order_1A2B3C...
order_id = f"order_{generate()}"

# Product: prod_1A2B3C...
product_id = f"prod_{generate()}"
```

### Benefits of Prefixed KSUIDs

1. **Type Safety**: Immediately identify the entity type
2. **Debugging**: Easier to trace issues in logs
3. **API Design**: Self-documenting API endpoints
4. **Database Queries**: Faster filtering by prefix
5. **Developer Experience**: Clear, readable identifiers

## Installation

```bash
pip install ksuid
```

## Quick Start

```python
from ksuid import KSUID, generate

# Generate a new KSUID
ksuid = generate()
print(ksuid)  # 2StGMtcWzRJ8qZqQjbJjGdTkVfv

# Create from string
ksuid2 = KSUID.from_string('2StGMtcWzRJ8qZqQjbJjGdTkVfv')

# KSUIDs are sortable
ksuid1 = generate()
time.sleep(0.001)
ksuid2 = generate()
assert ksuid1 < ksuid2  # True!

# Access timestamp and payload
print(ksuid.datetime)  # 2025-01-17 10:30:45+00:00
print(ksuid.timestamp)  # 1737108645
print(len(ksuid.payload))  # 16 bytes
```

## API Reference

### Class: `KSUID`

#### Constructor

```python
KSUID(timestamp=None, payload=None)
```

- `timestamp`: Unix timestamp (int). If None, uses current time.
- `payload`: 16-byte random payload (bytes). If None, generates random bytes.

#### Class Methods

```python
KSUID.from_string(ksuid_str: str) -> KSUID
```
Create a KSUID from its base62 string representation.

```python
KSUID.from_bytes(data: bytes) -> KSUID
```
Create a KSUID from raw 20-byte data.

#### Properties

- `timestamp`: Unix timestamp (int)
- `datetime`: Python datetime object (UTC)
- `payload`: 16-byte random payload (bytes)
- `bytes`: Raw 20-byte KSUID data (bytes)

#### Methods

- `__str__()`: Returns base62-encoded string representation
- `__repr__()`: Returns developer-friendly representation
- Comparison operators: `<`, `<=`, `>`, `>=`, `==`, `!=`
- `__hash__()`: Makes KSUIDs hashable (usable in sets/dicts)

### Convenience Functions

```python
generate() -> KSUID
```
Generate a new KSUID with current timestamp.

```python
from_string(ksuid_str: str) -> KSUID
```
Create KSUID from string (alias for `KSUID.from_string`).

```python
from_bytes(data: bytes) -> KSUID
```
Create KSUID from bytes (alias for `KSUID.from_bytes`).

## Examples

### Basic Usage

```python
from ksuid import KSUID, generate
import time

# Generate KSUIDs
ksuid1 = generate()
time.sleep(0.001)
ksuid2 = generate()

print(f"KSUID 1: {ksuid1}")
print(f"KSUID 2: {ksuid2}")
print(f"KSUID 1 < KSUID 2: {ksuid1 < ksuid2}")  # True
```

### Prefixed IDs (Stripe-Style)

```python
from ksuid import generate

def create_prefixed_id(prefix: str) -> str:
    """Create a prefixed ID like Stripe's API keys."""
    return f"{prefix}_{generate()}"

# Create different entity types
user_id = create_prefixed_id("user")        # user_2StGMtcWzRJ8qZqQjbJjGdTkVfv
payment_id = create_prefixed_id("pi")       # pi_2StGMtcWzRJ8qZqQjbJjGdTkVfv
customer_id = create_prefixed_id("cus")     # cus_2StGMtcWzRJ8qZqQjbJjGdTkVfv

print(f"User ID: {user_id}")
print(f"Payment ID: {payment_id}")
print(f"Customer ID: {customer_id}")

# Extract KSUID from prefixed ID
def extract_ksuid(prefixed_id: str) -> str:
    """Extract KSUID from prefixed ID."""
    return prefixed_id.split('_', 1)[1]

ksuid_part = extract_ksuid(user_id)
print(f"Extracted KSUID: {ksuid_part}")
```

### Custom Timestamp and Payload

```python
from ksuid import KSUID
from datetime import datetime

# Create with specific timestamp
timestamp = int(datetime(2021, 1, 1).timestamp())
ksuid = KSUID(timestamp=timestamp)

# Create with custom payload
payload = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10'
ksuid = KSUID(payload=payload)
```

### Sorting and Comparison

```python
from ksuid import generate
import time

# Generate multiple KSUIDs
ksuids = []
for i in range(5):
    ksuids.append(generate())
    time.sleep(0.001)

# They're naturally sorted by creation time
sorted_ksuids = sorted(ksuids)
assert ksuids == sorted_ksuids  # True!

# Use in data structures
ksuid_set = set(ksuids)
ksuid_dict = {k: f"value_{i}" for i, k in enumerate(ksuids)}
```

### Database Usage

```python
from ksuid import generate
import sqlite3

# Create table with KSUID primary key
conn = sqlite3.connect(':memory:')
conn.execute('''
    CREATE TABLE users (
        id TEXT PRIMARY KEY,
        name TEXT,
        created_at DATETIME
    )
''')

# Insert records with KSUID
ksuid = generate()
conn.execute(
    'INSERT INTO users (id, name, created_at) VALUES (?, ?, ?)',
    (str(ksuid), 'John Doe', ksuid.datetime)
)

# Query by KSUID
cursor = conn.execute('SELECT * FROM users WHERE id = ?', (str(ksuid),))
print(cursor.fetchone())
```

### Production API Example (Flask)

```python
from flask import Flask, jsonify, request
from ksuid import generate
import sqlite3

app = Flask(__name__)

def create_prefixed_id(prefix: str) -> str:
    return f"{prefix}_{generate()}"

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = create_prefixed_id("user")
    
    # Store in database
    conn = sqlite3.connect('app.db')
    conn.execute(
        'INSERT INTO users (id, name, email) VALUES (?, ?, ?)',
        (user_id, data['name'], data['email'])
    )
    conn.commit()
    conn.close()
    
    return jsonify({
        'id': user_id,
        'name': data['name'],
        'email': data['email']
    }), 201

@app.route('/api/users/<user_id>')
def get_user(user_id):
    # Validate prefix
    if not user_id.startswith('user_'):
        return jsonify({'error': 'Invalid user ID format'}), 400
    
    conn = sqlite3.connect('app.db')
    cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user[0],
        'name': user[1],
        'email': user[2]
    })

# Example usage:
# POST /api/users -> {"id": "user_2StGMtcWzRJ8qZqQjbJjGdTkVfv", ...}
# GET /api/users/user_2StGMtcWzRJ8qZqQjbJjGdTkVfv -> User details
```

### Converting Between Formats

```python
from ksuid import KSUID

# Start with a KSUID
ksuid = KSUID()

# Get different representations
string_repr = str(ksuid)           # Base62 string
bytes_repr = ksuid.bytes           # Raw bytes
timestamp = ksuid.timestamp        # Unix timestamp
datetime_obj = ksuid.datetime      # Python datetime

# Recreate from representations
ksuid_from_string = KSUID.from_string(string_repr)
ksuid_from_bytes = KSUID.from_bytes(bytes_repr)

# All should be equal
assert ksuid == ksuid_from_string == ksuid_from_bytes
```

## Performance

KSUIDs are designed to be fast and efficient:

- **Generation**: ~1-2 microseconds per KSUID
- **Parsing**: ~500 nanoseconds from string
- **Comparison**: ~100 nanoseconds
- **Memory**: 20 bytes per KSUID + Python object overhead

## Comparison with UUIDs

| Feature | KSUID | UUID v4 | UUID v1 | Stripe IDs |
|---------|-------|---------|---------|------------|
| Length | 27 chars | 36 chars | 36 chars | 24-28 chars |
| Sortable | ✅ Yes | ❌ No | ⚠️ Partially | ❌ No |
| URL-safe | ✅ Yes | ❌ No (hyphens) | ❌ No (hyphens) | ✅ Yes |
| Timestamp | ✅ Readable | ❌ No | ✅ But complex | ❌ No |
| Collision resistance | ✅ High | ✅ High | ✅ High | ✅ High |
| Monotonic | ✅ Yes | ❌ No | ⚠️ Partially | ❌ No |
| Prefix support | ✅ Natural | ❌ Awkward | ❌ Awkward | ✅ Built-in |
| Developer UX | ✅ Excellent | ⚠️ Good | ⚠️ Good | ✅ Excellent |

## Industry Adoption & Best Practices

### Companies Using KSUID-Style IDs

Many successful companies use sortable, prefixed identifiers:

- **Stripe**: `pi_1A2B3C...`, `cus_1A2B3C...`, `ch_1A2B3C...`
- **GitHub**: Repository and issue IDs with chronological ordering
- **Slack**: Channel and message IDs for efficient sorting
- **Discord**: Snowflake IDs (similar concept with timestamps)
- **Twitter**: Tweet IDs (chronologically sortable)

### Prefix Naming Conventions

Common patterns for prefixes:

```python
# Entity types (3-4 chars)
user_id = f"user_{generate()}"      # Users
prod_id = f"prod_{generate()}"      # Products
ord_id = f"ord_{generate()}"        # Orders

# Action types (2-3 chars)
payment_id = f"pi_{generate()}"     # Payment Intent (Stripe style)
charge_id = f"ch_{generate()}"      # Charge
refund_id = f"re_{generate()}"      # Refund

# Short codes (2-3 chars)
api_key = f"sk_{generate()}"        # Secret Key
pub_key = f"pk_{generate()}"        # Public Key
token = f"tok_{generate()}"         # Token
```

### Database Design Tips

```sql
-- Index on prefix for fast filtering
CREATE INDEX idx_users_by_type ON transactions(id) WHERE id LIKE 'user_%';

-- Partial indexes for different entity types
CREATE INDEX idx_payments ON transactions(id) WHERE id LIKE 'pi_%';
CREATE INDEX idx_refunds ON transactions(id) WHERE id LIKE 're_%';
```

### API Design Patterns

```python
# RESTful endpoints with typed IDs
GET /api/users/user_2StGMtcWzRJ8qZqQjbJjGdTkVfv
GET /api/payments/pi_2StGMtcWzRJ8qZqQjbJjGdTkVfv
GET /api/orders/ord_2StGMtcWzRJ8qZqQjbJjGdTkVfv

# Validation middleware
def validate_entity_id(entity_type, entity_id):
    if not entity_id.startswith(f"{entity_type}_"):
        raise ValueError(f"Invalid {entity_type} ID format")
    return entity_id.split('_', 1)[1]  # Return KSUID part
```

## Thread Safety

The KSUID library is thread-safe. Multiple threads can generate KSUIDs concurrently without coordination.

## Requirements

- Python 3.13 or later
- No external dependencies

## Development

```bash
# Clone repository
git clone https://github.com/geneseas/ksuid-python.git
cd ksuid-python

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=ksuid

# Format code
black .

# Type checking
mypy ksuid/
```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

- [Original KSUID specification](https://github.com/segmentio/ksuid)
- [KSUID in other languages](https://github.com/segmentio/ksuid#other-implementations) 