import pytest

from ledger_domain.engine import replay, balances
from ledger_domain.errors import InvalidAmount, AccountNotFound, InsufficientFunds
from ledger_domain.events import AccountOpened, Deposited, Transferred


def test_correct_transfer():
    events = [AccountOpened("A"), AccountOpened("B"), Deposited("A", 100), Transferred("A", "B", 40)]
    state = replay(events)
    assert balances(state) == {"A": 60, "B": 40}

def test_transfer_amount_zero_or_negative():
    events = [AccountOpened("A"), AccountOpened("B"), Deposited("A", 100), Transferred("A", "B", 0)]

    with pytest.raises(InvalidAmount):
        replay(events)

    events = [AccountOpened("A"), AccountOpened("B"), Deposited("A", 100), Transferred("A", "B", -1)]

    with pytest.raises(InvalidAmount):
        replay(events)

def test_transfer_nonexistent_from():
    events = [AccountOpened("B"), Transferred("A", "B", 20)]

    with pytest.raises(AccountNotFound):
        replay(events)

def test_transfer_nonexistent_to():
    events = [AccountOpened("A"), Deposited("A", 100), Transferred("A", "B", 40)]

    with pytest.raises(AccountNotFound):
        replay(events)

def test_transfer_more_than_balance():
    events = [AccountOpened("A"), AccountOpened("B"), Deposited("A", 100), Transferred("A", "B", 150)]

    with pytest.raises(InsufficientFunds):
        replay(events)

def test_transfer_atomicity():
    events_ok = [AccountOpened("A"), AccountOpened("B"), Deposited("A", 10)]
    state_before = replay(events_ok)
    events_fail =[AccountOpened("A"), AccountOpened("B"), Deposited("A", 10), Transferred("A", "B", 50)]
    with pytest.raises(InsufficientFunds):
        replay(events_fail)
    new_state = replay(events_ok)

    assert balances(new_state) == balances(state_before)

def test_conservation_invariant_transfer():
    events = [AccountOpened("A"), AccountOpened("B"), Deposited("A", 100)]
    state_before = replay(events)
    sum_before = sum(balances(state_before).values())
    events_with_transfer = [AccountOpened("A"), AccountOpened("B"), Deposited("A", 100), Transferred("A", "B", 40)]
    state_after = replay(events_with_transfer)
    sum_after = sum(balances(state_after).values())
    assert sum_before == sum_after



