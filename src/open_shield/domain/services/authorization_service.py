from open_shield.domain.entities import UserContext
from open_shield.domain.exceptions import AuthorizationError


class AuthorizationService:
    """
    Domain service for enforcing access control policies on a UserContext.
    """

    def require_scope(self, context: UserContext, required_scope: str) -> None:
        """
        Ensure the user has the required scope.

        Args:
            context: The authenticated user context.
            required_scope: The specific scope string required.

        Raises:
            AuthorizationError: If the scope is missing.
        """
        if required_scope not in context.user.scopes:
            # Check for exact match first.
            # TODO: Implement hierarchical scope checking (e.g. read:users implies read:users:self) if needed.
            raise AuthorizationError(f"Missing required scope: {required_scope}")

    def require_any_role(self, context: UserContext, roles: list[str]) -> None:
        """
        Ensure the user has at least one of the required roles.

        Args:
            context: The authenticated user context.
            roles: A list of allowed roles.

        Raises:
            AuthorizationError: If the user has none of the required roles.
        """
        user_roles = set(context.user.roles)
        required_roles = set(roles)

        if not user_roles.intersection(required_roles):
            raise AuthorizationError(
                f"Missing required role. User has: {user_roles}. "
                f"Required one of: {required_roles}"
            )
