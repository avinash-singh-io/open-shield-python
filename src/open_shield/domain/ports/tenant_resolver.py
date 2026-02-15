"""Port for resolving tenant context from machine client credentials.

This port supports Case 3 (M2M clients) in the tenant resolution cascade:

    1. M2M client → lookup_client_tenant(client_id) → tenant_id
    2. Organization claim → organization_id → tenant_id
    3. Fallback → sub → tenant_id (individual user mode only)

Consumers implement this port to map client_id → tenant_id using their
own registry (database, config file, Logto Management API, etc.).
"""

from abc import ABC, abstractmethod


class TenantResolverPort(ABC):
    """Resolves tenant context for machine-to-machine (M2M) clients.

    M2M tokens (client_credentials flow) don't carry organization claims.
    This port allows consumers to map a ``client_id`` to a ``tenant_id``
    using their own backend registry.

    If no resolver is provided to ``TokenService``, M2M tokens fall through
    to the organization claim or sub fallback.
    """

    @abstractmethod
    def resolve_tenant(self, client_id: str) -> str | None:
        """Look up the tenant for a machine client.

        Args:
            client_id: The OAuth2 client_id from the token.

        Returns:
            The tenant_id if found, or None to continue the cascade.
        """
        ...
