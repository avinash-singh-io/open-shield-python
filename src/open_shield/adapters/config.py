from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenShieldConfig(BaseSettings):
    """
    Configuration for Open Shield SDK.
    Loads settings from environment variables (OPEN_SHIELD_prefix).
    """

    model_config = SettingsConfigDict(
        env_prefix="OPEN_SHIELD_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ISSUER_URL: str
    AUDIENCE: str | None = None
    ALGORITHMS: list[str] = ["RS256"]

    # Authorization defaults
    REQUIRE_SCOPES: bool = True
    REQUIRE_ROLES: bool = False

    # Tenant extraction
    TENANT_ID_CLAIM: str = "tid"
