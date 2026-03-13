"""FlashAlpha API exceptions."""


class FlashAlphaError(Exception):
    """Base exception for FlashAlpha SDK."""

    def __init__(self, message: str, status_code: int | None = None, response: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AuthenticationError(FlashAlphaError):
    """Raised when the API key is invalid or missing (401)."""


class TierRestrictedError(FlashAlphaError):
    """Raised when the endpoint requires a higher plan (403)."""

    def __init__(self, message: str, current_plan: str | None = None, required_plan: str | None = None, **kwargs):
        super().__init__(message, **kwargs)
        self.current_plan = current_plan
        self.required_plan = required_plan


class NotFoundError(FlashAlphaError):
    """Raised when the requested resource is not found (404)."""


class RateLimitError(FlashAlphaError):
    """Raised when the rate limit is exceeded (429)."""

    def __init__(self, message: str, retry_after: int | None = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ServerError(FlashAlphaError):
    """Raised on 5xx server errors."""
