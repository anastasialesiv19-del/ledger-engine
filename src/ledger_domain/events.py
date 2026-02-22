from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    event_id: str

@dataclass(frozen=True)
class AccountOpened(Event):
    account_id: str

@dataclass(frozen=True)
class Deposited(Event):
    account_id: str
    amount: int

@dataclass(frozen=True)
class Withdrawn(Event):
    account_id: str
    amount: int

@dataclass(frozen=True)
class Transferred(Event):
    from_account_id: str
    to_account_id: str
    amount: int




