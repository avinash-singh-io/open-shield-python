from open_shield.domain.entities import TenantContext, Token, User, UserContext
from open_shield.domain.exceptions import TokenValidationError
from open_shield.domain.ports import TenantResolverPort, TokenValidatorPort
from open_shield.domain.services.claim_mapping import ClaimMapping


class TokenService:
    """Domain service for orchestrating token validation and context extraction.

    Implements a 3-step tenant resolution cascade:
        1. M2M client → lookup via TenantResolverPort (if provided)
        2. Organization claim → configurable tenant_id_claim
        3. Fallback → sub (if tenant_fallback="sub")

    Args:
        validator: Port for JWT validation.
        claim_mapping: Configurable claim-to-field mapping.
        tenant_resolver: Optional port for M2M client→tenant lookup.
            If not provided, M2M tokens fall through to the org claim.
    """

    def __init__(
        self,
        validator: TokenValidatorPort,
        claim_mapping: ClaimMapping | None = None,
        tenant_resolver: TenantResolverPort | None = None,
    ):
        self.validator = validator
        self.claims = claim_mapping or ClaimMapping()
        self.tenant_resolver = tenant_resolver

    def validate_and_extract(self, token_string: str) -> UserContext:
        """Validate a raw token string and extract the user context.

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

        return UserContext(user=user, token=token, tenant=tenant)

    def _extract_user(self, token: Token) -> User:
        """Extract user identity and permissions from the token.

        Uses the configured claim mapping to read fields from any
        OIDC-compliant provider's token format.
        """
        sub = token.subject
        if not sub:
            raise TokenValidationError("Token missing 'sub' claim")

        email = token.claims.get(self.claims.email_claim)

        # Roles: support flat list and nested Keycloak-style realm_access
        roles = token.claims.get(self.claims.roles_claim, [])
        if isinstance(roles, str):
            roles = [roles]
        if "realm_access" in token.claims and isinstance(
            token.claims["realm_access"], dict
        ):
            roles = list(roles)  # ensure mutable
            roles.extend(token.claims["realm_access"].get("roles", []))

        # Scopes: space-separated string or list
        raw_scope = token.claims.get(self.claims.scope_claim, "")
        scopes = raw_scope.split() if isinstance(raw_scope, str) else list(raw_scope)

        # Actor type inference
        actor_type = self._infer_actor_type(token.claims, roles)

        return User(
            id=sub,
            email=email,
            roles=list(set(roles)),  # Deduplicate
            scopes=scopes,
            actor_type=actor_type,
            metadata=token.claims,
        )

    def _extract_tenant(self, token: Token) -> TenantContext | None:
        """Extract tenant context using a 3-step cascade.

        Resolution order:
            1. M2M client lookup — If this is a client_credentials token
               (sub == client_id) AND a TenantResolverPort is configured,
               resolve tenant from the client registry.
            2. Organization claim — Read the configured tenant_id_claim
               (e.g. organization_id, tid, org_id).
            3. Sub fallback — If tenant_fallback="sub", use the user's
               subject as tenant_id (individual user mode).

        Returns:
            TenantContext if resolved, None if no tenant could be determined.
        """
        claims = token.claims
        sub = token.subject

        # --- Step 1: M2M client → tenant lookup ---
        client_id = claims.get("client_id", claims.get("azp"))
        is_m2m = client_id and sub and sub == client_id

        if is_m2m and self.tenant_resolver:
            resolved = self.tenant_resolver.resolve_tenant(client_id)
            if resolved:
                return TenantContext(
                    tenant_id=resolved,
                    metadata={"resolution": "m2m_lookup", "client_id": client_id},
                )

        # --- Step 2: Organization claim ---
        tid = claims.get(self.claims.tenant_id_claim)
        if tid:
            return TenantContext(
                tenant_id=tid,
                metadata={"resolution": "claim", "claim": self.claims.tenant_id_claim},
            )

        # --- Step 3: Sub fallback (individual user mode) ---
        if self.claims.tenant_fallback == "sub" and sub:
            return TenantContext(
                tenant_id=sub,
                metadata={"resolution": "sub_fallback"},
            )

        return None

    def _infer_actor_type(self, claims: dict, roles: list) -> str:  # type: ignore[type-arg]
        """Infer actor type from token claims.

        Heuristic:
        - If 'client_id' == 'sub' (client credentials flow) → "service" or "agent"
        - Default → "user"
        """
        sub = claims.get("sub", "")
        client_id = claims.get("client_id", claims.get("azp", ""))

        # Client credentials flow: sub == client_id (no human user)
        if client_id and sub == client_id:
            if "agent" in roles:
                return "agent"
            return "service"

        return "user"
