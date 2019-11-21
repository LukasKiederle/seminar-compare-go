from src.kvstore.core.raft.constant import FOLLOWER, CANDIDATE, LEADER


class StateMachine:

    def __init__(self):
        self.current = FOLLOWER  # Follower

        self.validTransactions = {
            FOLLOWER: {FOLLOWER, CANDIDATE},
            CANDIDATE: {FOLLOWER, CANDIDATE, LEADER},
            LEADER: {FOLLOWER}
        }

    def next(self, next_state):
        if not self.is_transaction_valid(next_state):
            raise Exception('Invalid State transaction!')
        self.current = next_state

    def is_transaction_valid(self, next_state):
        next_states = self.validTransactions[self.current]

        for state in next_states:
            if state == next_state:
                return True
        return False
