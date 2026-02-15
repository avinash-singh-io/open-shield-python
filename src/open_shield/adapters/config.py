from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenShieldConfig(BaseSettings):
    """Configuration for Open Shield SDK.

    Loads settings from environment variables (OPEN_SHIELD_ prefix).

    OIDC Settings:
        ISSUER_URL: OIDC provider's issuer URL (required).
        AUDIENCE: Expected audience claim value.
        ALGORITHMS: Allowed JWT signing algorithms.

    Claim Mapping:
        USER_ID_CLAIM: Claim containing the unique user identifier.
        EMAIL_CLAIM: Claim containing the user's email address.
        TENANT_ID_CLAIM: Claim containing tenant/organization ID.
        SCOPE_CLAIM: Claim containing space-separated scopes.
        ROLES_CLAIM: Claim containing user roles.
        TENANT_FALLBACK: Strategy when tenant claim is missing ("sub" | "none").

    Authorization:
        REQUIRE_SCOPES: Whether to enforce scope presence globally.
        REQUIRE_ROLES: Whether to enforce role presence globally.
    """

    model_config = SettingsConfigDict(
        env_prefix="OPEN_SHIELD_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # OIDC
    ISSUER_URL: str
    AUDIENCE: str | None = None
    ALGORITHMS: list[str] = ["RS256"]

    # Claim mapping (identity-provider agnostic)
    USER_ID_CLAIM: str = "sub"
    EMAIL_CLAIM: str = "email"
    TENANT_ID_CLAIM: str = "tid"
    SCOPE_CLAIM: str = "scope"
    ROLES_CLAIM: str = "roles"
    TENANT_FALLBACK: str = "none"

    # Authorization defaults
    REQUIRE_SCOPES: bool = True
    REQUIRE_ROLES: bool = False
