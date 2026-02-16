from dataclasses import dataclass

@dataclass()
class AccountState:
    account_id: str
    balance: int = 0


@dataclass()
class LedgerState:
    accounts: dict[str, AccountState]