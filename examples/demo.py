"""Showcase demo for AOT-Toolkit.

Run with:
    python examples/demo.py

This script demonstrates three key capabilities:
1) Offline lore lookup via AoTDatabase.
2) ODM movement simulation via ODMGear.
3) Narrative combat simulation via CombatSimulator.
"""

from __future__ import annotations

from aot.core.database import AoTDatabase
from aot.engine.combat import CombatSimulator
from aot.engine.odm_gear import ODMGear


def main() -> None:
    """Execute a complete showcase pass of the toolkit."""
    # Initialize the singleton offline database. This does not require network calls.
    db = AoTDatabase()

    print("=" * 72)
    print("🪽  AOT-Toolkit v1.0.0 Showcase Demo")
    print("=" * 72)

    # ---------------------------------------------------------------------
    # 1) Pull and display a random quote from the local JSON quote dataset.
    # ---------------------------------------------------------------------
    quote = db.get_random_quote()
    print("\n📚 Random Quote")
    print(f'   "{quote["quote_text"]}"')
    print(f'   — {quote["character_name"]} ({quote["episode_reference"]})')

    # ---------------------------------------------------------------------
    # 2) Simulate a short ODM grapple sequence and report gas usage metrics.
    # ---------------------------------------------------------------------
    gear = ODMGear(gas_capacity=100.0, blade_durability=100)
    grapple_result = gear.grapple(distance_m=85.0, speed="fast")

    print("\n⚙️  ODM Grapple Simulation")
    print(f"   Distance: 85.0m @ fast profile")
    print(f"   Gas Used: {grapple_result['gas_used']}")
    print(f"   Time Taken: {grapple_result['time_taken']} seconds")
    print(f"   Remaining Gas: {gear.gas_capacity}")

    # ---------------------------------------------------------------------
    # 3) Simulate a canonical high-threat battle and print the narrative.
    # ---------------------------------------------------------------------
    simulator = CombatSimulator(database=db)
    narrative = simulator.simulate_encounter("Levi Ackerman", "Beast Titan")

    print("\n⚔️  Combat Simulation")
    print("   Levi Ackerman vs Beast Titan")
    print(f"\n{narrative}")

    print("\n" + "=" * 72)
    print("✅ Demo complete. Try: aot fetch  |  aot battle 'Levi Ackerman' 'Beast Titan'")
    print("=" * 72)


if __name__ == "__main__":
    main()
