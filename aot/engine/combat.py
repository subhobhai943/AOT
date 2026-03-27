"""Battle resolution helpers for Scout vs Titan encounters."""

from __future__ import annotations

import random

from aot.core.database import AoTDatabase


class CombatSimulator:
    """Resolve combat encounters by combining scout profile and titan threat data."""

    def __init__(self, database: AoTDatabase):
        self.database = database

    @staticmethod
    def _character_combat_score(character: dict) -> float:
        stats = character.get("stats", {})

        wits = float(stats.get("intelligence", 5))
        initiative = float(stats.get("agility", 5))
        combat = float(stats.get("strength", 5))

        return (wits * 0.35) + (initiative * 0.30) + (combat * 0.35)

    @staticmethod
    def _titan_threat_score(titan: dict) -> float:
        height = float(titan.get("height_m", 15))
        abilities = titan.get("special_abilities", [])
        ability_count = len(abilities) if isinstance(abilities, list) else 0
        return (height / 10.0) + (ability_count * 1.8)

    def simulate_encounter(self, character_name: str, titan_name: str) -> str:
        """Simulate an encounter and return a stylized narrative outcome string."""
        character = self.database.get_character(character_name)
        titan = self.database.get_titan(titan_name)

        scout_score = self._character_combat_score(character)
        titan_score = self._titan_threat_score(titan)

        # logistic-like squashing into [0.05, 0.95]
        raw_advantage = (scout_score - titan_score) / 12.0
        win_probability = max(0.05, min(0.95, 0.5 + raw_advantage))

        roll = random.random()
        full_name = character.get("full_name", character_name)
        titan_title = titan.get("name", titan_name)

        if roll <= win_probability * 0.7:
            return (
                f"⚔️ {full_name} rockets through the skyline, threads the thunder-spears, "
                f"and carves through the {titan_title}'s nape. Humanity roars in triumph!"
            )

        if roll <= win_probability:
            return (
                f"🛡️ {full_name} reads the {titan_title}'s movements and orders a tactical retreat. "
                "The Scout survives to fight another day."
            )

        if roll <= min(0.98, win_probability + 0.2):
            return (
                f"💥 The {titan_title} unleashes chaos. {full_name} barely escapes, gas spent and blades chipped."
            )

        return (
            f"☠️ In a brutal instant, the {titan_title} overwhelms {full_name}. "
            "The battlefield falls silent as another Scout is lost."
        )
