"""CLI entry point for the aot toolkit."""

from __future__ import annotations

import argparse
from typing import Sequence

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from aot.cli.art import WINGS_OF_FREEDOM
from aot.cli.fetch import calculate_scout_rank, get_system_info
from aot.core.database import AoTDatabase


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
    return parser


def _handle_fetch(_: argparse.Namespace) -> int:
    console = Console()
    db = AoTDatabase()
    quote = db.get_random_quote()
    system_info = get_system_info()
    scout_rank = calculate_scout_rank(system_info["ram_gb"])

    art_block = Text(WINGS_OF_FREEDOM, style="bold green")

    detail_lines = [
        "[bold cyan]System Intel[/bold cyan]",
        f"[bold]OS:[/bold] {system_info['os']}",
        f"[bold]Kernel:[/bold] {system_info['kernel_version']}",
        f"[bold]CPU:[/bold] {system_info['cpu_name']}",
        f"[bold]RAM:[/bold] {system_info['total_ram']}",
        f"[bold]Uptime:[/bold] {system_info['uptime']}",
        f"[bold]Scout Rank:[/bold] {scout_rank}",
        "",
        "[bold magenta]Quote of the Day[/bold magenta]",
        f"[bold]\"{quote['quote_text']}\"[/bold]",
        f"— {quote['character_name']} ({quote['episode_reference']})",
    ]

    info_panel = Panel(
        "\n".join(detail_lines),
        title="[bold]AoT Fetch[/bold]",
        border_style="bright_blue",
        padding=(1, 2),
    )

    console.print(Columns([art_block, info_panel], expand=True, equal=False))
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
