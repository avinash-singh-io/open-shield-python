from typing import Any

from open_shield.domain.entities import Token
from open_shield.domain.ports import TenantResolverPort, TokenValidatorPort
from open_shield.domain.services import TokenService
from open_shield.domain.services.claim_mapping import ClaimMapping


class _MockValidator(TokenValidatorPort):
    """Mock validator that returns a token with given claims."""

    def __init__(self, claims: dict[str, Any]) -> None:
        self._claims = claims

    def validate_token(self, token_string: str) -> Token:
        return Token(raw=token_string, claims=self._claims)

    def decode_unverified(self, token_string: str) -> dict[str, Any]:
        return self._claims


# ---------------------------------------------------------------------------
# Claim Mapping Tests
# ---------------------------------------------------------------------------


def test_default_claim_mapping() -> None:
    """Default ClaimMapping reads standard OIDC claims."""
    cm = ClaimMapping()
    assert cm.user_id_claim == "sub"
    assert cm.email_claim == "email"
    assert cm.tenant_id_claim == "tid"
    assert cm.scope_claim == "scope"
    assert cm.roles_claim == "roles"
    assert cm.tenant_fallback == "none"


def test_custom_email_claim() -> None:
    """Email is extracted from a custom claim name."""
    claims = {"sub": "u1", "preferred_username": "alice@corp.com"}
    cm = ClaimMapping(email_claim="preferred_username")
    service = TokenService(_MockValidator(claims), claim_mapping=cm)

    ctx = service.validate_and_extract("token")
    assert ctx.user.email == "alice@corp.com"


def test_custom_tenant_claim_logto() -> None:
    """Tenant extracted from Logto's organization_id claim."""
    claims = {"sub": "u1", "organization_id": "org_abc"}
    cm = ClaimMapping(tenant_id_claim="organization_id")
    service = TokenService(_MockValidator(claims), claim_mapping=cm)

    ctx = service.validate_and_extract("token")
    assert ctx.tenant is not None
    assert ctx.tenant.tenant_id == "org_abc"


def test_custom_tenant_claim_keycloak() -> None:
    """Tenant extracted from Keycloak-style custom claim."""
    claims = {"sub": "u1", "tenant": "customer_a"}
    cm = ClaimMapping(tenant_id_claim="tenant")
    service = TokenService(_MockValidator(claims), claim_mapping=cm)

    ctx = service.validate_and_extract("token")
    assert ctx.tenant is not None
    assert ctx.tenant.tenant_id == "customer_a"


def test_tenant_fallback_to_sub() -> None:
    """When tenant claim is missing and fallback='sub', use user ID."""
    claims = {"sub": "user_123"}
    cm = ClaimMapping(tenant_fallback="sub")
    service = TokenService(_MockValidator(claims), claim_mapping=cm)

    ctx = service.validate_and_extract("token")
    assert ctx.tenant is not None
    assert ctx.tenant.tenant_id == "user_123"


def test_tenant_fallback_none() -> None:
    """When tenant claim is missing and fallback='none', tenant is None."""
    claims = {"sub": "user_123"}
    cm = ClaimMapping(tenant_fallback="none")
    service = TokenService(_MockValidator(claims), claim_mapping=cm)

    ctx = service.validate_and_extract("token")
    assert ctx.tenant is None


def test_custom_scope_claim() -> None:
    """Scopes extracted from a custom claim name."""
    claims = {"sub": "u1", "permissions": "read write admin"}
    cm = ClaimMapping(scope_claim="permissions")
    service = TokenService(_MockValidator(claims), claim_mapping=cm)

    ctx = service.validate_and_extract("token")
    assert ctx.user.scopes == ["read", "write", "admin"]


def test_custom_roles_claim() -> None:
    """Roles extracted from a custom claim name."""
    claims = {"sub": "u1", "app_roles": ["editor", "viewer"]}
    cm = ClaimMapping(roles_claim="app_roles")
    service = TokenService(_MockValidator(claims), claim_mapping=cm)

    ctx = service.validate_and_extract("token")
    assert "editor" in ctx.user.roles
    assert "viewer" in ctx.user.roles


# ---------------------------------------------------------------------------
# Actor Type Inference Tests
# ---------------------------------------------------------------------------


def test_actor_type_user_default() -> None:
    """Default actor type is 'user' for normal JWT tokens."""
    claims = {"sub": "user_123", "email": "user@test.com"}
    service = TokenService(_MockValidator(claims))

    ctx = service.validate_and_extract("token")
    assert ctx.user.actor_type == "user"


