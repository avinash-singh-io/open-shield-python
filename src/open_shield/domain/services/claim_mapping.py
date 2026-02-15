"""Configurable JWT claim-to-field mapping.

Allows consumers to map any OIDC provider's claim names to Open Shield's
internal user/tenant model without modifying SDK code.

Examples:
    # Logto
    ClaimMapping(tenant_id_claim="organization_id")

    # Keycloak
    ClaimMapping(roles_claim="realm_access.roles", tenant_id_claim="tenant")

    # Auth0
    ClaimMapping(tenant_id_claim="https://myapp.com/org_id")
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ClaimMapping:
    """Maps JWT claim names to semantic identity fields.

    All fields have sensible defaults that work with most OIDC providers.
    Override individual fields to match your provider's token format.

    Attributes:
        user_id_claim: Claim containing the unique user identifier.
        email_claim: Claim containing the user's email address.
        tenant_id_claim: Claim containing the tenant/organization ID.
        scope_claim: Claim containing space-separated scopes.
        roles_claim: Claim containing the user's roles.
        tenant_fallback: Strategy when tenant claim is missing.
            "sub" = fall back to user_id, "none" = no tenant.
    """

    user_id_claim: str = "sub"
    email_claim: str = "email"
    tenant_id_claim: str = "tid"
    scope_claim: str = "scope"
    roles_claim: str = "roles"
    tenant_fallback: str = "none"
