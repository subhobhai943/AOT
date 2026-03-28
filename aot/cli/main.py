"""CLI entry point for the aot toolkit."""

from __future__ import annotations

import argparse
from typing import Sequence

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from aot.cli.art import WINGS_OF_FREEDOM
from aot.cli.fetch import calculate_scout_rank, get_system_info
from aot.core.database import AoTDatabase
from aot.core.exceptions import AoTException
from aot.engine.combat import CombatSimulator


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aot",
        description="Attack on Titan developer toolkit.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch_parser = subparsers.add_parser(
        "fetch",
        help="Display system information and AoT flavor text.",
    )
    fetch_parser.set_defaults(handler=_handle_fetch)

    battle_parser = subparsers.add_parser(
        "battle",
        help="Simulate a Scout-versus-Titan encounter.",
    )
    battle_parser.add_argument("char_name", help="Character name, e.g. 'Levi Ackerman' or 'Levi'.")
    battle_parser.add_argument("titan_name", help="Titan name, e.g. 'Beast Titan' or 'Armored'.")
    battle_parser.set_defaults(handler=_handle_battle)
    return parser


def _build_fetch_layout() -> Columns:
    db = AoTDatabase()
    quote = db.get_random_quote()
    system_info = get_system_info()
    scout_rank = calculate_scout_rank(system_info["ram_gb"])

    art_panel = Panel(
        Text(WINGS_OF_FREEDOM, style="bold green"),
        title="[bold bright_green]Wings of Freedom[/bold bright_green]",
        border_style="green",
        padding=(1, 2),
    )

    info_table = Table.grid(padding=(0, 1))
    info_table.add_row("[bold cyan]OS[/bold cyan]", str(system_info["os"]))
    info_table.add_row("[bold cyan]Kernel[/bold cyan]", str(system_info["kernel_version"]))
    info_table.add_row("[bold cyan]CPU[/bold cyan]", str(system_info["cpu_name"]))
    info_table.add_row("[bold cyan]RAM[/bold cyan]", str(system_info["total_ram"]))
    info_table.add_row("[bold cyan]Uptime[/bold cyan]", str(system_info["uptime"]))
    info_table.add_row("[bold cyan]Scout Rank[/bold cyan]", f"[bold yellow]{scout_rank}[/bold yellow]")

    quote_text = Text()
    quote_text.append('"', style="bold")
    quote_text.append(quote["quote_text"], style="italic magenta")
    quote_text.append('"', style="bold")
    quote_text.append(f"\n— {quote['character_name']} ({quote['episode_reference']})", style="bright_white")

    right_column = Columns(
        [
            Panel(info_table, title="[bold]System Intel[/bold]", border_style="bright_blue", padding=(1, 2)),
            Panel(quote_text, title="[bold]Quote of the Day[/bold]", border_style="magenta", padding=(1, 2)),
        ],
        expand=True,
        equal=True,
    )

    return Columns([art_panel, right_column], expand=True, equal=True, padding=(1, 2))


def _handle_fetch(_: argparse.Namespace) -> int:
    console = Console()
    console.print(_build_fetch_layout())
    return 0


def _handle_battle(args: argparse.Namespace) -> int:
    console = Console()
    db = AoTDatabase()
    simulator = CombatSimulator(database=db)

    try:
        narrative = simulator.simulate_encounter(args.char_name, args.titan_name)
    except AoTException as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        return 2

    console.print(
        Panel(
            narrative,
            title=f"[bold]Battle Report[/bold] — {args.char_name} vs {args.titan_name}",
            border_style="red",
            padding=(1, 2),
        )
    )
    return 0


def app(argv: Sequence[str] | None = None) -> int:
    """Run the `aot` command-line application."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 1
    return int(handler(args))


if __name__ == "__main__":
    raise SystemExit(app())
