# Ledger Engine

Ledger engine with event replay, invariants, idempotency, and tests (TDD).

## Purpose
Built as a portfolio project to demonstrate idempotent event processing, domain invariants, and test-driven development.

## Rules v0.1
1. The source of truth is an event log.
2. Balances are obtained through `replay(events)` from scratch.
3. Events v0.1: `AccountOpened`, `Deposited`, `Withdrawn`.
4. `amount` must be > 0 for deposit/withdraw.
5. Deposits and withdrawals are not allowed for non-existent accounts.
6. `Withdrawn` cannot make the balance negative.
7. `replay` is deterministic: the same log → the same state.

## Features
- Replay-based state reconstruction (replay(events))
- Domain invariants — InvalidAmount / AccountNotFound / InsufficientFunds enforced
- Transfer with atomicity guarantees and conservation invariant
- Idempotency with event_id (duplicate events ignored; invalid events not marked as seen)
- Automated tests using pytest (parametrized scenario matrix + invariants)

## Project structure
```
src/ledger_domain/
  __init__.py
  engine.py
  errors.py
  events.py
  models.py
tests/
  helpers.py
  test_idempotency.py
  test_invariants.py
  test_replay_basics.py
  test_sequences.py
  test_transfer.py
```
`engine.py` — replay/apply_event, invariants, transfer, idempotency (seen_event_ids policy)
`events.py` — event dataclasses (event log)
`errors.py` — domain exceptions
`test_transfer.py` — transfer + atomicity + conservation invariant
`test_idempotency.py` — duplicate events ignored + “invalid not marked as seen”
`test_sequences.py` — test matrix / parametrized scenario coverage
`demo.py` — quick smoke-run for demonstration

## Quickstart
```
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -e ".[dev]"
pytest
python scripts/demo.py
```

## Example 
```
Balances after replay (ok): 
{'A': 60, 'B': 40}

Balances after replay (with duplicates):
{'A': 60, 'B': 40}
```

## Testing
Tests cover invariants, transfer atomicity, idempotency, and scenario-based sequences.

Aspects covered:
- Atomicity of event processing (events are not partially executed in case of exceptions)
- Idempotency (duplication of events does not change the balance)
- Failure scenarios and exception handling

Tests are implemented using pytest.

Run all tests:
```
pytest
```

## Design decisions
- Deterministic replay
- Idempotency policy: mark event_id as seen only after successful apply
- Atomic transfer: validate first, then apply changes

## Roadmap
- Add DuplicateEvent error policy option