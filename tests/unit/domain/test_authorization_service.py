import pytest

from open_shield.domain.entities import Token, User, UserContext
from open_shield.domain.exceptions import AuthorizationError
from open_shield.domain.services import AuthorizationService


@pytest.fixture
def user_context():
    return UserContext(
        user=User(id="123", scopes=["read:users"], roles=["admin"]),
        token=Token(raw="raw", claims={}),
        tenant=None,
    )


def test_require_scope_success(user_context):
    service = AuthorizationService()
    service.require_scope(user_context, "read:users")


def test_require_scope_failure(user_context):
    service = AuthorizationService()
    with pytest.raises(AuthorizationError):
        service.require_scope(user_context, "write:users")


def test_require_any_role_success(user_context):
    service = AuthorizationService()
    service.require_any_role(user_context, ["admin", "editor"])


def test_require_any_role_failure(user_context):
    service = AuthorizationService()
    with pytest.raises(AuthorizationError):
        service.require_any_role(user_context, ["guest"])
