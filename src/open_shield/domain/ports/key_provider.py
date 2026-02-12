from abc import ABC, abstractmethod
from typing import Any


class KeyProviderPort(ABC):
    """Abstract interface for retrieving and caching JSON Web Keys (JWKS)."""

    @abstractmethod
    def get_key(self, kid: str) -> Any:
        """
        Retrieve a specific key by Key ID (kid).

        Args:
            kid: The Key ID to search for.

        Returns:
            The key object (implementation dependent, usually a public key).

        Raises:
            KeyCorrectionError: If the key cannot be found or retrieved.
        """
        pass

    @abstractmethod
    def get_all_keys(self) -> list[dict[str, Any]]:
        """
        Retrieve all available keys in JWK format.

        Returns:
            A list of JWK dictionaries.
        """
        pass
