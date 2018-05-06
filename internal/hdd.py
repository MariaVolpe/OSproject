from collections import deque

class HDD:
    hdd_count = 0

    def __init__(self):
        HDD.hdd_count += 1
        self.io_queue = deque()
        self.using_HDD = None
        #name of file using HDD
        self.file_name = ""

    def request_io(self, file_name, process):
        process.file_name = file_name
        if self.using_HDD == None:
            self.using_HDD = process
            self.file_name = file_name
        else:
            self.io_queue.append(process)

    #stop process from using HDD, refresh I/O queue and then return the process
    def terminate_io(self):
        process = self.using_HDD
        process.file_name = ""
        self.using_HDD = None
        self.refresh_io()
        return process

    def refresh_io(self):
        if len(self.io_queue) == 0:
            self.using_HDD = None
        else:
            self.using_HDD = self.io_queue.popleft()
            self.file_name = self.using_HDD.file_name