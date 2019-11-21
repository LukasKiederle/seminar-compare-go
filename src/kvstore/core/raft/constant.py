from src.kvstore.core.raft.state import State

FOLLOWER = State(0)
CANDIDATE = State(1)
LEADER = State(2)
