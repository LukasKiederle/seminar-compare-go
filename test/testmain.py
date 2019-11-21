import time
import unittest
from threading import Timer

from src.kvstore.core.raft.cluster import Cluster
from src.kvstore.core.raft.constant import FOLLOWER, CANDIDATE, LEADER
from src.kvstore.core.raft.node import Node
from src.kvstore.core.raft.repeatingtimer import RepeatingTimer
from src.kvstore.core.raft.statemachine import StateMachine
from src.server.serverThread import ServerThread
from src.kvstore.core.kvstoreimpl import KvStore


class TestKvStoreImpl(unittest.TestCase):

    def test_store_and_get_key_value(self):
        kv_store = KvStore()
        kv_store.setString("1", "value1")
        self.assertEqual("value1", kv_store.getString("1"))


class TestState(unittest.TestCase):

    def test_state_creation(self):
        state1 = FOLLOWER
        state2 = CANDIDATE
        state3 = LEADER

        self.assertEqual(0, state1.state_id)
        self.assertEqual(1, state2.state_id)
        self.assertEqual(2, state3.state_id)


class TestStateMachine(unittest.TestCase):

    def test_statemachine_next(self):
        statemachine = StateMachine()
        self.assertEqual(0, statemachine.current.state_id)

        statemachine.next(FOLLOWER)
        self.assertEqual(0, statemachine.current.state_id)

        statemachine.next(CANDIDATE)
        self.assertEqual(1, statemachine.current.state_id)

        statemachine.next(LEADER)
        self.assertEqual(2, statemachine.current.state_id)

        # self.assertRaises(Exception, statemachine.next(CANDIDATE))


class TestClusterWithNodes(unittest.TestCase):
    def test_cluster_start(self):
        n1 = Node(0)
        n2 = Node(1)
        n3 = Node(2)
        n4 = Node(3)
        n5 = Node(4)

        nodes = [n1, n2, n3, n4, n5]

        cluster = Cluster(nodes)

        cluster.start_all()

        # time.sleep(10)

        # ok, err = cluster.check()

        # self.assertTrue(ok)

        # cluster.stop_all()

        # time.sleep(5)

    def test_if_timer_time_differs(self):
        n1 = Node(0)
        n2 = Node(1)
        n3 = Node(2)
        n4 = Node(3)
        n5 = Node(4)

        print("n1: " + str(n1.election_timer.interval))
        print("n2: " + str(n2.election_timer.interval))
        print("n3: " + str(n3.election_timer.interval))
        print("n4: " + str(n4.election_timer.interval))
        print("n5: " + str(n5.election_timer.interval))

        # fails sometimes :)
        self.assertNotEqual(n1.election_timer.interval, n2.election_timer.interval
                            or n1.election_timer.interval, n2.election_timer.interval)


class TestServerThreadsWithRaft(unittest.TestCase):

    def test_numberofthreadsstarted(self):
        thread_number = 8
        threads_started_counter = 0

        for x in range(thread_number):
            server = ServerThread(x)
            # Setting daemon to True will let the main thread exit even though the workers are blocking
            server.daemon = True
            server.start()
            threads_started_counter += 1

        while threads_started_counter < 8:
            pass

        self.assertEqual(threads_started_counter, thread_number)


if __name__ == '__main__':
    unittest.main()
