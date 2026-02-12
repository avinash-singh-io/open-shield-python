from abc import ABC, abstractmethod
from typing import Any

from open_shield.domain.entities import Token


class TokenValidatorPort(ABC):
    """Abstract interface for validating JWT tokens."""

    @abstractmethod
    def validate_token(self, token_string: str) -> Token:
        """
        Parse and validate a raw JWT string.

        Args:
            token_string: The raw JWT string.

        Returns:
            A validated Token entity.

        Raises:
            TokenValidationError: If validation fails (expired, invalid signature, etc).
        """
        pass

    @abstractmethod
    def decode_unverified(self, token_string: str) -> dict[str, Any]:
        """
        Decode the token without verification (useful for inspecting headers/claims
        pre-validation).

        Args:
            token_string: The raw JWT string.

        Returns:
            The decoded claims dictionary.
        """
        pass
