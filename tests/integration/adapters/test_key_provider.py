import pytest
import respx
from httpx import Response
from open_shield.adapters.key_provider import OIDCDiscoKeyProvider
from open_shield.domain.exceptions import OpenShieldError, ConfigurationError


@respx.mock
def test_oidc_discovery_and_key_retrieval():
    issuer = "https://auth.example.com"
    jwks_uri = f"{issuer}/protocol/openid-connect/certs"
    
    # Mock Discovery
    respx.get(f"{issuer}/.well-known/openid-configuration").mock(
        return_value=Response(200, json={"jwks_uri": jwks_uri})
    )
    
    # Mock JWKS
    respx.get(jwks_uri).mock(
        return_value=Response(200, json={
            "keys": [
                {
                    "kid": "key1",
                    "kty": "RSA",
                    "alg": "RS256",
                    "n": "vX8_J85d4rF3_2_5_3_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3_5_3",
                    "e": "AQAB"
                }
            ]
        })
    )
    
    provider = OIDCDiscoKeyProvider(issuer)
    
    # Should trigger discovery and fetch
    keys = provider.get_all_keys()
    assert len(keys) == 1
    
    # Should return cached key (JWK dict in this implementation phase)
    key = provider.get_key("key1")
    assert key is not None
    assert isinstance(key, dict) or hasattr(key, 'public_numbers') # Flexibly assert based on implementation details

@respx.mock
def test_oidc_discovery_failure():
    issuer = "https://auth.example.com"
    respx.get(f"{issuer}/.well-known/openid-configuration").mock(
        return_value=Response(500)
    )
    
    provider = OIDCDiscoKeyProvider(issuer)
    with pytest.raises(ConfigurationError):
        provider.get_all_keys()