def test_actor_type_service_m2m() -> None:
    """M2M token (sub == client_id) → 'service'."""
    claims = {"sub": "client_abc", "client_id": "client_abc"}
    service = TokenService(_MockValidator(claims))

    ctx = service.validate_and_extract("token")
    assert ctx.user.actor_type == "service"


def test_actor_type_agent_m2m() -> None:
    """M2M token with 'agent' role → 'agent'."""
    claims = {
        "sub": "agent_xyz",
        "client_id": "agent_xyz",
        "roles": ["agent"],
    }
    service = TokenService(_MockValidator(claims))

    ctx = service.validate_and_extract("token")
    assert ctx.user.actor_type == "agent"


def test_actor_type_azp_fallback() -> None:
    """azp claim used when client_id is absent."""
    claims = {"sub": "svc_001", "azp": "svc_001"}
    service = TokenService(_MockValidator(claims))

    ctx = service.validate_and_extract("token")
    assert ctx.user.actor_type == "service"


# ---------------------------------------------------------------------------
# Tenant Resolution Cascade Tests
# ---------------------------------------------------------------------------


class _MockTenantResolver(TenantResolverPort):
    """Mock tenant resolver for testing M2M lookup."""

    def __init__(self, mapping: dict[str, str]) -> None:
        self._mapping = mapping

    def resolve_tenant(self, client_id: str) -> str | None:
        return self._mapping.get(client_id)


def test_cascade_step1_m2m_resolver() -> None:
    """Step 1: M2M token with resolver → tenant from registry."""
    claims = {"sub": "client_abc", "client_id": "client_abc"}
    resolver = _MockTenantResolver({"client_abc": "tenant_from_registry"})
    service = TokenService(
        _MockValidator(claims),
        tenant_resolver=resolver,
    )

    ctx = service.validate_and_extract("token")
    assert ctx.tenant is not None
    assert ctx.tenant.tenant_id == "tenant_from_registry"
    assert ctx.tenant.metadata["resolution"] == "m2m_lookup"


def test_cascade_step1_m2m_no_resolver_falls_through() -> None:
    """Step 1 skipped: M2M token but no resolver → falls to step 2/3."""
    claims = {"sub": "client_abc", "client_id": "client_abc", "tid": "org_123"}
    service = TokenService(
        _MockValidator(claims),
        # No tenant_resolver provided
    )

    ctx = service.validate_and_extract("token")
    assert ctx.tenant is not None
    assert ctx.tenant.tenant_id == "org_123"
    assert ctx.tenant.metadata["resolution"] == "claim"


def test_cascade_step1_resolver_returns_none_falls_through() -> None:
    """Step 1: Resolver doesn't know this client → falls to step 2."""
    claims = {
        "sub": "unknown_client",
        "client_id": "unknown_client",
        "organization_id": "fallback_org",
    }
    resolver = _MockTenantResolver({})  # Empty — won't match
    cm = ClaimMapping(tenant_id_claim="organization_id")
    service = TokenService(
        _MockValidator(claims),
        claim_mapping=cm,
        tenant_resolver=resolver,
    )

    ctx = service.validate_and_extract("token")
    assert ctx.tenant is not None
    assert ctx.tenant.tenant_id == "fallback_org"
    assert ctx.tenant.metadata["resolution"] == "claim"


def test_cascade_step2_org_claim_priority() -> None:
    """Step 2: Organization claim takes priority over sub fallback."""
    claims = {"sub": "user_123", "organization_id": "team_abc"}
    cm = ClaimMapping(
        tenant_id_claim="organization_id",
        tenant_fallback="sub",  # Would use sub, but org claim wins
    )
    service = TokenService(_MockValidator(claims), claim_mapping=cm)

    ctx = service.validate_and_extract("token")
    assert ctx.tenant is not None
    assert ctx.tenant.tenant_id == "team_abc"
    assert ctx.tenant.metadata["resolution"] == "claim"


def test_cascade_step3_sub_fallback_metadata() -> None:
    """Step 3: Sub fallback includes resolution metadata."""
    claims = {"sub": "solo_user"}
    cm = ClaimMapping(tenant_fallback="sub")
    service = TokenService(_MockValidator(claims), claim_mapping=cm)

    ctx = service.validate_and_extract("token")
    assert ctx.tenant is not None
    assert ctx.tenant.tenant_id == "solo_user"
    assert ctx.tenant.metadata["resolution"] == "sub_fallback"

