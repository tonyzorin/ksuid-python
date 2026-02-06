# KSUID - K-Sortable Unique Identifier

[![Python Version](https://img.shields.io/pypi/pyversions/ksuid-python.svg)](https://pypi.org/project/ksuid-python/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python implementation of [KSUID](https://github.com/segmentio/ksuid) (K-Sortable Unique Identifier) for Python 3.9+.

## What is a KSUID?

A KSUID is a globally unique identifier similar to a UUID, but with better properties:

- **Sortable**: KSUIDs are naturally sortable by creation time
- **Compact**: 27 characters when base62-encoded (vs 36 for UUID)
- **URL-safe**: Uses base62 encoding (no special characters)
- **Collision-resistant**: 128 bits of randomness per second
- **Time-based**: Encodes creation timestamp for easy debugging
- **Prefix-friendly**: Can be prefixed for type identification (like Stripe's API keys)
- **Lowercase option**: Base36 encoding for case-insensitive contexts (31 characters)
- **Secure tokens**: Generate timestamp-free tokens with 160 bits of entropy
- **Thread-safe**: Safe for concurrent use across multiple threads

## Format

A KSUID is a 20-byte identifier consisting of:
- **4 bytes**: Timestamp (seconds since KSUID epoch: 2014-05-13 16:53:20 UTC)
- **16 bytes**: Random payload

| Encoding | Characters | Alphabet | Use case |
|----------|-----------|----------|----------|
| Base62 (default) | 27 | `0-9A-Za-z` | Standard, compact |
| Base36 (lowercase) | 31 | `0-9a-z` | Case-insensitive systems |

## Quick Start

```python
from ksuid import KSUID, generate, generate_lowercase

# Generate a new KSUID (base62, mixed-case)
ksuid = generate()
print(ksuid)  # 2StGMtcWzRJ8qZqQjbJjGdTkVfv

# Generate a lowercase KSUID (base36)
lower_id = generate_lowercase()
print(lower_id)  # 0c7de9014xkr8gqp3n7ewbz5jhr

# Create from string
ksuid2 = KSUID.from_string("2StGMtcWzRJ8qZqQjbJjGdTkVfv")

# Convert between formats
ksuid = KSUID()
str(ksuid)          # Base62: "2StGMtcWzRJ8qZqQjbJjGdTkVfv" (27 chars)
ksuid.to_base36()   # Base36: "0c7de9014xkr8gqp3n7ewbz5jhr" (31 chars)

# KSUIDs are sortable
ksuid_a = KSUID(timestamp=1609459200)
ksuid_b = KSUID(timestamp=1609459201)
assert ksuid_a < ksuid_b  # True!

# Access timestamp and payload
print(ksuid.datetime)       # 2025-01-17 10:30:45+00:00
print(ksuid.timestamp)      # 1737108645
print(len(ksuid.payload))   # 16 bytes
```

## Secure Tokens

For API keys, session tokens, and other security-sensitive values, use
`generate_token()` or `generate_token_lowercase()`. These use 160 bits of
`secrets.token_bytes` randomness with **no embedded timestamp**, so creation
time cannot be leaked.

```python
from ksuid import generate_token, generate_token_lowercase

# Mixed-case token (27 chars, base62, 160-bit entropy)
api_key = f"sk_{generate_token()}"
# sk_7kQ9xLm3RtN5vW8yBzCdEfGhJ

# Lowercase token (31 chars, base36, 160-bit entropy)
session = f"sess_{generate_token_lowercase()}"
# sess_4f8a2bc90d1e3f5g6h7i8j9k0lm
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

| Method | Description |
|--------|-------------|
| `KSUID.from_string(s)` | Create from 27-char base62 string |
| `KSUID.from_base36(s)` | Create from 31-char lowercase base36 string |
| `KSUID.from_bytes(data)` | Create from raw 20-byte data |

#### Properties

| Property | Type | Description |
|----------|------|-------------|
| `timestamp` | `int` | Unix timestamp |
| `datetime` | `datetime` | UTC datetime object |
| `payload` | `bytes` | 16-byte random payload |
| `bytes` | `bytes` | Raw 20-byte KSUID data |

#### Methods

| Method | Description |
|--------|-------------|
| `__str__()` | Base62-encoded string (27 chars) |
| `to_base36()` | Base36-encoded lowercase string (31 chars) |
| `__repr__()` | Developer-friendly representation |
| `__hash__()` | Hashable (usable in sets/dicts) |
| `<`, `<=`, `>`, `>=`, `==`, `!=` | Sortable comparison |

### Convenience Functions

| Function | Returns | Description |
|----------|---------|-------------|
| `generate()` | `KSUID` | New KSUID with current timestamp |
| `generate_lowercase()` | `str` | 31-char lowercase base36 KSUID (sortable) |
| `generate_token()` | `str` | 27-char base62 secure token (no timestamp) |
| `generate_token_lowercase()` | `str` | 31-char base36 secure token (no timestamp) |
| `from_string(s)` | `KSUID` | Parse base62 string |
| `from_base36(s)` | `KSUID` | Parse base36 string |
| `from_bytes(data)` | `KSUID` | Parse raw bytes |

## Examples

### Prefixed IDs (Stripe-Style)

```python
from ksuid import generate, generate_lowercase

# Mixed-case prefixed IDs
user_id = f"user_{generate()}"      # user_2StGMtcWzRJ8qZqQjbJjGdTkVfv
payment_id = f"pi_{generate()}"     # pi_2StGMtcWzRJ8qZqQjbJjGdTkVfv

# Lowercase prefixed IDs
user_id = f"user_{generate_lowercase()}"   # user_0c7de9014xkr8gqp3n7ewbz5jhr
order_id = f"ord_{generate_lowercase()}"   # ord_0c7de9014xkr8gqp3n7ewbz5jhr
```

### Secure API Keys and Session Tokens

```python
from ksuid import generate_token, generate_token_lowercase

# API keys (no timestamp leakage, 160-bit entropy)
secret_key = f"sk_{generate_token()}"
public_key = f"pk_{generate_token()}"

# Lowercase session tokens
session_id = f"sess_{generate_token_lowercase()}"
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
from ksuid import KSUID, generate

# Generate KSUIDs with different timestamps
ksuids = [KSUID(timestamp=1609459200 + i) for i in range(5)]

# They're naturally sorted by creation time
sorted_ksuids = sorted(ksuids)
assert ksuids == sorted_ksuids  # True!

# Use in data structures
ksuid_set = set(ksuids)
ksuid_dict = {k: f"value_{i}" for i, k in enumerate(ksuids)}
```

### Converting Between Formats

```python
from ksuid import KSUID, from_base36

# Start with a KSUID
ksuid = KSUID()

# Get different representations
b62 = str(ksuid)             # Base62: 27 chars
b36 = ksuid.to_base36()      # Base36: 31 chars, lowercase
raw = ksuid.bytes             # Raw: 20 bytes

# Recreate from any representation
assert KSUID.from_string(b62) == ksuid
assert KSUID.from_base36(b36) == ksuid
assert KSUID.from_bytes(raw) == ksuid
```

### Database Usage

```python
from ksuid import generate_lowercase
import sqlite3

conn = sqlite3.connect(':memory:')
conn.execute('''
    CREATE TABLE users (
        id TEXT PRIMARY KEY,
        name TEXT
    )
''')

user_id = f"user_{generate_lowercase()}"
conn.execute(
    'INSERT INTO users (id, name) VALUES (?, ?)',
    (user_id, 'John Doe')
)
```

## Performance

KSUIDs are designed to be fast and efficient:

- **Generation**: ~1-2 microseconds per KSUID
- **Parsing**: ~500 nanoseconds from string
- **Comparison**: ~100 nanoseconds
- **Memory**: Optimized with `__slots__` (~48 bytes per instance)

## Comparison with UUIDs

| Feature | KSUID | UUID v4 | Stripe IDs |
|---------|-------|---------|------------|
| Length | 27 chars (base62) / 31 chars (base36) | 36 chars | 24-28 chars |
| Sortable | Yes | No | No |
| URL-safe | Yes | No (hyphens) | Yes |
| Timestamp | Readable | No | No |
| Collision resistance | High (128 bits) | High (122 bits) | High |
| Lowercase option | Yes (base36) | Yes (already) | No |
| Secure tokens | Yes (`generate_token`) | No | No |
| Thread-safe | Yes | Yes | Yes |

## Thread Safety

The KSUID library is fully thread-safe. All functions use only thread-safe
primitives (`os.urandom`, `secrets.token_bytes`, `time.time`) and KSUID
instances are immutable after construction. Safe even under free-threaded
Python 3.13+ (no-GIL).

## Requirements

- Python 3.9 or later
- No external dependencies

## Development

```bash
# Clone repository
git clone https://github.com/tonyzorin/ksuid-python.git
cd ksuid-python

# Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# Run tests
pytest test_ksuid.py -v

# Run tests with coverage
pytest test_ksuid.py --cov=ksuid

# Format code
black .

# Lint
flake8 . --max-line-length=88 --extend-ignore=E203,W503
```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

- [Original KSUID specification](https://github.com/segmentio/ksuid)
- [KSUID in other languages](https://github.com/segmentio/ksuid#other-implementations)
