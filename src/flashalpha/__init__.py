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
from .types import (
    ZeroDteDecay,
    ZeroDteExpectedMove,
    ZeroDteExposures,
    ZeroDteFlow,
    ZeroDteHedging,
    ZeroDteHedgingBucket,
    ZeroDteLevels,
    ZeroDteLiquidity,
    ZeroDteMetadata,
    ZeroDtePinComponents,
    ZeroDtePinRisk,
    ZeroDteRegime,
    ZeroDteResponse,
    ZeroDteStrike,
    ZeroDteVolContext,
)

__version__ = "0.3.7"
__all__ = [
    "FlashAlpha",
    "FlashAlphaError",
    "AuthenticationError",
    "TierRestrictedError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "ZeroDteResponse",
    "ZeroDteRegime",
    "ZeroDteExposures",
    "ZeroDteExpectedMove",
    "ZeroDtePinRisk",
    "ZeroDtePinComponents",
    "ZeroDteHedging",
    "ZeroDteHedgingBucket",
    "ZeroDteDecay",
    "ZeroDteVolContext",
    "ZeroDteFlow",
    "ZeroDteLevels",
    "ZeroDteLiquidity",
    "ZeroDteMetadata",
    "ZeroDteStrike",
]
