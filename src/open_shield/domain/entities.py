from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class Entity(BaseModel):
    """Base class for all domain entities."""

    model_config = ConfigDict(frozen=True)


class TenantContext(Entity):
    """Represents the tenant context extracted from a token."""

    tenant_id: str = Field(..., description="Unique identifier for the tenant")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional tenant metadata"
    )


class User(Entity):
    """Represents an authenticated user."""

    id: str = Field(..., description="Unique user identifier (sub)")
    email: str | None = Field(None, description="User email address")
    roles: list[str] = Field(default_factory=list, description="Assigned roles")
    scopes: list[str] = Field(
        default_factory=list, description="Granted scopes/permissions"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional user attributes"
    )


class Token(Entity):
    """Represents a raw and parsed authentication token."""

    raw: str = Field(..., description="The raw JWT string")
    claims: dict[str, Any] = Field(..., description="The parsed claims dictionary")

    @property
    def issuer(self) -> str | None:
        return self.claims.get("iss")

    @property
    def audience(self) -> str | list[str] | None:
        return self.claims.get("aud")

    @property
    def subject(self) -> str | None:
        return self.claims.get("sub")


class UserContext(Entity):
    """Aggregates User, Token, and Tenant information for a request."""

    user: User
    token: Token
    tenant: TenantContext | None = None
