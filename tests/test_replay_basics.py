from ledger_domain.engine import replay
from ledger_domain.events import AccountOpened, Deposited, Withdrawn
from ledger_domain.models import AccountState


def test_correct_open_new_account():
    events = [AccountOpened("A")]
    state = replay(events)
    assert state.accounts["A"].balance == 0

def test_correct_add_deposit_to_account():
    events = [AccountOpened("A"), Deposited("A", amount=100)]
    state = replay(events)
    assert state.accounts["A"].balance == 100

def test_correct_withdraw_from_account():
    events = [AccountOpened("A"), Deposited("A", amount=100), Withdrawn("A", amount=30)]
    state = replay(events)
    assert state.accounts["A"].balance == 70
