class FlumesError(Exception):
    """Base exception for all SDK errors."""


class AuthenticationError(FlumesError):
    """Invalid or missing API key."""


class NotFoundError(FlumesError):
    """Requested resource not found."""


class RateLimitError(FlumesError):
    """Quota exceeded (HTTP 429)."""


class TransportError(FlumesError):
    """Generic network / transport error."""
