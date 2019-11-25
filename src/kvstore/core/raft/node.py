import random
from threading import Lock, Thread

from src.kvstore.core.raft.constant import FOLLOWER, CANDIDATE, LEADER
from src.kvstore.core.raft.repeatingtimer import RepeatingTimer
from src.kvstore.core.raft.replicatedlog import ReplicatedLog
from src.kvstore.core.raft.statemachine import StateMachine
from src.kvstore.core.raft.waitgroup import WaitGroup


class Node:

    def __init__(self, id):
        self.id = id
        self.state_machine = StateMachine()
        self.replicated_log = ReplicatedLog()
        self.election_timer = RepeatingTimer(5 + (random.randrange(10) / 10),
                                             self.election_timeout)  # 5s +- 1s
        self.heartbeat_timer = RepeatingTimer(2 + (random.randrange(10) / 10),
                                              self.heartbeat_timeout)  # 2s +- 1s to avoid conflicts
        self.current_term = 0
        self.votedFor = None
        self.stopped = False
        self.mutex = None
        self.cluster = None

    # starts a node for a cluster
    def start(self, cluster):
        self.mutex = Lock()
        with self.mutex:
            self.stopped = False
            self.cluster = cluster
            self.election_timer.reset()

    # stops a node
    def stop(self):
        self.mutex = Lock()
        with self.mutex:

            self.stopped = True
            self.heartbeat_timer.cancel()
            self.election_timer.cancel()
            self.state_machine.next(FOLLOWER)

    # this function is used when the election_timer runs out
    # an election process is started
    def election_timeout(self):
        self.mutex = Lock()
        with self.mutex:

            if self.stopped:
                return

            print('Election timeout.')

            if self.is_leader():
                raise Exception('The election timeout should not happen, when a node is LEADER.')
            self.start_election_process()

    # starts real election process
    # handles result of election
    # calls promotion function
    def start_election_process(self):
        self.current_term += 1
        self.state_machine.next(CANDIDATE)
        self.votedFor = None
        election_won = self.execute_election()

        if election_won:
            print("[" + str(self.id) + "] Election won. Now acting as leader.")
            self.switch_to_leader()
        else:
            print("Election was not won. Reset election timer")
            self.state_machine.next(FOLLOWER)
            # try again, split vote or cluster down
            self.election_timer.reset()

    # election process:
    # asks for votes of all others
    # return voting result
    def execute_election(self):
        print("-> Election")
        self.votedFor = self.id  # vote for yourself

        # used for thread sync
        wg = WaitGroup()

        nodes = self.cluster.get_remote_followers(self.id)
        votes = []

        # amount of threads to wait for
        wg.add(len(nodes))

        # this function calls the request_vote from all other known nodes in the cluster
        def request_votes():
            term, ok = node.request_vote(self.current_term, self.id, 0, 0)
            if term > self.current_term:
                # not not needed
                pass
            votes.append(ok)
            wg.done()

        for i, node in enumerate(nodes):
            Thread(target=request_votes).start()

        wg.wait()

        number_of_votes = 1  # Master votes for himself
        for vote in votes:
            if vote:  # if the person voted for me:
                number_of_votes += 1

        # check if over half of the cluster is alive and about to have a new master
        election_won = number_of_votes > len(self.cluster.allNodes) / 2

        print('<- Election:' + str(election_won))

        return election_won

    # SwitchToLeader does the state change from CANDIDATE to LEADER.
    def switch_to_leader(self):
        self.state_machine.next(LEADER)
        self.election_timer.cancel()
        self.heartbeat_timer.reset()

    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # Leader only functions
    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

    def heartbeat_timeout(self):
        self.mutex = Lock()
        with self.mutex:

            if self.stopped:
                return

            if not self.is_leader():
                raise Exception('sendHeartbeat should only run in LEADER state!')

            print('-> Heartbeat')

            wg = WaitGroup()

            nodes = self.cluster.get_remote_followers(self.id)

            if len(nodes) > 1:
                result = []

                # amount of threads to wait for
                wg.add(len(nodes))

                def send_votes():
                    term, ok = node.append_entries(self.current_term, self.id, 0, 0, None, 0)
                    if term > self.current_term:
                        node.switch_to_follower()
                    result.append(ok)
                    wg.done()

                for i, node in enumerate(nodes):
                    Thread(target=send_votes).start()

                wg.wait()

                print('<- Heartbeat')
            else:
                print("Cluster contains only one node")

    # SwitchToFollower switches a LEADER or CANDIDATE to the follower state
    def switch_to_follower(self):
        if self.is_leader():
            self.heartbeat_timer.cancel()
            self.state_machine.next(FOLLOWER)
        elif self.is_candidate():
            self.state_machine.next(FOLLOWER)

    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # Follower RPC - Heartbeat & Replication
    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

    def append_entries(self, term, leader_id, prev_log_index, prev_log_termin, entries, leader_commit):
        self.mutex = Lock()
        with self.mutex:

            if self.stopped:
                return self.current_term, False  # stopped node

            if term < self.current_term:
                return self.current_term, False  # 5.1

            # see 5.1 - If one servers term is smaller than the others, then it updates its current term to the larger
            # value.
            if term > self.current_term:
                self.current_term = term

                if self.is_leader() or self.is_candidate():
                    self.switch_to_follower()
                    return self.current_term, False

            if entries is None or len(entries) == 0:
                print('Heartbeat received. Reset election timer.')
                # n.electionTimer.resetC <- true
                self.election_timer.reset()

            else:
                # TODO replicate logs
                print("[%s] AppendEntries replicate logs on Node: %s", self.state_machine.current, self.id)

            return self.current_term, True

    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # Follower RPC - Leader Election
    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

    # RequestVote is called by candidates to gather votes.
    # It returns the current term to update the candidate
    # It returns true when the candidate received vote.
    def request_vote(self, term, candidate_id, last_log_index, last_log_term):
        self.mutex = Lock()
        with self.mutex:

            if self.stopped:
                return self.current_term, False

            self.election_timer.reset()

            # see RequestVoteRPC receiver implementation 1
            if term < self.current_term:
                return self.current_term, False

            # see RequestVoteRPC receiver implementation 2
            if self.votedFor is not None and term == self.current_term:
                return self.current_term, False

            # see 5.1 - If one servers term is smaller than the others, then it updates its current term to the larger
            # value.
            if term > self.current_term:
                self.current_term = term
                if self.is_candidate() or self.is_leader():
                    self.switch_to_follower()

            self.votedFor = candidate_id
            print("RequestVote received from Candidate " + str(candidate_id) + ". Vote OK.")

            return self.current_term, True

    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =
    # Helper Methods for nodes
    # == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == == =

    def log(self):
        print("[%s] [%s] [%s] : %s", self.id, self.state_machine.current, self.current_term)

    def is_leader(self):
        return self.state_machine.current == LEADER

    def is_follower(self):
        return self.state_machine.current == FOLLOWER

    def is_candidate(self):
        return self.state_machine.current == CANDIDATE
