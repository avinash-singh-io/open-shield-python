from typing import Any

import httpx

from open_shield.domain.exceptions import ConfigurationError, OpenShieldError
from open_shield.domain.ports import KeyProviderPort


class OIDCDiscoKeyProvider(KeyProviderPort):
    """
    Adapter that fetches JWKS from an OIDC provider's well-known configuration.
    Features:
    - Automatic discovery of jwks_uri
    - Key caching (simple in-memory for MVP)
    - Key rotation support (refresh on miss)
    """

    def __init__(self, issuer_url: str):
        self.issuer_url = issuer_url.rstrip("/")
        self._jwks_uri: str | None = None
        self._keys: dict[str, Any] = {}
        self._client = httpx.Client()  # Use sync client for simplicity in core logic

    def get_key(self, kid: str) -> Any:
        if kid not in self._keys:
            self._refresh_keys()

        if kid not in self._keys:
            # Try one more time, force refresh
            self._refresh_keys()

        if kid not in self._keys:
            raise OpenShieldError(
                f"Key ID {kid} not found in JWKS from {self.issuer_url}"
            )

        return self._keys[kid]

    def get_all_keys(self) -> list[dict[str, Any]]:
        if not self._keys:
            self._refresh_keys()
        return list(self._keys.values())

    def _refresh_keys(self):
        if not self._jwks_uri:
            self._discover()

        try:
            response = self._client.get(self._jwks_uri)  # type: ignore
            response.raise_for_status()
            jwks = response.json()

            new_keys = {}
            for key_data in jwks.get("keys", []):
                kid = key_data.get("kid")
                if kid:
                    # Convert JWK to PEM/Public Key object using PyJWT helpers
                    # Optimization: In real world, use
                    # jwt.algorithms.RSAAlgorithm.from_jwk
                    # Here we store raw JWK or converted object depending on what validator
                    # expects. For PyJWT, passing the JWK dict or a key object often works,
                    # but let's be explicit.
                    # We will use PyJWT's internal helpers if available or just return
                    # the dict as PyJWT decode() accepts a JWK dict set or specific key.
                    # Ideally we convert distinct key per algorithm.

                    # For simplicity in this phase, we'll store the JWK dict.
                    # The Validator adapter will need to handle the conversion if
                    # needed, OR we implement conversion here.
                    # Best practice: KeyProvider returns ready-to-use keys.
                    import jwt.algorithms

                    # Try to get algo from 'alg' field first (e.g. RS256)
                    alg_name = key_data.get("alg")
                    if alg_name:
                        algo = jwt.algorithms.get_default_algorithms().get(alg_name)
                    else:
                        # Fallback for RSA if alg is missing but kty is RSA
                        if key_data.get("kty") == "RSA":
                            algo = jwt.algorithms.RSAAlgorithm
                        else:
                            algo = None

                    if algo:
                        public_key = algo.from_jwk(key_data)
                        new_keys[kid] = public_key

            self._keys = new_keys

        except Exception as e:
            raise OpenShieldError(f"Failed to refresh JWKS: {e!s}") from e

    def _discover(self):
        try:
            disco_url = f"{self.issuer_url}/.well-known/openid-configuration"
            response = self._client.get(disco_url)
            response.raise_for_status()
            config = response.json()
            self._jwks_uri = config.get("jwks_uri")
            if not self._jwks_uri:
                raise ConfigurationError(
                    "Pre-discovery failed: jwks_uri not found in OIDC config"
                )
        except Exception as e:
            raise ConfigurationError(
                f"OIDC discovery failed for {self.issuer_url}: {e!s}"
            ) from e
