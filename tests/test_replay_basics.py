from ledger_domain.engine import replay, balances
from ledger_domain.events import AccountOpened, Deposited, Withdrawn
from ledger_domain.utils import eid


def test_correct_open_new_account():
    events = [AccountOpened(eid("open_A"), "A")]
    state = replay(events)
    assert balances(state)["A"] == 0

def test_correct_add_deposit_to_account():
    events = [AccountOpened(eid("open_A"), "A"), Deposited(eid("deposit_A"), "A", amount=100)]
    state = replay(events)
    assert balances(state)["A"] == 100

def test_correct_withdraw_from_account():
    events = [AccountOpened(eid("open_A"), "A"), Deposited(eid("deposit_A"), "A", amount=100), Withdrawn(eid("withdraw_A"), "A", amount=30)]
    state = replay(events)
    assert balances(state)["A"] == 70
