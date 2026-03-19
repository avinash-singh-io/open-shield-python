# Phase 4 Retrospective: Polish & Release

> **Completed**: 2026-03-06 | **Release**: v0.2.7

## What Went Well

- PyPI publication workflow (Test PyPI → PyPI) caught issues early
- Architecture diagrams significantly improved project visibility
- Configurable claim mapping (v0.2.0) made the SDK truly provider-agnostic
- Tenant resolution cascade handles individual users, SaaS orgs, and M2M accounts

## What Could Be Improved

- README went through multiple restructures (v0.2.6, v0.2.7) — should have planned layout upfront
- Git history cleanup was necessary but disruptive

## Key Features Added

- Configurable claim mapping (any JWT claim → user/tenant/role fields)
- 3-step tenant resolution cascade (sub fallback, org claim, M2M lookup)
- Actor type inference (user, service, agent)
- Optional authentication (`get_optional_user_context`)
- Architecture and sequence flow diagrams

## Lessons Learned

- Visual documentation (diagrams) has outsized impact on adoption
- Provider-agnostic claim mapping should have been in v0.1.0 — it's fundamental to vendor neutrality
- Open source readiness (CODE_OF_CONDUCT, SECURITY, CONTRIBUTING) is non-trivial but essential
