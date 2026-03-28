"""Battle resolution helpers for Scout vs Titan encounters."""

from __future__ import annotations

import random

from aot.core.database import AoTDatabase


class CombatSimulator:
    """Resolve combat encounters by combining scout profile and titan threat data."""

    ADVANTAGE_SCALING_FACTOR = 8.0

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

    @staticmethod
    def _format_ability_list(abilities: list[str]) -> str:
        if not abilities:
            return "no notable abilities"
        friendly = [ability.replace("_", " ") for ability in abilities]
        if len(friendly) == 1:
            return friendly[0]
        if len(friendly) == 2:
            return f"{friendly[0]} and {friendly[1]}"
        return ", ".join(friendly[:-1]) + f", and {friendly[-1]}"

    def simulate_encounter(self, character_name: str, titan_name: str) -> str:
        """Simulate an encounter and return a 3-4 sentence stylized narrative."""
        character = self.database.get_character(character_name)
        titan = self.database.get_titan(titan_name)

        scout_score = self._character_combat_score(character)
        titan_score = self._titan_threat_score(titan)

        raw_advantage = (scout_score - titan_score) / self.ADVANTAGE_SCALING_FACTOR
        win_probability = max(0.08, min(0.92, 0.5 + raw_advantage))

        roll = random.random()
        full_name = character.get("full_name", character_name)
        titan_title = titan.get("name", titan_name)
        titan_height = titan.get("height_m", "?")

        stats = character.get("stats", {})
        strength = int(stats.get("strength", 5))
        agility = int(stats.get("agility", 5))
        intelligence = int(stats.get("intelligence", 5))
        leadership = int(stats.get("leadership", 5))

        titan_abilities = titan.get("special_abilities", [])
        abilities_text = self._format_ability_list(titan_abilities if isinstance(titan_abilities, list) else [])

        opening = (
            f"🌆 {full_name} enters the engagement at rooftop altitude, facing the {titan_height}m {titan_title} "
            f"whose profile includes {abilities_text}."
        )
        tactical = (
            f"📊 Combat readout: STR {strength}/10, AGI {agility}/10, INT {intelligence}/10, LDR {leadership}/10; "
            f"computed scout index {scout_score:.2f} versus titan threat {titan_score:.2f}, "
            f"yielding a {win_probability * 100:.1f}% projected success rate."
        )

        if roll <= win_probability * 0.6:
            climax = (
                f"⚔️ Using a feint-and-spiral approach, {full_name} forces a blind angle and commits to a high-G nape pass, "
                "blades flashing in a single decisive arc."
            )
            resolution = (
                f"✅ The strike lands true; the {titan_title} collapses and the squad channel marks the operation as a clean victory."
            )
            return " ".join([opening, tactical, climax, resolution])

        if roll <= win_probability:
            climax = (
                f"🛡️ {full_name} recognizes the threat curve mid-flight, aborts the kill line, and pivots into evasive cover to preserve gas and steel."
            )
            resolution = (
                f"↩️ No kill confirmed, but the {titan_title} is outmaneuvered long enough for allies to reposition; the encounter ends as a tactical survival."
            )
            return " ".join([opening, tactical, climax, resolution])

        if roll <= min(0.98, win_probability + 0.2):
            climax = (
                f"💥 The {titan_title} counters with brutal timing, clipping {full_name}'s attack lane and shredding momentum at close range."
            )
            resolution = (
                "⚠️ Severe gear strain and near-fatal pressure force an emergency disengage, leaving the battlefield unresolved and dangerously contested."
            )
            return " ".join([opening, tactical, climax, resolution])

        climax = (
            f"☠️ A catastrophic read error opens a narrow window that the {titan_title} exploits instantly, overwhelming {full_name} before a recovery route forms."
        )
        resolution = (
            "🕯️ Signal flares fade over the district as command records a total loss and postpones further assault until reinforcement arrives."
        )
        return " ".join([opening, tactical, climax, resolution])
