import pytest
from unittest.mock import Mock
from open_shield.domain.services import TokenService
from open_shield.domain.ports import TokenValidatorPort
from open_shield.domain.entities import Token, UserContext
from open_shield.domain.exceptions import TokenValidationError


class MockValidator(TokenValidatorPort):
    def validate_token(self, token_string: str) -> Token:
        return Token(raw=token_string, claims={"sub": "user123", "email": "test@example.com", "roles": ["admin"]})

    def decode_unverified(self, token_string: str) -> dict:
        return {}


def test_token_service_extracts_user():
    validator = MockValidator()
    service = TokenService(validator)
    
    context = service.validate_and_extract("valid.token")
    
    assert isinstance(context, UserContext)
    assert context.user.id == "user123"
    assert context.user.email == "test@example.com"
    assert "admin" in context.user.roles


def test_token_service_raises_validation_error():
    validator = Mock()
    validator.validate_token.side_effect = TokenValidationError("Invalid token")
    service = TokenService(validator)
    
    with pytest.raises(TokenValidationError):
        service.validate_and_extract("invalid.token")
