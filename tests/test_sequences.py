import pytest

from ledger_domain.engine import replay, balances
from ledger_domain.errors import InsufficientFunds
from ledger_domain.events import AccountOpened, Deposited, Withdrawn, Transferred
from ledger_domain.utils import eid

matrix = [
    ("open+deposit+withdraw",
     [AccountOpened(eid("open_A"), "A"), Deposited(eid("deposit_A"), "A", 50), Withdrawn(eid("withdraw_A"), "A", 20)],
     {"A": 30},
     None),
    ("transfer A->B",
     [AccountOpened(eid("open_A"), "A"), AccountOpened(eid("open_B"), "B"), Deposited(eid("deposit_A"), "A", 10), Transferred(eid("transfer_A_to_B"), "A", "B", 5)],
     {"A": 5, "B": 5},
     None),
    ("invalid withdraw -> InsufficientFunds",
     [AccountOpened(eid("open_A"), "A"), Withdrawn(eid("withdraw_A"), "A", 1)],
     None,
     InsufficientFunds)
]
@pytest.mark.parametrize("case_name, events, expected_balances, expected_exc",
                         matrix,
                         ids=[row[0] for row in matrix])
def test_event_sequences_matrix(case_name, events, expected_balances, expected_exc):
    if expected_exc is not None:
        with pytest.raises(expected_exc):
            replay(events)
        return
    else:
        state = replay(events)
        assert balances(state) == expected_balances