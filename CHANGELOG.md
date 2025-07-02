# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Comprehensive test suite with 268 test cases
- Performance benchmarks (459,856+ KSUIDs/second with Python 3.13)
- Complete API documentation and usage examples
- Production-ready Flask API examples
- Database integration examples (SQLite)
- Industry adoption documentation and best practices

### Performance
- Generation: 459,856 KSUIDs/second
- String parsing: 136,803 parses/second  
- Bytes parsing: 821,620 parses/second
- Comparisons: 4.7M comparisons/second

### Compatibility
- Python 3.13+ support
- Cross-platform compatibility (Windows, macOS, Linux)
- Thread-safe concurrent generation
- Hashable for use in sets and dictionaries

[1.0.0]: https://github.com/tototheo/ksuid-python/releases/tag/v1.0.0
