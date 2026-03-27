"""ODM gear simulation primitives for movement and nape attacks."""

from __future__ import annotations

from dataclasses import dataclass


class OutOfGasError(RuntimeError):
    """Raised when ODM gas reserves are insufficient for a maneuver."""


class BrokenBladeError(RuntimeError):
    """Raised when blades are too damaged to continue attacking."""


@dataclass
class ODMGear:
    """Simulate ODM gear resource usage and combat wear."""

    gas_capacity: float = 100.0
    blade_durability: int = 100

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

    def attack_nape(self, titan_armor_level: int) -> dict[str, int | str]:
        """Strike a titan's nape, reducing blade durability by armor resistance."""
        if titan_armor_level < 0:
            raise ValueError("titan_armor_level must be >= 0")
        wear = max(self.MIN_WEAR, self.BASE_WEAR + titan_armor_level * self.ARMOR_WEAR_MULTIPLIER)
        damage_dealt = max(self.MIN_DAMAGE, self.BASE_DAMAGE - titan_armor_level * self.ARMOR_DAMAGE_REDUCTION)
        damage_dealt = max(1, 40 - titan_armor_level * 3)

        remaining = self.blade_durability - wear
        if remaining <= 0:
            self.blade_durability = 0
            raise BrokenBladeError("Blade shattered during nape strike.")

        self.blade_durability = remaining
        return {
            "damage_dealt": damage_dealt,
            "remaining_durability": self.blade_durability,
            "status": "Nape strike landed cleanly.",
        }
