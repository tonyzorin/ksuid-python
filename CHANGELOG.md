# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-06

### Added
- Lowercase base36 encoding (`0-9a-z`, 31 characters) for case-insensitive contexts
- `KSUID.to_base36()` / `KSUID.from_base36()` instance and class methods
- `generate_lowercase()` — sortable KSUID as lowercase base36 string
- `generate_token()` — secure 160-bit random token (no timestamp), base62
- `generate_token_lowercase()` — secure 160-bit random token, base36
- `from_base36()` module-level convenience function
- `__slots__` on KSUID class for memory efficiency
- Thread-safety tests (concurrent generation across 4 threads)
- CI matrix: Python 3.9, 3.10, 3.11, 3.12, 3.13, 3.14
- CLI `--count` upper bound (1,000,000) to prevent memory exhaustion
- Edge-case tests: zero-value round-trip, max-timestamp round-trip, base62 overflow

### Fixed
- `_base62_decode` raised uncontrolled `OverflowError` on crafted input exceeding 20-byte max; now raises `ValueError`
- `_base62_encode` returned single-char `"0"` for all-zero input instead of 27-char padded string
- `__eq__` returned `False` instead of `NotImplemented` for non-KSUID types
- `PrefixedKSUID.create` allowed underscores in prefixes but `parse` couldn't round-trip them
- CI workflow referenced nonexistent `python -m ksuid.cli` module path
- KSUID epoch comment said "January 1, 2014" but value is May 13, 2014
- Flaky smoke test using 1ms sleep for 1-second resolution timestamps
- Unicode emoji in print statements caused `UnicodeEncodeError` on Windows (cp1252)
- `_validate_count` raised `ValueError` instead of `ArgumentTypeError` for non-numeric input

### Changed
- **BREAKING**: Renamed `__init__.py` to `ksuid.py` (fixes Windows imports; `from ksuid import ...` still works)
- Minimum Python version lowered from 3.13 to 3.9
- `_base62_decode` uses O(1) dict lookup instead of O(n) `str.index()`
- `create_api_key()` / `create_session_id()` now use `generate_token()` (no timestamp leakage)
- Upgraded `actions/setup-python` from v4 to v5
- Removed `sys.path.insert` hacks from all files
- Applied `black` formatting across entire codebase

### Security
- `generate_token()` / `generate_token_lowercase()` use `secrets.token_bytes` for 160-bit entropy with no embedded timestamp
- Added security warnings to `create_api_key()` / `create_session_id()` docstrings

## [1.0.0] - 2025-07-02

### Added
- Initial release of KSUID Python implementation
- Core KSUID class with 20-byte identifiers (4-byte timestamp + 16-byte payload)
- Base62 encoding/decoding for URL-safe string representation
- Comprehensive comparison operators (<, <=, >, >=, ==, !=)
- Thread-safe KSUID generation
- Zero external dependencies
- Command-line interface (CLI) with generate, inspect, compare, and benchmark commands
- Stripe-style prefixed ID examples and utilities
- Comprehensive test suite
- Performance benchmarks
- Complete API documentation and usage examples

### Compatibility
- Python 3.13+ support
- Cross-platform compatibility (Windows, macOS, Linux)
- Thread-safe concurrent generation
- Hashable for use in sets and dictionaries

[2.0.0]: https://github.com/tonyzorin/ksuid-python/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/tonyzorin/ksuid-python/releases/tag/v1.0.0
