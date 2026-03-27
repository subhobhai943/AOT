"""Singleton JSON-backed offline database for Attack on Titan data."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any

from aot.core.exceptions import (
    CharacterNotFoundError,
    QuoteNotFoundError,
    TitanNotFoundError,
)


class AoTDatabase:
    """Singleton data manager that lazily loads AoT JSON data into memory."""

    _instance: AoTDatabase | None = None

    def __new__(cls) -> AoTDatabase:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return

        self._data_path = Path(__file__).resolve().parent.parent / "data"
        self._characters = self._load_json("characters.json")
        self._titans = self._load_json("titans.json")
        self._quotes = self._load_json("quotes.json")
        self._initialized = True

    def _load_json(self, filename: str) -> list[dict[str, Any]]:
        file_path = self._data_path / filename
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError(f"Expected list in {filename}, got {type(data).__name__}")
        return data

    @staticmethod
    def _normalize(value: str) -> str:
        return value.strip().casefold()

    @classmethod
    def _matches(cls, needle: str, haystack: str) -> bool:
        normalized_needle = cls._normalize(needle)
        normalized_haystack = cls._normalize(haystack)
        return (
            normalized_needle == normalized_haystack
            or normalized_needle in normalized_haystack
            or normalized_haystack in normalized_needle
        )

    def get_character(self, name: str) -> dict[str, Any]:
        """Return a character by case-insensitive fuzzy match against full_name."""
        for character in self._characters:
            if self._matches(name, str(character.get("full_name", ""))):
                return character
        raise CharacterNotFoundError(f"Character not found: {name}")

    def get_titan(self, name: str) -> dict[str, Any]:
        """Return a titan by case-insensitive fuzzy match against name."""
        for titan in self._titans:
            if self._matches(name, str(titan.get("name", ""))):
                return titan
        raise TitanNotFoundError(f"Titan not found: {name}")

    def get_random_quote(self, character: str | None = None, tag: str | None = None) -> dict[str, Any]:
        """Return a random quote, optionally filtered by character and/or vibe tag."""
        filtered_quotes = self._quotes

        if character:
            filtered_quotes = [
                quote
                for quote in filtered_quotes
                if self._matches(character, str(quote.get("character_name", "")))
            ]

        if tag:
            normalized_tag = self._normalize(tag)
            filtered_quotes = [
                quote
                for quote in filtered_quotes
                if any(self._normalize(str(existing_tag)) == normalized_tag for existing_tag in quote.get("vibe_tags", []))
            ]

        if not filtered_quotes:
            filters = []
            if character:
                filters.append(f"character={character!r}")
            if tag:
                filters.append(f"tag={tag!r}")
            detail = ", ".join(filters) if filters else "no filters"
            raise QuoteNotFoundError(f"No quotes found for {detail}")

        return random.choice(filtered_quotes)
