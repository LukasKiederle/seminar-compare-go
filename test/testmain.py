import unittest

from src.server.serverThread import ServerThread


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())


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
