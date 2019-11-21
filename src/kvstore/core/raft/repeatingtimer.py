from __future__ import print_function

from threading import Timer, Lock


class RepeatingTimer(object):
    interval = 0

    def __init__(self, interval, f, *args, **kwargs):
        self.interval = interval
        self.f = f
        self.args = args
        self.kwargs = kwargs

        self.timer = None

    def callback(self):
        self.f(*self.args, **self.kwargs)
        self.start()

    def cancel(self):
        if self.timer is not None:
            self.timer.cancel()

    def start(self):
        self.timer = Timer(self.interval, self.callback)
        self.timer.start()

    # t = RepeatingTimer(3, hello)
    # t.start()
    # https://stackoverflow.com/questions/24072765/timer-cannot-restart-after-it-is-being-stopped-in-python
