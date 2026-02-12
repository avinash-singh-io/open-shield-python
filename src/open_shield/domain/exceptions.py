class OpenShieldError(Exception):
    """Base exception for all Open Shield errors."""

    pass


class ConfigurationError(OpenShieldError):
    """Raised when the SDK configuration is invalid."""

    pass


class TokenValidationError(OpenShieldError):
    """Base exception for token validation failures."""

    pass


class InvalidSignatureError(TokenValidationError):
    """Raised when the token signature is invalid."""

    pass


class ExpiredTokenError(TokenValidationError):
    """Raised when the token has expired."""

    pass


class InvalidClaimsError(TokenValidationError):
    """Raised when token claims (iss, aud, etc.) are invalid."""

    pass


class AuthorizationError(OpenShieldError):
    """Raised when a user lacks required permissions."""

    pass
