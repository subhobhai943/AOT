"""Custom exception hierarchy for the AoT data engine."""


class AoTException(Exception):
    """Base class for all library-specific exceptions."""


class CharacterNotFoundError(AoTException):
    """Raised when a character cannot be found in the database."""


class TitanNotFoundError(AoTException):
    """Raised when a titan cannot be found in the database."""


class QuoteNotFoundError(AoTException):
    """Raised when a quote cannot be found in the database."""
