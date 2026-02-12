# Clean Architecture — Python Project Layout

Reference folder structure for a Python project following **Hexagonal Architecture (Ports & Adapters)** with strict layer boundaries.

## Directory Structure

```
src/<project_name>/
│
├── domain/                     # 🧠 Core Business Logic (innermost layer)
│   ├── __init__.py
│   ├── entities/               # Domain entities & value objects
│   │   ├── __init__.py
│   │   ├── user.py             # @dataclass(frozen=True) User
│   │   └── order.py
│   ├── exceptions.py           # Domain-specific exceptions
│   ├── ports/                  # Abstract interfaces (owned by domain)
│   │   ├── __init__.py
│   │   ├── user_repository.py  # ABC: UserRepository
│   │   ├── notification.py     # ABC: NotificationPort
│   │   └── payment.py          # ABC: PaymentGateway
│   └── services/               # Domain services (business rules)
│       ├── __init__.py
│       ├── user_service.py     # Depends on ports, NOT adapters
│       └── order_service.py
│
├── adapters/                   # 🔌 Infrastructure Implementations (outer layer)
│   ├── __init__.py
│   ├── persistence/            # Database adapters
│   │   ├── __init__.py
│   │   ├── sqlalchemy_user_repo.py   # Implements UserRepository
│   │   └── in_memory_user_repo.py    # For testing / dev
│   ├── notification/           # Notification adapters
│   │   ├── __init__.py
│   │   ├── smtp_adapter.py     # Implements NotificationPort
│   │   └── twilio_adapter.py   # Alternative implementation
│   ├── payment/                # Payment adapters
│   │   ├── __init__.py
│   │   └── stripe_adapter.py   # Implements PaymentGateway
│   └── external/               # Third-party API clients
│       ├── __init__.py
│       └── geocoding_adapter.py
│
├── api/                        # 🌐 Delivery Layer (HTTP, CLI, gRPC)
│   ├── __init__.py
│   ├── routes/                 # Route handlers
│   │   ├── __init__.py
│   │   ├── user_routes.py      # Thin — delegates to domain services
│   │   └── order_routes.py
│   ├── schemas/                # Request/Response DTOs (Pydantic)
│   │   ├── __init__.py
│   │   ├── user_schema.py
│   │   └── order_schema.py
│   ├── middleware/              # Auth, logging, error handling
│   │   ├── __init__.py
│   │   └── error_handler.py
│   └── main.py                 # App factory / entry point
│
├── config.py                   # Configuration (env vars, settings)
└── container.py                # 🏭 Composition Root (DI wiring)

tests/
├── unit/                       # ⚡ Fast, isolated, no I/O
│   ├── domain/
│   │   ├── test_user_service.py    # Uses mock ports
│   │   └── test_order_service.py
│   └── conftest.py             # Shared fixtures (fake repos, etc.)
├── integration/                # 🔗 Tests with real infra
│   ├── adapters/
│   │   ├── test_sqlalchemy_repo.py
│   │   └── test_smtp_adapter.py
│   └── conftest.py             # DB setup, test containers
└── conftest.py                 # Root fixtures
```

## Layer Rules

| Layer | Can Depend On | Must NOT Depend On |
|-------|---------------|-------------------|
| `domain/` | Nothing (pure Python, stdlib only) | `adapters/`, `api/`, frameworks |
| `adapters/` | `domain/ports/`, `domain/entities/` | `api/`, other adapters |
| `api/` | `domain/services/`, `domain/entities/` | `adapters/` (uses container) |
| `container.py` | Everything (wiring only) | — |

## Dependency Flow

```
┌─────────────────────────────────────────┐
│              api/ (routes)              │  ← Thin controllers
│         Depends on: domain/services     │
├─────────────────────────────────────────┤
│           domain/ (core)                │  ← Pure business logic
│    entities/ | services/ | ports/       │
│         Depends on: NOTHING             │
├─────────────────────────────────────────┤
│          adapters/ (infra)              │  ← Concrete implementations
│      Implements: domain/ports           │
├─────────────────────────────────────────┤
│     container.py (composition root)     │  ← Wires adapters → ports
│         Knows everything                │
└─────────────────────────────────────────┘
```

## Key Principles

1. **Domain is pure** — no imports from `adapters/`, `api/`, or third-party libraries
2. **Ports live in `domain/`** — the domain _owns_ its interfaces
3. **Adapters implement ports** — one adapter per external dependency
4. **Composition root** — `container.py` is the only place where concrete classes are instantiated and injected
5. **Routes are thin** — only parse requests, delegate to services, format responses
6. **Tests mirror structure** — `unit/domain/` mirrors `src/domain/`, `integration/adapters/` mirrors `src/adapters/`
