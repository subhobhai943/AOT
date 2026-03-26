# aot

![Build Status](https://github.com/your-org/aot/actions/workflows/python-app.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A comprehensive Python library for the Attack on Titan universe. Features a complete offline data API, a physics engine for game development, and productivity-focused CLI utilities.

---

## Why `aot`?

`aot` is designed as a modular, batteries-included toolkit for fans and developers building Attack on Titan-inspired projects. Phase 1 focuses on a fast offline data engine, clean documentation, and CI/CD foundations.

## Features (Phase 1)

- ✅ Offline JSON-backed database for characters, titans, and quotes.
- ✅ Structured core module with custom exception handling.
- ✅ Fuzzy, case-insensitive lookups.
- ✅ Tag- and character-filtered random quote retrieval.
- ✅ CI pipeline across Python 3.10–3.12.

## Installation

```bash
pip install aot
```

> For local development:

```bash
pip install -e .
```

## Quick Start

```python
from aot.core.database import AoTDatabase

# Singleton instance
db = AoTDatabase()

character = db.get_character("levi")
print(character["full_name"])  # Levi Ackerman

titan = db.get_titan("attack")
print(titan["name"])  # Attack Titan

quote = db.get_random_quote(tag="motivational")
print(f"{quote['character_name']}: {quote['quote_text']}")
```

## Project Layout

```text
.
├── .github/
│   └── workflows/
│       └── python-app.yml
├── aot/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── exceptions.py
│   └── data/
│       ├── characters.json
│       ├── titans.json
│       └── quotes.json
├── tests/
│   └── test_database.py
├── pyproject.toml
└── README.md
```

## Roadmap

- Phase 1: Core Data Engine, Documentation, CI/CD
- Phase 2: CLI and command set expansion
- Phase 3: Physics engine and gameplay simulation modules

## License

MIT License. See `LICENSE` for details.
