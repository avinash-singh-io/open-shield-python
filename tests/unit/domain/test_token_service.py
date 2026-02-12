from typing import Any
from unittest.mock import Mock

import pytest

from open_shield.domain.entities import Token, UserContext
from open_shield.domain.exceptions import TokenValidationError
from open_shield.domain.ports import TokenValidatorPort
from open_shield.domain.services import TokenService


class MockValidator(TokenValidatorPort):
    def validate_token(self, token_string: str) -> Token:
        return Token(
            raw=token_string,
            claims={"sub": "user123", "email": "test@example.com", "roles": ["admin"]},
        )

    def decode_unverified(self, token_string: str) -> dict[str, Any]:
        return {}


def test_token_service_extracts_user() -> None:
    validator = MockValidator()
    service = TokenService(validator)

    context = service.validate_and_extract("valid.token")

    assert isinstance(context, UserContext)
    assert context.user.id == "user123"
    assert context.user.email == "test@example.com"
    assert "admin" in context.user.roles


def test_token_service_raises_validation_error() -> None:
    validator = Mock()
    validator.validate_token.side_effect = TokenValidationError("Invalid token")
    service = TokenService(validator)

    with pytest.raises(TokenValidationError):
        service.validate_and_extract("invalid.token")


def test_token_service_missing_sub() -> None:
    validator = Mock()
    validator.validate_token.return_value = Token(
        raw="token", claims={"email": "no_sub@example.com"}
    )
    service = TokenService(validator)

    with pytest.raises(TokenValidationError) as exc:
        service.validate_and_extract("token")
    assert "missing 'sub'" in str(exc.value)


def test_token_service_realm_access_roles() -> None:
    validator = Mock()
    claims = {
        "sub": "user123",
        "realm_access": {"roles": ["superuser"]},
        "roles": ["user"],
    }
    validator.validate_token.return_value = Token(raw="token", claims=claims)
    service = TokenService(validator)

    context = service.validate_and_extract("token")
    assert "superuser" in context.user.roles
    assert "user" in context.user.roles


def test_token_service_extracts_tenant() -> None:
    validator = Mock()
    validator.validate_token.return_value = Token(
        raw="token", claims={"sub": "u1", "tid": "tenant_abc"}
    )
    service = TokenService(validator)

    context = service.validate_and_extract("token")
    assert context.tenant is not None
    assert context.tenant.tenant_id == "tenant_abc"
