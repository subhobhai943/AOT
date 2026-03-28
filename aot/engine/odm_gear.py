"""ODM gear simulation primitives for movement and nape attacks."""

from __future__ import annotations

from dataclasses import dataclass


class OutOfGasError(RuntimeError):
    """Raised when ODM gas reserves are insufficient for a maneuver."""


class BrokenBladeError(RuntimeError):
    """Raised when blades are too damaged to continue attacking."""


@dataclass
class ODMGear:
    """Simulate ODM gear resource usage and combat wear.

    The model intentionally balances readability with game-ready behavior:
    - Grapple gas consumption scales with distance and speed profile.
    - Nape attacks reduce durability by armor resistance.
    - Titans with hardening traits dramatically increase blade wear.
    """

    gas_capacity: float = 100.0
    blade_durability: int = 100

    BASE_WEAR: int = 8
    MIN_WEAR: int = 4
    ARMOR_WEAR_MULTIPLIER: int = 3
    HARDENED_ARMOR_MULTIPLIER: float = 2.35

    BASE_DAMAGE: int = 46
    MIN_DAMAGE: int = 6
    ARMOR_DAMAGE_REDUCTION: int = 3

    def __post_init__(self) -> None:
        if self.gas_capacity < 0:
            raise ValueError("gas_capacity must be >= 0")
        if self.blade_durability < 0:
            raise ValueError("blade_durability must be >= 0")

    def grapple(self, distance_m: float, speed: str = "normal") -> dict[str, float | str]:
        """Perform a grapple maneuver and consume gas based on distance and speed.

        Speed profiles:
        - normal: baseline gas usage and travel speed
        - fast: moderate gas increase with shorter travel time
        - burst: heavy gas burn and fastest travel time
        """
        if distance_m <= 0:
            raise ValueError("distance_m must be > 0")

        speed_profile = {
            "normal": {"gas_per_meter": 0.35, "m_per_sec": 28.0},
            "fast": {"gas_per_meter": 0.5, "m_per_sec": 40.0},
            "burst": {"gas_per_meter": 0.8, "m_per_sec": 60.0},
        }

        mode = speed.strip().casefold()
        if mode not in speed_profile:
            raise ValueError("speed must be one of: normal, fast, burst")

        gas_used = round(distance_m * speed_profile[mode]["gas_per_meter"], 2)
        projected_gas = self.gas_capacity - gas_used
        if projected_gas < 0:
            raise OutOfGasError(
                f"ODM gas depleted: required {gas_used}, available {self.gas_capacity}"
            )

        self.gas_capacity = round(projected_gas, 2)
        time_taken = round(distance_m / speed_profile[mode]["m_per_sec"], 2)

        return {
            "gas_used": gas_used,
            "time_taken": time_taken,
            "status": f"Grapple successful at {mode} speed. Remaining gas: {self.gas_capacity}",
        }

    @staticmethod
    def _has_hardened_armor(titan_abilities: list[str] | tuple[str, ...] | None) -> bool:
        if not titan_abilities:
            return False

        normalized = {ability.strip().casefold() for ability in titan_abilities if isinstance(ability, str)}
        hardened_signatures = {
            "hardened_armor",
            "advanced_hardening",
            "hardening",
            "hardened_jaws",
            "hardened_claws",
        }
        return bool(normalized.intersection(hardened_signatures))

    def attack_nape(
        self,
        titan_armor_level: int,
        titan_abilities: list[str] | tuple[str, ...] | None = None,
    ) -> dict[str, int | str | bool]:
        """Strike a titan's nape, reducing blade durability by armor resistance.

        Args:
            titan_armor_level: Integer armor resistance (0 = none).
            titan_abilities: Optional titan abilities to detect hardening traits.

        Returns:
            A result payload describing damage output and durability state.
        """
        if titan_armor_level < 0:
            raise ValueError("titan_armor_level must be >= 0")

        hardened_armor = self._has_hardened_armor(titan_abilities)

        base_wear = self.BASE_WEAR + titan_armor_level * self.ARMOR_WEAR_MULTIPLIER
        wear = max(self.MIN_WEAR, base_wear)
        if hardened_armor:
            wear = int(round(wear * self.HARDENED_ARMOR_MULTIPLIER))

        damage_dealt = self.BASE_DAMAGE - titan_armor_level * self.ARMOR_DAMAGE_REDUCTION
        if hardened_armor:
            damage_dealt -= 6
        damage_dealt = max(self.MIN_DAMAGE, damage_dealt)

        remaining = self.blade_durability - wear
        if remaining <= 0:
            self.blade_durability = 0
            raise BrokenBladeError(
                "Blade shattered during nape strike; hardened armor overwhelmed the edge."
                if hardened_armor
                else "Blade shattered during nape strike."
            )

        self.blade_durability = remaining
        return {
            "damage_dealt": damage_dealt,
            "durability_cost": wear,
            "remaining_durability": self.blade_durability,
            "hardened_armor_detected": hardened_armor,
            "status": "Nape strike landed cleanly.",
        }
