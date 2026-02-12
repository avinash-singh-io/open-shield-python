from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from open_shield.adapters import OIDCDiscoKeyProvider, OpenShieldConfig, PyJWTValidator
from open_shield.domain.exceptions import OpenShieldError, TokenValidationError
from open_shield.domain.services import TokenService


class OpenShieldMiddleware(BaseHTTPMiddleware):
    """
    Middleware that intercepts requests, validates the Authorization header,
    and attaches the UserContext to the request state.

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
    ):
        super().__init__(app)
        self.config = config
        self.exclude_paths = exclude_paths or {
            "/docs",
            "/openapi.json",
            "/redoc",
            "/health",
        }

        # Initialize dependencies
        # In a real app, these might be injected, but middleware initialization is often
        # the composition root.
        key_provider = OIDCDiscoKeyProvider(issuer_url=config.ISSUER_URL)
        validator = PyJWTValidator(
            key_provider=key_provider,
            algorithms=config.ALGORITHMS,
            audience=config.AUDIENCE,
            issuer=config.ISSUER_URL,
        )
        self.token_service = TokenService(validator=validator)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            # Basic check, detailed handling usually done by dependency or explicit 401
            # If we want global enforcement, strictly 401 here.
            # Return 401.
            return Response("Missing Authorization Header", status_code=401)

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                return Response("Invalid Authorization Scheme", status_code=401)

            user_context = self.token_service.validate_and_extract(token)

            # Attach to request.state for downstream access
            request.state.user_context = user_context

            # Enforce global require_scopes/roles if configured?
            # Usually better handled in route dependencies.

        except (ValueError, TokenValidationError) as e:
            return Response(f"Unauthorized: {e!s}", status_code=401)
        except OpenShieldError as e:
            return Response(f"Forbidden: {e!s}", status_code=403)
        except Exception:
            # Log this error
            return Response(
                "Internal Server Error during Authentication", status_code=500
            )

        return await call_next(request)
