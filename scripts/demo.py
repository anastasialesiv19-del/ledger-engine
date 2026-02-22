from ledger_domain.engine import replay, balances
from ledger_domain.errors import InsufficientFunds, InvalidAmount
from ledger_domain.events import AccountOpened, Deposited, Transferred
from ledger_domain.utils import eid


def main():
    print("== OK scenario ==")
    events_ok = [AccountOpened(eid("open_A"), "A"),
                 AccountOpened(eid("open_B"), "B"),
                 Deposited(eid("deposit_A"), "A", 100),
                 Transferred(eid("transfer_A_to_B"), "A", "B", 40)]
    state = replay(events_ok)
    print(f"Balances after replay (ok):\n {balances(state)}\n")

    print("== Duplicate event_id ignored ==")
    events_with_duplicates = [AccountOpened(eid("open_A"), "A"),
                              AccountOpened(eid("open_B"), "B"),
                              Deposited(eid("deposit_A"), "A", 100),
                              Transferred(eid("transfer_A_to_B"), "A", "B", 40),
                              Transferred(eid("transfer_A_to_B"), "A", "B", 40)]
    state = replay(events_with_duplicates)
    print(f"Balances after replay (with duplicates):\n {balances(state)}\n")

    print("== Invalid event ==")
    events_with_exception = [AccountOpened(eid("open_A"), "A"),
                             Deposited(eid("deposit_A"), "A", 0)]
    try:
        replay(events_with_exception)
    except InvalidAmount:
        print("InvalidAmount caught: deposit amount must be > 0")



if __name__ == "__main__":
    main()
