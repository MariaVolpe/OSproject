from collections import deque

class HDD:
    hdd_count = 0

    def __init__(self):
        HDD.hdd_count += 1
        self.io_queue = deque()
        self.using_HDD = None

    def request_io(self, process):
        if self.using_HDD = None:
            self.using_HDD = process
        else:
            self.io_queue.append(process)

    def terminate_io(self):
        #return process to CPU
        #todo: goes back to cpu?
        process = self.using_HDD
        self.refresh_io()
        return process

    def refresh_io(self):
        if len(self.io_queue) == 0:
            self.using_HDD = None
        else:
            self.using_HDD = self.io_queue.popleft()
        