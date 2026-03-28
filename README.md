# 🪽 AOT-Toolkit — Offline Attack on Titan Python Toolkit

[![PyPI version](https://img.shields.io/pypi/v/AOT-Toolkit.svg)](https://pypi.org/project/AOT-Toolkit/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

**AOT-Toolkit** is a production-ready Python package for Attack on Titan fans and developers who want:

- 🧠 **Offline lore access** (characters, titans, quotes) with no API dependency.
- 🗡️ **ODM and combat simulation primitives** for games, experiments, and CLI storytelling.
- 🖥️ **A rich terminal UX** with side-by-side themed rendering and instant battle simulation.

---

## ✨ Highlights

- **Zero-network data access** via local JSON datasets.
- **Fuzzy lookup support** for character and titan names.
- **ODM gear model** with gas consumption and blade durability logic.
- **Combat narrative engine** that generates cinematic encounter reports.
- **CLI commands** for system+lore fetches and direct battle simulation.

---

## 📦 Installation

```bash
pip install AOT-Toolkit
```

---

## 🖥️ CLI Usage

After installation, the `aot` command is available globally.

### `aot fetch`

Displays a polished side-by-side output featuring:

- Wings of Freedom ASCII art
- System information (OS/kernel/CPU/RAM/uptime)
- Scout rank estimation
- Random quote from the offline database

```bash
aot fetch
```

### `aot battle [char_name] [titan_name]`

Runs the combat simulator directly from your terminal and prints a styled battle report.

```bash
aot battle "Levi Ackerman" "Beast Titan"
```

You can also use fuzzy names:

```bash
aot battle Levi Armored
```

---

## 🐍 Python API Usage

### 1) Database access (offline lore queries)

```python
from aot.core.database import AoTDatabase


db = AoTDatabase()

levi = db.get_character("Levi")
beast = db.get_titan("Beast")
quote = db.get_random_quote(tag="motivational")

print(levi["full_name"])
print(beast["name"], beast["special_abilities"])
print(f"{quote['character_name']}: {quote['quote_text']}")
```

### 2) Engine usage (ODM + combat)

```python
from aot.core.database import AoTDatabase
from aot.engine.combat import CombatSimulator
from aot.engine.odm_gear import ODMGear

# ODM simulation
gear = ODMGear(gas_capacity=100.0, blade_durability=100)
print(gear.grapple(distance_m=90.0, speed="fast"))

# Hardened armor affects blade durability significantly
strike = gear.attack_nape(
    titan_armor_level=4,
    titan_abilities=["hardened_armor", "high_endurance"],
)
print(strike)

# Combat narrative simulation
db = AoTDatabase()
simulator = CombatSimulator(db)
report = simulator.simulate_encounter("Mikasa Ackerman", "War Hammer Titan")
print(report)
```

---

## 🎬 Showcase Demo

A complete demonstration script is provided:

```bash
python examples/demo.py
```

The demo will:

1. Fetch and print a random quote.
2. Run a quick ODM grapple simulation and print gas usage.
3. Simulate **Levi Ackerman vs Beast Titan** and print the narrative result.

---

## 🧱 Project Structure

```text
.
├── aot/
│   ├── cli/                # Rich-powered terminal commands
│   ├── core/               # Offline database and exceptions
│   ├── data/               # Characters, titans, quotes JSON datasets
│   └── engine/             # ODM gear + combat simulation
├── examples/
│   └── demo.py             # End-to-end showcase script
├── tests/
├── .github/workflows/
│   └── publish-to-pypi.yml
├── pyproject.toml
└── README.md
```

---

## 🚀 Release & Publishing

The repository includes an automated GitHub Actions workflow to:

- Build source/wheel distributions on version tags (`v*`)
- Publish to **TestPyPI**
- Publish to **PyPI** on tag push

See: `.github/workflows/publish-to-pypi.yml`

---

## 🤝 Contributing

Contributions are welcome. If you submit PRs, please include:

- Unit tests for new behavior
- Clear docstrings and type hints
- Updated README snippets for public-facing API changes

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE).
