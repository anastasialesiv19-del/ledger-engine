import pytest

from ledger_domain.engine import replay, balances
from ledger_domain.errors import InvalidAmount
from ledger_domain.events import AccountOpened, Deposited, Transferred
from helpers import eid


def test_duplicate_deposit_is_ignored():
    events = [AccountOpened(eid("open_A"), "A"), Deposited(eid("deposit_A"), "A", 20),
              Deposited(eid("deposit_A"),"A", 20)]

    state = replay(events)

    assert balances(state)["A"] == 20

def test_duplicate_transfer_is_ignored():
    events = [AccountOpened(eid("open_A"), "A"), AccountOpened(eid("open_B"), "B"),
              Deposited(eid("deposit_A"), "A", 50), Transferred(eid("transfer_A_to_B"), "A", "B", 10),
              Transferred(eid("transfer_A_to_B"), "A", "B", 10)]

    state = replay(events)

    assert balances(state)["A"] == 40
    assert balances(state)["B"] == 10

def test_invalid_event_is_not_marked_as_seen():
    events = [AccountOpened(eid("open_A"), "A"), Deposited(eid("deposit_A"), "A", 0)]

    with pytest.raises(InvalidAmount):
        replay(events)

    with pytest.raises(InvalidAmount):
        replay(events)
