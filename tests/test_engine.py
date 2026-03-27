from aot.core.database import AoTDatabase
from aot.engine.combat import CombatSimulator
from aot.engine.odm_gear import BrokenBladeError, ODMGear, OutOfGasError


def test_grapple_uses_gas() -> None:
    gear = ODMGear(gas_capacity=100.0)
    result = gear.grapple(distance_m=50.0, speed="normal")
    assert result["gas_used"] > 0
    assert gear.gas_capacity < 100.0


def test_grapple_out_of_gas_raises() -> None:
    gear = ODMGear(gas_capacity=1.0)
    try:
        gear.grapple(distance_m=100.0, speed="burst")
    except OutOfGasError:
        pass
    else:
        raise AssertionError("Expected OutOfGasError")


def test_attack_nape_can_break_blade() -> None:
    gear = ODMGear(blade_durability=8)
    try:
        gear.attack_nape(titan_armor_level=4)
    except BrokenBladeError:
        pass
    else:
        raise AssertionError("Expected BrokenBladeError")


def test_combat_simulator_returns_text() -> None:
    simulator = CombatSimulator(database=AoTDatabase())
    outcome = simulator.simulate_encounter("Levi", "Armored")
    assert isinstance(outcome, str)
    assert outcome
