---
name: solid_architecture
description: Enforces SOLID principles, design patterns, and clean architecture in code generation and review.
---

# 🧠 Skill: Senior Software Engineer (SOLID-Driven Architecture)

## 🎯 Purpose

This skill ensures all generated or reviewed code:

- Follows SOLID principles
- Applies appropriate design patterns
- Enforces clean architecture
- Maintains high testability
- Prioritizes Dependency Inversion Principle (DIP)
- Avoids tight coupling and premature optimization

## 🏗 Core Coding Philosophy

### 1️⃣ SOLID Principles (Mandatory)

**S — Single Responsibility Principle**
- One class/module = one reason to change
- Business logic separated from:
  - I/O
  - DB
  - Network
  - Framework concerns

**O — Open/Closed Principle**
- Extend behavior via:
  - Interfaces
  - Composition
  - Strategy Pattern
- Avoid modifying stable, production-tested code

**L — Liskov Substitution Principle**
- Subtypes must:
  - Respect contracts
  - Not weaken preconditions
  - Not strengthen postconditions

**I — Interface Segregation Principle**
- Prefer small, role-specific interfaces
- No “fat” interfaces
- Consumers depend only on what they use

**🔥 D — Dependency Inversion Principle (Most Important)**
- High-level modules must NOT depend on low-level modules. Both must depend on abstractions.
- **Rules**:
  - No direct instantiation of concrete dependencies inside business logic
  - No framework classes inside domain layer
- **Use**:
  - Constructor Injection
  - Interface-based design
  - Ports & Adapters
- **Business rules must not depend on**:
  - Database implementation
  - HTTP framework
  - External SDKs
  - Infrastructure layer

### 🧩 Design Patterns (Use When Appropriate)
Use patterns only when they improve clarity.

**Creational**
- Factory
- Abstract Factory
- Builder

**Structural**
- Adapter
- Decorator
- Facade

**Behavioral**
- Strategy
- Observer
- Command
- Chain of Responsibility

### 🧼 Clean Code Standards

**Naming**
- Descriptive, intention-revealing names
- Avoid abbreviations
- No single-letter variables (except loops)

**Functions**
- Small (≤ 20 lines ideally)
- Do one thing
- No side effects unless explicit
- Max 3 parameters (else use object)

**Classes**
- Small
- Focused
- Low cyclomatic complexity

**Error Handling**
- No silent failures
- No generic catch-all blocks
- Use domain-specific exceptions

### 🧱 Architecture Guidelines
- Prefer Composition over Inheritance
- Favor Immutability
- Explicit dependencies
- Stateless services where possible
- Side effects isolated

### 🧪 Testing Standards
- Code must be testable
- No static/global state
- Business logic testable without:
  - DB
  - Network
  - Framework
- Use mocks at boundaries only
- Prefer behavior testing over implementation testing

### ⚙️ Best Practices
- DRY but not at cost of clarity
- Avoid premature abstraction
- Avoid God classes
- Keep modules cohesive
- Follow consistent folder structure
- Document public APIs

### 🚫 Anti-Patterns to Avoid
- Tight coupling
- Hard-coded dependencies
- Framework leakage into domain
- Massive services
- Circular dependencies
- Anemic domain model (when domain logic exists)

### 🏛 Architecture Preference
Default to:
- Clean Architecture
- Hexagonal Architecture (Ports & Adapters)
- Layered architecture with strict boundaries

## 🧠 Engineering Mindset
When writing code:
1. First design abstractions
2. Then implement concrete adapters
3. Keep domain pure
4. Make code replaceable
5. Optimize for maintainability, not cleverness

## 🔒 Output Expectations
Whenever generating or reviewing code:
- Explain architectural decisions
- Show abstraction boundaries
- Justify design pattern usage
- Highlight SOLID compliance
- Explicitly mention DIP usage

## 📂 Reference Materials

### Examples (`examples/`)
When generating or reviewing code, consult these reference implementations:

| File | Purpose |
|------|---------|
| `dip_ports_adapters.py` | Full DIP example with abstract ports, concrete adapters, constructor injection, factory wiring, and test doubles |
| `before_after_refactor.py` | Side-by-side comparison of SOLID violations vs. clean refactored code |
| `clean_architecture_layout.md` | Reference folder structure for hexagonal architecture with layer rules |

### Resources (`resources/`)
| File | Purpose |
|------|---------|
| `code_review_checklist.md` | SOLID compliance checklist with per-principle checks and red flags |

