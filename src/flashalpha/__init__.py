"""FlashAlpha Python SDK — options exposure analytics API."""

from .client import FlashAlpha
from .exceptions import (
    AuthenticationError,
    FlashAlphaError,
    NotFoundError,
    RateLimitError,
    ServerError,
    TierRestrictedError,
)

__version__ = "0.1.0"
__all__ = [
    "FlashAlpha",
    "FlashAlphaError",
    "AuthenticationError",
    "TierRestrictedError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
]
