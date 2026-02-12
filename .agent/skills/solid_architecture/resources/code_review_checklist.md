# SOLID Code Review Checklist

Use this checklist when generating or reviewing code to ensure SOLID compliance.

## 🔍 Quick Assessment

| # | Check | Pass? |
|---|-------|-------|
| 1 | Does each class have a single, clear responsibility? | ☐ |
| 2 | Can behavior be extended without modifying existing code? | ☐ |
| 3 | Are subtypes fully substitutable for their base types? | ☐ |
| 4 | Are interfaces small and role-specific? | ☐ |
| 5 | Do high-level modules depend on abstractions, not concretions? | ☐ |

## S — Single Responsibility

- [ ] Each class/module has ONE reason to change
- [ ] Business logic is separated from I/O, DB, and framework code
- [ ] No "god classes" that do everything
- [ ] Helper/utility methods belong to the right class

## O — Open/Closed

- [ ] New features added via new classes/adapters, NOT by modifying existing ones
- [ ] Strategy or plugin patterns used where behavior varies
- [ ] Configuration-driven behavior where appropriate

## L — Liskov Substitution

- [ ] Subclasses honor parent contracts (same inputs → compatible outputs)
- [ ] No methods that raise `NotImplementedError` in subclasses (design smell)
- [ ] No conditional logic based on concrete subtype (`isinstance` checks)

## I — Interface Segregation

- [ ] Interfaces are small (3–5 methods max)
- [ ] No unused methods forced on implementors
- [ ] Clients depend only on the methods they actually call

## D — Dependency Inversion (Most Critical)

- [ ] Domain services depend on abstract ports, NOT concrete adapters
- [ ] No `import` of infrastructure modules inside domain layer
- [ ] Dependencies injected via constructor (not created internally)
- [ ] Composition root is the ONLY place concrete classes are instantiated
- [ ] No framework classes (FastAPI, SQLAlchemy, etc.) in domain layer

## 🧼 Clean Code

- [ ] Functions are small (≤ 20 lines)
- [ ] Max 3 parameters per function (else use a DTO/dataclass)
- [ ] Names are descriptive and intention-revealing
- [ ] No silent error swallowing (`except: pass`)
- [ ] Domain-specific exceptions used (not generic `Exception`)

## 🧪 Testability

- [ ] Business logic testable WITHOUT database, network, or framework
- [ ] Mock/stub ports available for unit testing
- [ ] No static/global mutable state
- [ ] Tests verify behavior, not implementation details

## 🏛 Architecture

- [ ] Clear layer boundaries (domain → adapters → api)
- [ ] Dependency arrows point inward (toward domain)
- [ ] Composition over inheritance
- [ ] Immutable data objects where possible (`frozen=True`)

## 🚫 Red Flags

If any of these are present, refactoring is needed:

| Red Flag | Violation |
|----------|-----------|
| `import sqlite3` inside a service class | DIP |
| `if isinstance(x, ConcreteType)` | LSP |
| Class with 10+ methods doing unrelated things | SRP |
| Interface with 8+ methods | ISP |
| Adding a feature requires editing 5+ files | OCP |
| Tests need a running database | DIP / Testability |
| `from fastapi import ...` in domain layer | DIP |
