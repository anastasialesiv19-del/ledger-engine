from dataclasses import dataclass

@dataclass(frozen=True)
class AccountOpened:
    account_id: str

@dataclass(frozen=True)
class Deposited:
    account_id: str
    amount: int

@dataclass(frozen=True)
class Withdrawn:
    account_id: str
    amount: int




