from typing import Any

import jwt
from jwt.exceptions import ExpiredSignatureError
from jwt.exceptions import InvalidTokenError as PyJWTError

from open_shield.domain.entities import Token
from open_shield.domain.exceptions import (
    ExpiredTokenError,
    InvalidSignatureError,
    TokenValidationError,
)
from open_shield.domain.ports import TokenValidatorPort


class PyJWTValidator(TokenValidatorPort):
    """
    Adapter that uses PyJWT to validate tokens.
    """

    def __init__(self, key_provider=None, algorithms=None, audience=None, issuer=None):
        self.key_provider = key_provider
        self.algorithms = algorithms or ["RS256"]
        self.audience = audience
        self.issuer = issuer

    def validate_token(self, token_string: str) -> Token:
        try:
            # 1. Decode unverified header to get key ID (kid)
            header = jwt.get_unverified_header(token_string)
            kid = header.get("kid")

            key = None
            if self.key_provider and kid:
                key = self.key_provider.get_key(kid)

            # 2. Decode and validate
            # options={"verify_signature": True} is default
            payload = jwt.decode(
                token_string,
                key=key,
                algorithms=self.algorithms,
                audience=self.audience,
                issuer=self.issuer,
                options={
                    "verify_exp": True,
                    "verify_aud": True if self.audience else False,
                    "verify_iss": True if self.issuer else False,
                }
            )
            
            return Token(raw=token_string, claims=payload)

        except ExpiredSignatureError as e:
            raise ExpiredTokenError(f"Token expired: {e!s}") from e
        except PyJWTError as e:
            # Map generic PyJWT errors to specific domain errors if possible
            if "Signature verification failed" in str(e):
                raise InvalidSignatureError(f"Invalid signature: {e!s}") from e
            raise TokenValidationError(f"Token validation failed: {e!s}") from e
        except Exception as e:
            # Fallback for unexpected errors
            raise TokenValidationError(f"Unexpected validation error: {e!s}") from e

    def decode_unverified(self, token_string: str) -> dict[str, Any]:
        try:
            return jwt.decode(token_string, options={"verify_signature": False})
        except PyJWTError as e:
             raise TokenValidationError(f"Failed to decode token: {e!s}") from e
