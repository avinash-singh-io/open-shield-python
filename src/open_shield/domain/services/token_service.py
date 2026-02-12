from open_shield.domain.entities import TenantContext, Token, User, UserContext
from open_shield.domain.exceptions import TokenValidationError
from open_shield.domain.ports import TokenValidatorPort


class TokenService:
    """
    Domain service for orchestrating token validation and context extraction.
    Dependencies are injected via constructor (DIP).
    """

    def __init__(self, validator: TokenValidatorPort):
        self.validator = validator

    def validate_and_extract(self, token_string: str) -> UserContext:
        """
        Validate a raw token string and extract the user context.

        Args:
            token_string: The raw JWT from the Authorization header.

        Returns:
            A populated UserContext object.

        Raises:
            TokenValidationError: If validation fails.
        """
        token = self.validator.validate_token(token_string)
        user = self._extract_user(token)
        tenant = self._extract_tenant(token)

        return UserContext(
            user=user,
            token=token,
            tenant=tenant
        )

    def _extract_user(self, token: Token) -> User:
        """Extract user identity and permissions from the token."""
        # Default claim mapping (stateless)
        # TODO: Make claim mapping configurable
        sub = token.subject
        if not sub:
            raise TokenValidationError("Token missing 'sub' claim")

        email = token.claims.get("email")
        # Standard claim for roles in Keycloak/Auth0 varies.
        # We look for 'roles', 'realm_access.roles', or 'permissions'.
        roles = token.claims.get("roles", [])
        if "realm_access" in token.claims and isinstance(token.claims["realm_access"], dict):
            roles.extend(token.claims["realm_access"].get("roles", []))
            
        scopes = token.claims.get("scope", "").split() if isinstance(token.claims.get("scope"), str) else []
        
        return User(
            id=sub,
            email=email,
            roles=list(set(roles)),  # Deduplicate
            scopes=scopes,
            metadata=token.claims
        )

    def _extract_tenant(self, token: Token) -> TenantContext | None:
        """
        Extract tenant context from the token.
        Strategies:
        1. Custom claim 'tid' or 'org_id'
        2. Issuer URL parsing (e.g. https://auth.com/realms/{tenant})
        """
        # Simple default strategy: look for specific claims
        # TODO: Make tenant extraction strategy configurable
        tid = token.claims.get("tid") or token.claims.get("org_id") or token.claims.get("tenant_id")
        
        if tid:
            return TenantContext(tenant_id=tid, metadata={})
        
        return None
