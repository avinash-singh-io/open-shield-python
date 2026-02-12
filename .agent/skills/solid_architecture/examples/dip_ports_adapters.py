"""
Example: Dependency Inversion Principle — Ports & Adapters Pattern

This example demonstrates how to structure a notification service using
DIP with constructor injection and abstract ports. The domain layer
(NotificationService) knows nothing about email, SMS, or any concrete
delivery mechanism.

Key Concepts:
  - Abstract Port:        NotificationPort (interface for sending)
  - Concrete Adapters:    EmailAdapter, SmsAdapter
  - Domain Service:       NotificationService (depends only on the port)
  - Composition Root:     create_notification_service() wires everything
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

# ─────────────────────────────────────────────
# 1. Domain Layer — Pure business logic + DTOs
# ─────────────────────────────────────────────


@dataclass(frozen=True)
class Notification:
    """Domain DTO — no framework or infra dependencies."""

    recipient: str
    subject: str
    body: str


class NotificationPort(ABC):
    """
    Abstract Port — defines WHAT the domain needs, not HOW it's done.

    This is the contract that all delivery adapters must honor.
    The domain layer owns this interface (Dependency Inversion).
    """

    @abstractmethod
    def send(self, notification: Notification) -> bool:
        """Send a notification. Returns True on success."""
        ...


class NotificationService:
    """
    Domain Service — orchestrates business logic.

    ✅ Depends only on the abstract NotificationPort
    ✅ No knowledge of email, SMS, HTTP, or any infrastructure
    ✅ Fully testable with a mock/stub port
    """

    def __init__(self, port: NotificationPort) -> None:
        self._port = port  # Constructor Injection

    def notify_user(self, recipient: str, subject: str, body: str) -> bool:
        """Business rule: validate, build DTO, delegate to port."""
        if not recipient or not subject:
            raise ValueError("Recipient and subject are required.")

        notification = Notification(
            recipient=recipient,
            subject=subject,
            body=body,
        )
        return self._port.send(notification)


# ─────────────────────────────────────────────
# 2. Adapter Layer — Concrete implementations
# ─────────────────────────────────────────────


class EmailAdapter(NotificationPort):
    """
    Concrete Adapter — sends notifications via email.

    ✅ Implements the abstract port
    ✅ Infrastructure details are encapsulated here
    ✅ Can be swapped without touching domain code
    """

    def __init__(self, smtp_host: str, smtp_port: int) -> None:
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port

    def send(self, notification: Notification) -> bool:
        # Real implementation would use smtplib here
        print(
            f"[EMAIL] To: {notification.recipient} | "
            f"Subject: {notification.subject} | "
            f"Via: {self._smtp_host}:{self._smtp_port}"
        )
        return True


class SmsAdapter(NotificationPort):
    """
    Concrete Adapter — sends notifications via SMS.

    Demonstrates that the domain service works with ANY adapter
    that honors the NotificationPort contract.
    """

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def send(self, notification: Notification) -> bool:
        print(f"[SMS] To: {notification.recipient} | Message: {notification.body}")
        return True


# ─────────────────────────────────────────────
# 3. Composition Root — Wiring (entry point)
# ─────────────────────────────────────────────


def create_notification_service(channel: str = "email") -> NotificationService:
    """
    Factory function — the ONLY place where concrete classes are instantiated.

    ✅ Domain code never calls this
    ✅ Framework/config layer calls this at startup
    ✅ Easy to swap adapters via config
    """
    adapters = {
        "email": lambda: EmailAdapter(smtp_host="smtp.example.com", smtp_port=587),
        "sms": lambda: SmsAdapter(api_key="secret-api-key"),
    }

    adapter_factory = adapters.get(channel)
    if not adapter_factory:
        raise ValueError(f"Unknown notification channel: {channel}")

    return NotificationService(port=adapter_factory())


# ─────────────────────────────────────────────
# 4. Testing — Mock adapter for unit tests
# ─────────────────────────────────────────────


class MockNotificationPort(NotificationPort):
    """
    Test double — records calls for assertion.

    ✅ No real I/O
    ✅ Verifies behavior, not implementation
    """

    def __init__(self) -> None:
        self.sent: list[Notification] = []

    def send(self, notification: Notification) -> bool:
        self.sent.append(notification)
        return True


def test_notify_user_sends_notification() -> None:
    """Example unit test — domain logic tested without infrastructure."""
    mock_port = MockNotificationPort()
    service = NotificationService(port=mock_port)

    result = service.notify_user(
        recipient="user@example.com",
        subject="Welcome",
        body="Hello!",
    )

    assert result is True
    assert len(mock_port.sent) == 1
    assert mock_port.sent[0].recipient == "user@example.com"
    assert mock_port.sent[0].subject == "Welcome"


if __name__ == "__main__":
    # Demo: swap adapters at runtime
    for channel in ("email", "sms"):
        svc = create_notification_service(channel)
        svc.notify_user("user@example.com", "Hello", "Welcome aboard!")
        print()

    # Run the test
    test_notify_user_sends_notification()
    print("✅ All tests passed.")
