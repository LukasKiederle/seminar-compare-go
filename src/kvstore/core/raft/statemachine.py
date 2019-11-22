from src.kvstore.core.raft.constant import FOLLOWER, CANDIDATE, LEADER


class StateMachine:

    current = None

    def __init__(self):
        self.current = FOLLOWER  # Follower

        self.validTransactions = {
            FOLLOWER: {FOLLOWER, CANDIDATE},
            CANDIDATE: {FOLLOWER, CANDIDATE, LEADER},
            LEADER: {FOLLOWER}
        }

    # processes a  transaction from state x to state y
    def next(self, next_state):
        if not self.is_transaction_valid(next_state):
            raise Exception('Invalid State transaction!')
        self.current = next_state

    # check if the transaction from one status into another is valid based on the validTransactions-map
    def is_transaction_valid(self, next_state):
        next_states = self.validTransactions[self.current]

        for state in next_states:
            if state == next_state:
                return True
        return False
