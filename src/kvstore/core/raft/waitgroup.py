import threading


class WaitGroup(object):
    """WaitGroup is like Go sync.WaitGroup.

    Without all the useful corner cases.
    """

    def __init__(self):
        self.count = 0
        self.cv = threading.Condition()

    # add amount of processes
    def add(self, n):
        self.cv.acquire()
        self.count += n
        self.cv.release()

    # call out that a process stopped
    def done(self):
        self.cv.acquire()
        self.count -= 1
        if self.count == 0:
            self.cv.notify_all()
        self.cv.release()

    # wait for all processes to be done
    def wait(self):
        self.cv.acquire()
        while self.count > 0:
            self.cv.wait()
        self.cv.release()
