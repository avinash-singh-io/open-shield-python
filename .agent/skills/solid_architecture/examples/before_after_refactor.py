"""
Example: Before & After SOLID Refactoring

This file shows the same feature implemented TWO ways:
  1. ❌ BEFORE — violates SOLID (tightly coupled, untestable)
  2. ✅ AFTER  — follows SOLID (decoupled, injectable, testable)

Feature: "Save a user profile and notify them via email."
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ══════════════════════════════════════════════
# ❌ BEFORE — SOLID VIOLATIONS
# ══════════════════════════════════════════════

class UserServiceBad:
    """
    ❌ God class with multiple SOLID violations.

    Violations:
      - SRP: handles DB, email, AND business logic
      - OCP: adding SMS requires modifying this class
      - DIP: directly instantiates sqlite3 and smtplib
      - Untestable: can't unit test without a real DB and SMTP server
    """

    def save_and_notify(self, name: str, email: str) -> None:
        import sqlite3  # ❌ Infrastructure inside business logic

        # ❌ Hard-coded database dependency
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (name, email),
        )
        conn.commit()
        conn.close()

        import smtplib  # ❌ Infrastructure inside business logic

        # ❌ Hard-coded email dependency
        server = smtplib.SMTP("smtp.example.com", 587)
        server.sendmail(
            "noreply@example.com",
            email,
            f"Welcome {name}!",
        )
        server.quit()


# ══════════════════════════════════════════════
# ✅ AFTER — SOLID-COMPLIANT REFACTORING
# ══════════════════════════════════════════════

# ── Domain DTOs ──────────────────────────────

@dataclass(frozen=True)
class UserProfile:
    """Immutable domain entity — no infrastructure knowledge."""
    name: str
    email: str


# ── Abstract Ports (owned by domain) ─────────

class UserRepository(ABC):
    """
    SRP: Only responsible for user persistence.
    DIP: Domain defines the interface, adapters implement it.
    """

    @abstractmethod
    def save(self, user: UserProfile) -> None:
        """Persist a user profile."""
        ...


class NotificationSender(ABC):
    """
    ISP: Focused interface — send only.
    DIP: Domain defines what it needs; infra provides how.
    """

    @abstractmethod
    def send_welcome(self, user: UserProfile) -> None:
        """Send a welcome notification to the user."""
        ...


# ── Domain Service ───────────────────────────

class UserService:
    """
    ✅ SRP: Only orchestrates the "save & notify" business flow.
    ✅ OCP: New notification channels = new adapter, no change here.
    ✅ DIP: Depends on abstractions, not concrete DB/email classes.
    ✅ Testable: Inject mocks for both ports.
    """

    def __init__(
        self,
        repository: UserRepository,
        notifier: NotificationSender,
    ) -> None:
        self._repository = repository
        self._notifier = notifier

    def save_and_notify(self, name: str, email: str) -> None:
        """Business rule: save the user, then send welcome."""
        if not name or not email:
            raise ValueError("Name and email are required.")

        user = UserProfile(name=name, email=email)
        self._repository.save(user)
        self._notifier.send_welcome(user)


# ── Concrete Adapters (infrastructure) ───────

class SqliteUserRepository(UserRepository):
    """
    Adapter: SQLite implementation of UserRepository.

    ✅ Infrastructure details encapsulated.
    ✅ Swappable — e.g., for PostgresUserRepository.
    """

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def save(self, user: UserProfile) -> None:
        import sqlite3

        conn = sqlite3.connect(self._db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user.name, user.email),
        )
        conn.commit()
        conn.close()


class SmtpNotificationSender(NotificationSender):
    """
    Adapter: SMTP implementation of NotificationSender.

    ✅ Infrastructure details encapsulated.
    ✅ Swappable — e.g., for SmsNotificationSender.
    """

    def __init__(self, smtp_host: str, smtp_port: int) -> None:
        self._smtp_host = smtp_host
        self._smtp_port = smtp_port

    def send_welcome(self, user: UserProfile) -> None:
        import smtplib

        server = smtplib.SMTP(self._smtp_host, self._smtp_port)
        server.sendmail(
            "noreply@example.com",
            user.email,
            f"Welcome {user.name}!",
        )
        server.quit()


# ── Composition Root ─────────────────────────

def create_user_service() -> UserService:
    """Wire concrete adapters — the ONLY place this happens."""
    repo = SqliteUserRepository(db_path="users.db")
    notifier = SmtpNotificationSender(smtp_host="smtp.example.com", smtp_port=587)
    return UserService(repository=repo, notifier=notifier)


# ── Testing with Mocks ──────────────────────

class FakeUserRepository(UserRepository):
    """Test double for persistence."""

    def __init__(self) -> None:
        self.saved: list[UserProfile] = []

    def save(self, user: UserProfile) -> None:
        self.saved.append(user)


class FakeNotificationSender(NotificationSender):
    """Test double for notifications."""

    def __init__(self) -> None:
        self.welcomed: list[UserProfile] = []

    def send_welcome(self, user: UserProfile) -> None:
        self.welcomed.append(user)


def test_save_and_notify() -> None:
    """
    ✅ Unit test with NO database, NO network, NO framework.
    Tests behavior: "was user saved AND notified?"
    """
    fake_repo = FakeUserRepository()
    fake_notifier = FakeNotificationSender()
    service = UserService(repository=fake_repo, notifier=fake_notifier)

    service.save_and_notify("Alice", "alice@example.com")

    assert len(fake_repo.saved) == 1
    assert fake_repo.saved[0].name == "Alice"
    assert len(fake_notifier.welcomed) == 1
    assert fake_notifier.welcomed[0].email == "alice@example.com"


def test_save_and_notify_rejects_empty_name() -> None:
    """✅ Tests validation without any infrastructure."""
    fake_repo = FakeUserRepository()
    fake_notifier = FakeNotificationSender()
    service = UserService(repository=fake_repo, notifier=fake_notifier)

    try:
        service.save_and_notify("", "alice@example.com")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected

    assert len(fake_repo.saved) == 0  # Nothing was saved


if __name__ == "__main__":
    test_save_and_notify()
    test_save_and_notify_rejects_empty_name()
    print("✅ All tests passed.")
