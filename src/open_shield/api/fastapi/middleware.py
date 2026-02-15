from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from open_shield.adapters import OIDCDiscoKeyProvider, OpenShieldConfig, PyJWTValidator
from open_shield.domain.exceptions import OpenShieldError, TokenValidationError
from open_shield.domain.ports import TenantResolverPort
from open_shield.domain.services import TokenService
from open_shield.domain.services.claim_mapping import ClaimMapping


class OpenShieldMiddleware(BaseHTTPMiddleware):
    """Middleware that intercepts requests, validates the Authorization header,
    and attaches the UserContext to the request state.

    Supports configurable claim mapping via OpenShieldConfig, making it
    compatible with any OIDC-compliant provider (Logto, Keycloak, Auth0, etc.).

    Attributes:
        app: The ASGI application.
        token_service: The domain service for validation.
        config: The SDK configuration.
        exclude_paths: A set of paths to exclude from authentication.
    """

    def __init__(
        self,
        app: ASGIApp,
        config: OpenShieldConfig,
        exclude_paths: set[str] | None = None,
        tenant_resolver: TenantResolverPort | None = None,
    ):
        super().__init__(app)
        self.config = config
        self.exclude_paths = exclude_paths or {
            "/docs",
            "/openapi.json",
            "/redoc",
            "/health",
        }

        # Build claim mapping from config
        claim_mapping = ClaimMapping(
            user_id_claim=config.USER_ID_CLAIM,
            email_claim=config.EMAIL_CLAIM,
            tenant_id_claim=config.TENANT_ID_CLAIM,
            scope_claim=config.SCOPE_CLAIM,
            roles_claim=config.ROLES_CLAIM,
            tenant_fallback=config.TENANT_FALLBACK,
        )

        # Initialize dependencies (composition root)
        key_provider = OIDCDiscoKeyProvider(issuer_url=config.ISSUER_URL)
        validator = PyJWTValidator(
            key_provider=key_provider,
            algorithms=config.ALGORITHMS,
            audience=config.AUDIENCE,
            issuer=config.ISSUER_URL,
        )
        self.token_service = TokenService(
            validator=validator,
            claim_mapping=claim_mapping,
            tenant_resolver=tenant_resolver,
        )

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return Response("Missing Authorization Header", status_code=401)

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                return Response("Invalid Authorization Scheme", status_code=401)

            user_context = self.token_service.validate_and_extract(token)

            # Attach to request.state for downstream access
            request.state.user_context = user_context

        except (ValueError, TokenValidationError) as e:
            return Response(f"Unauthorized: {e!s}", status_code=401)
        except OpenShieldError as e:
            return Response(f"Forbidden: {e!s}", status_code=403)
        except Exception:
            return Response(
                "Internal Server Error during Authentication", status_code=500
            )

        return await call_next(request)
