# Smart Todo Manager Constitution

## Principle I: Specification-First Development

All functional requirements, acceptance criteria,
and design decisions must be documented and traceable.

## Principle II: Deterministic Behavior

Given identical inputs and persisted application state,
the application must produce identical outputs.

## Principle III: Independent Testing Harness

The application must be validated through automated
tests covering:

- CRUD operations
- Invalid inputs
- JSON persistence
- Edge cases
- Regression testing

Tests must use isolated data.

## Principle IV: Code Quality and Security

All application code must pass:

- Ruff linting
- Bandit security scanning
- Automated functional tests

## Principle V: Defect Traceability

Every discovered defect must have:

1. Failure evidence
2. Root-cause analysis
3. Corrective action
4. Regression verification

## Principle VI: Reliable Persistence

Tasks must be stored in JSON.

Task IDs must remain unique and must not be reused
after deletion.

## Principle VII: Evidence Integrity

Only genuine execution results may be recorded.

Test logs and defect histories must never be fabricated.

## Principle VIII: Implementation Preservation

Existing validated functionality must be preserved
during specification updates.

Any implementation changes require regression testing.

## Technology Constraints

- Python 3.12
- JSON persistence
- PowerShell
- Ruff
- Bandit
- Automated testing harness