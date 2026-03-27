from aot.core.database import AoTDatabase
from aot.core.exceptions import CharacterNotFoundError, QuoteNotFoundError, TitanNotFoundError


def test_singleton_behavior() -> None:
    first = AoTDatabase()
    second = AoTDatabase()
    assert first is second


def test_get_character_fuzzy_case_insensitive() -> None:
    db = AoTDatabase()
    result = db.get_character("levi")
    assert result["full_name"] == "Levi Ackerman"


def test_get_titan_fuzzy_case_insensitive() -> None:
    db = AoTDatabase()
    result = db.get_titan("attack")
    assert result["name"] == "Attack Titan"


def test_get_random_quote_with_tag_filter() -> None:
    db = AoTDatabase()
    quote = db.get_random_quote(tag="motivational")
    assert "motivational" in quote["vibe_tags"]


def test_missing_character_raises() -> None:
    db = AoTDatabase()
    try:
        db.get_character("not-a-character")
    except CharacterNotFoundError:
        pass
    else:
        raise AssertionError("Expected CharacterNotFoundError")


def test_missing_titan_raises() -> None:
    db = AoTDatabase()
    try:
        db.get_titan("not-a-titan")
    except TitanNotFoundError:
        pass
    else:
        raise AssertionError("Expected TitanNotFoundError")


def test_missing_quote_raises() -> None:
    db = AoTDatabase()
    try:
        db.get_random_quote(character="Levi", tag="nonexistent")
    except QuoteNotFoundError:
        pass
    else:
        raise AssertionError("Expected QuoteNotFoundError")
