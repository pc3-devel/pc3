import time


class Clock(object):
    def __init__(self):
        self.startTime = time.time()

    def timePassed(self):
        return int(time.time() - self.startTime)


if __name__ == "__main__":
    clock = Clock()
    time.sleep(3)
    print clock.timePassed()
