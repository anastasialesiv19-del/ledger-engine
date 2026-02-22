import pytest

from ledger_domain.engine import replay, balances
from ledger_domain.errors import InsufficientFunds, AccountNotFound, InvalidAmount
from ledger_domain.events import AccountOpened, Withdrawn, Deposited
from helpers import eid


def test_withdraw_more_balance():
    events = [AccountOpened(eid("open_A"), "A"), Withdrawn(eid("withdraw_A"), "A", 1)]

    with pytest.raises(InsufficientFunds):
        replay(events)

def test_withdraw_zero_or_negative():
    events = [AccountOpened(eid("open_A"), "A"), Withdrawn(eid("withdraw_A"), "A", 0)]

    with pytest.raises(InvalidAmount):
        replay(events)

    events = [AccountOpened(eid("open_A"),"A"), Withdrawn(eid("withdraw_A"), "A", -1)]

    with pytest.raises(InvalidAmount):
        replay(events)

def test_deposit_zero_or_negative():
    events = [AccountOpened(eid("open_A"), "A"), Deposited(eid("deposit_A"), "A", 0)]

    with pytest.raises(InvalidAmount):
        replay(events)

    events = [AccountOpened(eid("open_A"), "A"), Deposited(eid("deposit_A"), "A", -1)]

    with pytest.raises(InvalidAmount):
        replay(events)


def test_event_for_nonexistent_account():
    events = [Deposited(eid("deposit_B"),"B", amount=100)]

    with pytest.raises(AccountNotFound):
        replay(events)

def test_of_deterministic_replays():
    events = [AccountOpened(eid("open_A"), "A"), Deposited(eid("deposit_A"), "A", amount=100), Withdrawn(eid("withdraw_A"), "A", 20)]

    state_1 = replay(events)
    state_2 = replay(events)

    assert balances(state_1).keys() == balances(state_2).keys()
    assert balances(state_1)["A"] == balances(state_2)["A"]
