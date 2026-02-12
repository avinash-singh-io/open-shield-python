from fastapi import Depends, HTTPException, Request

from open_shield.domain.entities import UserContext
from open_shield.domain.exceptions import AuthorizationError
from open_shield.domain.services import AuthorizationService


def get_user_context(request: Request) -> UserContext:
    """
    Dependency to retrieve the UserContext from request.state.
    Assumes OpenShieldMiddleware has run.
    """
    if not hasattr(request.state, "user_context"):
        raise HTTPException(status_code=401, detail="Authentication required")
    from typing import cast
    return cast(UserContext, request.state.user_context)


class RequireScope:
    """Dependency that enforces a required scope."""

    def __init__(self, scope: str):
        self.scope = scope
        self.auth_service = AuthorizationService()

    def __call__(self, context: UserContext = Depends(get_user_context)) -> UserContext:
        try:
            self.auth_service.require_scope(context, self.scope)
        except AuthorizationError as e:
            raise HTTPException(status_code=403, detail=str(e)) from e
        return context


class RequireRole:
    """Dependency that enforces one of the required roles."""

    def __init__(self, roles: list[str]):
        self.roles = roles
        self.auth_service = AuthorizationService()

    def __call__(self, context: UserContext = Depends(get_user_context)) -> UserContext:
        try:
            self.auth_service.require_any_role(context, self.roles)
        except AuthorizationError as e:
            raise HTTPException(status_code=403, detail=str(e)) from e
        return context
