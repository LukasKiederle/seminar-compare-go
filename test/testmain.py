import unittest

from src.kvstore.core.raft.constant import FOLLOWER, CANDIDATE, LEADER
from src.kvstore.core.raft.state import State
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
