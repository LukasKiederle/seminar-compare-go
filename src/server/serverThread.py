from threading import Thread


class ServerThread(Thread):

    def __init__(self, counter):
        Thread.__init__(self)
        self.counter = counter

    def run(self):
        try:
            for i in range(0, self.counter):
                print(i)
        finally:
            print("Thread finished")
