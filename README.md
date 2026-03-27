# 🪽 aot — Attack on Titan Python Toolkit

![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Build Status](https://github.com/your-org/aot/actions/workflows/python-app.yml/badge.svg)

A comprehensive Python library for the Attack on Titan universe. Features a complete offline data API, a physics engine for game development, and productivity-focused CLI utilities.

---

## Why `aot`?

`aot` is built for developers who want a clean, modular toolkit with zero external web calls for core lore data, a rich terminal experience, and extensible simulation primitives for game mechanics.

### Highlights

- 📚 **Offline Data API** for characters, titans, and quotes.
- 🖥️ **CLI Experience** with `aot fetch` for stylized system + lore output.
- ⚙️ **Game Physics Layer** with ODM movement and combat simulation.
- 🧩 **Modular Architecture** designed for growth into CLI/game tooling.

---

## Installation

```bash
pip install .
```

---

## CLI Usage

Run the themed fetch view (similar spirit to `neofetch`):

```bash
aot fetch
```

Expected output includes:

- Scout Regiment ASCII art
- System information (OS, kernel, CPU, RAM, uptime, rank)
- A random AoT quote from the offline database

---

## Data API Usage

```python
from aot.core.database import AoTDatabase

db = AoTDatabase()
quote = db.get_random_quote(tag="motivational")
print(f"{quote['character_name']}: {quote['quote_text']}")
```

---

## Game Engine Usage

```python
from aot.core.database import AoTDatabase
from aot.engine.combat import CombatSimulator
from aot.engine.odm_gear import ODMGear

# ODM physics/resource simulation
gear = ODMGear(gas_capacity=100.0, blade_durability=100)
print(gear.grapple(distance_m=120.0, speed="fast"))

# Combat simulation using offline data
db = AoTDatabase()
sim = CombatSimulator(database=db)
outcome = sim.simulate_encounter("Levi", "Armored")
print(outcome)
```

---

## Project Structure

```text
.
├── aot/
│   ├── core/       # Offline database engine
│   ├── cli/        # Terminal UI and commands
│   ├── engine/     # Physics and combat simulation
│   └── data/       # JSON lore datasets
├── tests/
├── .github/workflows/
└── pyproject.toml
```

---

## License

MIT License. See `LICENSE` for details.
