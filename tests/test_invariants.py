import pytest

from ledger_domain.engine import replay
from ledger_domain.errors import InsufficientFunds, AccountNotFound, InvalidAmount
from ledger_domain.events import AccountOpened, Withdrawn, Deposited


def test_withdraw_more_balance():
    events = [AccountOpened("A"), Withdrawn("A", 1)]

    with pytest.raises(InsufficientFunds):
        replay(events)

def test_withdraw_zero_or_negative():
    events = [AccountOpened("A"), Withdrawn("A", 0)]

    with pytest.raises(InvalidAmount):
        replay(events)

    events = [AccountOpened("A"), Withdrawn("A", -1)]

    with pytest.raises(InvalidAmount):
        replay(events)

def test_deposit_zero_or_negative():
    events = [AccountOpened("A"), Deposited("A", 0)]

    with pytest.raises(InvalidAmount):
        replay(events)

    events = [AccountOpened("A"), Deposited("A", -1)]

    with pytest.raises(InvalidAmount):
        replay(events)


def test_event_for_non_existent_account():
    events = [Deposited("B", amount=100)]

    with pytest.raises(AccountNotFound):
        replay(events)

def test_of_deterministic_replays():
    events = [AccountOpened("A"), Deposited("A", amount=100), Withdrawn("A", 20)]

    state_1 = replay(events)
    state_2 = replay(events)

    assert state_1.accounts["A"].account_id == state_2.accounts["A"].account_id
    assert state_1.accounts["A"].balance == state_2.accounts["A"].balance
    assert state_1.accounts.keys() == state_2.accounts.keys()
