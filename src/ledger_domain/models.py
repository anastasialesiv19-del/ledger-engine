from dataclasses import dataclass

@dataclass()
class AccountState:
    account_id: str
    balance: int = 0


@dataclass()
class LedgerState:
    seen_event_ids: set[str]
    accounts: dict[str, AccountState]