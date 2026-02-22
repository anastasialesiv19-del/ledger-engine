from ledger_domain.engine import replay, balances
from ledger_domain.events import AccountOpened, Deposited, Transferred


def main():
    events_ok = [AccountOpened("e1", "A"), AccountOpened("e2", "B"), Deposited("e3", "A", 100), Transferred("e4", "A", "B", 40)]
    state = replay(events_ok)
    print(f"Balances after replay (ok): \n {balances(state)}")

    events_with_duplicates = [AccountOpened("e1", "A"), AccountOpened("e2", "B"), Deposited("e3", "A", 100),
                 Transferred("e4", "A", "B", 40), Transferred("e4", "A", "B", 40)]
    state = replay(events_with_duplicates)
    print(f"Balances after replay (with duplicates): \n {balances(state)}")


if __name__ == "__main__":
    main()
