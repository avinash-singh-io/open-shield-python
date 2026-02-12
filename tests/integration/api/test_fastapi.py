from unittest.mock import MagicMock, patch

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

from open_shield.adapters import OpenShieldConfig
from open_shield.api.fastapi import OpenShieldMiddleware, RequireScope, get_user_context
from open_shield.domain.entities import Token, User, UserContext
from open_shield.domain.exceptions import TokenValidationError


@pytest.fixture
def mock_token_service():
    return MagicMock()


@pytest.fixture
def client(mock_token_service):
    app = FastAPI()
    config = OpenShieldConfig(ISSUER_URL="https://test.auth", AUDIENCE="test-api")

    # Patch the TokenService class used in middleware
    with (
        patch("open_shield.api.fastapi.middleware.TokenService") as mock_service_class,
        patch("open_shield.api.fastapi.middleware.OIDCDiscoKeyProvider"),
        patch("open_shield.api.fastapi.middleware.PyJWTValidator"),
    ):
        mock_service_class.return_value = mock_token_service
        app.add_middleware(OpenShieldMiddleware, config=config)

        @app.get("/public")
        def public():
            return {"msg": "public"}

        @app.get("/protected")
        def protected(context: UserContext = Depends(get_user_context)):
            return {"user": context.user.id}

        @app.get("/scoped")
        def scoped(context: UserContext = Depends(RequireScope("read:data"))):
            return {"status": "ok"}

        yield TestClient(app)


def test_public_endpoint_no_auth(client, mock_token_service):
    # Middleware excludes are default (/docs, etc). /public is NOT excluded by default.
    # So it should be 401 if we enforce strict auth in middleware.
    # Our middleware implementation:
    # if request.url.path in self.exclude_paths: return call_next
    # else: check auth header

    # If we want /public to be public, we must exclude it or change middleware policy.
    # For this test, let's assume strict default.
    response = client.get("/public")
    assert response.status_code == 401
    assert "Missing Authorization Header" in response.text


def test_protected_endpoint_valid_token(client, mock_token_service):
    # Setup mock
    context = UserContext(
        user=User(id="user123", scopes=["read:data"]),
        token=Token(raw="token", claims={}),
        tenant=None,
    )
    mock_token_service.validate_and_extract.return_value = context

    response = client.get("/protected", headers={"Authorization": "Bearer best_token"})

    assert response.status_code == 200
    assert response.json() == {"user": "user123"}
    mock_token_service.validate_and_extract.assert_called_once_with("best_token")
    # Wait, header is "Bearer valid_token", split gives "valid_token" in middleware?
    # Scheme is "Bearer", token is "valid_token".


def test_protected_endpoint_invalid_token(client, mock_token_service):
    mock_token_service.validate_and_extract.side_effect = TokenValidationError(
        "Invalid"
    )

    response = client.get("/protected", headers={"Authorization": "Bearer invalid"})

    assert response.status_code == 401
    assert "Unauthorized" in response.text


def test_require_scope_success(client, mock_token_service):
    context = UserContext(
        user=User(id="user123", scopes=["read:data"]),
        token=Token(raw="token", claims={}),
        tenant=None,
    )
    mock_token_service.validate_and_extract.return_value = context

    response = client.get("/scoped", headers={"Authorization": "Bearer token"})
    assert response.status_code == 200


def test_require_scope_failure(client, mock_token_service):
    context = UserContext(
        user=User(id="user123", scopes=["other:scope"]),
        token=Token(raw="token", claims={}),
        tenant=None,
    )
    mock_token_service.validate_and_extract.return_value = context

    response = client.get("/scoped", headers={"Authorization": "Bearer token"})

    # Middleware passes 200 (auth ok), but Dependency raises 403
    assert response.status_code == 403
