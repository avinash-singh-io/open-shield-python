from datetime import UTC, datetime, timedelta

import jwt
import pytest
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from open_shield.adapters.token_validator import PyJWTValidator
from open_shield.domain.exceptions import ExpiredTokenError


@pytest.fixture
def rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # public_pem not used in this test, but generation logic kept for reference/completeness if needed
    # public_pem = public_key.public_bytes(...)

    return private_key, public_key


class MockKeyProvider:
    def __init__(self, key):
        self.key = key

    def get_key(self, kid):
        return self.key


def test_validate_valid_token(rsa_keys):
    private_key, public_key = rsa_keys

    payload = {
        "sub": "user123",
        "iss": "https://auth.example.com",
        "aud": "my-api",
        "exp": datetime.now(UTC) + timedelta(hours=1),
        "iat": datetime.now(UTC),
    }

    token = jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": "key1"})

    validator = PyJWTValidator(
        key_provider=MockKeyProvider(public_key),
        audience="my-api",
        issuer="https://auth.example.com",
    )

    res = validator.validate_token(token)
    assert res.claims["sub"] == "user123"


def test_validate_expired_token(rsa_keys):
    private_key, public_key = rsa_keys

    payload = {"sub": "user123", "exp": datetime.now(UTC) - timedelta(hours=1)}

    token = jwt.encode(payload, private_key, algorithm="RS256", headers={"kid": "key1"})

    validator = PyJWTValidator(key_provider=MockKeyProvider(public_key))

    with pytest.raises(ExpiredTokenError):
        validator.validate_token(token)
