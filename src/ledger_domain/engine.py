from ledger_domain.errors import AccountNotFound, InvalidAmount, InsufficientFunds
from ledger_domain.events import AccountOpened, Deposited, Withdrawn, Transferred
from ledger_domain.models import LedgerState, AccountState


def replay(events) -> LedgerState:
    state = LedgerState(accounts={})
    for event in events:
        state = apply_event(state, event)

    return state

def apply_event(state, event) -> LedgerState:
    match event:
        case AccountOpened():
            if event.account_id not in state.accounts:
                state.accounts[event.account_id] = AccountState(event.account_id)
            return state

        case Deposited():
            if event.account_id not in state.accounts:
                raise AccountNotFound()
            if event.amount <= 0:
                raise InvalidAmount()
            state.accounts[event.account_id].balance += event.amount
            return state

        case Withdrawn():
            if event.account_id not in state.accounts:
                raise AccountNotFound()
            if event.amount <= 0:
                raise InvalidAmount()
            if state.accounts[event.account_id].balance - event.amount < 0:
                raise InsufficientFunds()
            state.accounts[event.account_id].balance -= event.amount
            return state

        case Transferred():
            if (event.from_account_id not in state.accounts
                    or event.to_account_id not in state.accounts):
                raise AccountNotFound()
            if event.amount <= 0:
                raise InvalidAmount()
            if state.accounts[event.from_account_id].balance - event.amount < 0:
                raise InsufficientFunds()
            state.accounts[event.from_account_id].balance -= event.amount
            state.accounts[event.to_account_id].balance += event.amount
            return state

        case _:
            raise ValueError("Unknown event")


def balances(state: LedgerState) -> dict[str, int]:
    balance = {}
    for account_id, account in state.accounts.items():
        balance[account_id] = account.balance
    return balance