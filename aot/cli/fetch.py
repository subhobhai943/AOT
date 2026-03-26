"""System information helpers for the `aot fetch` command."""

from __future__ import annotations

import platform
import time
from datetime import timedelta
from typing import Any

import psutil


def calculate_scout_rank(ram_gb: int) -> str:
    """Map RAM capacity to a Scout Regiment rank."""
    if ram_gb > 16:
        return "Commander"
    if 8 <= ram_gb <= 16:
        return "Captain"
    return "Cadet"


def _format_uptime(seconds: float) -> str:
    uptime = timedelta(seconds=int(seconds))
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    return f"{days}d {hours}h {minutes}m"


def get_system_info() -> dict[str, Any]:
    """Collect host system information for rendering in the CLI."""
    total_ram_bytes = psutil.virtual_memory().total
    total_ram_gb = int(total_ram_bytes / (1024**3))

    info: dict[str, Any] = {
        "os": platform.system(),
        "kernel_version": platform.release(),
        "cpu_name": platform.processor() or "Unknown CPU",
        "total_ram": f"{total_ram_gb} GB",
        "uptime": _format_uptime(time.time() - psutil.boot_time()),
        "ram_gb": total_ram_gb,
    }
    return info
