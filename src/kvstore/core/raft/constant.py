from src.kvstore.core.raft.state import State

# these 3 states represent the only available states in the raft cluster
FOLLOWER = State(0)
CANDIDATE = State(1)
LEADER = State(2)
