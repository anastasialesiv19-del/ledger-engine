# Ledger Engine

///description

## Purpose

## Rules v0.1
1. The main book is an event log.
2. Balances are obtained through `replay(events)` from scratch.
3. Events v0.1: `AccountOpened`, `Deposited`, `Withdrawn`.
4. `amount` must be > 0 for deposit/withdraw.
5. You cannot make deposit/withdraw for a non-existent account.
6. `Withdrawn` cannot make the balance negative.
7. `Replay` is deterministic: the same log → the same state.

## Features

## Project structure

## Installation & run

## Example 

## Testing

## Design decisions

## Roadmap