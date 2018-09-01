from collections import deque


class HDD:
    __hdd_count = 0

    def __init__(self):
        HDD.__hdd_count += 1
        self.__io_queue = deque()
        self.__using_HDD = None
        self.__file_name = ""

    @property
    def hdd_count(self):
        return HDD.__hdd_count

    @property
    def io_queue(self):
        return self.__io_queue

    @property
    def using_HDD(self):
        return self.__using_HDD

    @property
    def file_name(self):
        return self.__file_name

    def request_io(self, new_file, process):
        process.file_name = new_file
        if not self.__using_HDD:
            self.__using_HDD = process
            self.__file_name = new_file
        else:
            self.__io_queue.append(process)

    # stop process from using HDD, refresh I/O queue and then return the process
    # only is called from CPU class if there is a process currently using the disk
    def terminate_io(self):
        process = self.__using_HDD
        process.file_name = ""
        self.__using_HDD = None
        self.refresh_io()
        return process

    def refresh_io(self):
        if not self.__io_queue:
            self.__using_HDD = None
        else:
            self.__using_HDD = self.__io_queue.popleft()
            self.__file_name = self.__using_HDD.file_name

    def print(self):
        print("Using disk:")
        if self.__using_HDD:
            message = "is using"
            self.__using_HDD.print_disk(message)
        else:
            print("[idle]")
        print("In I/O queue:")
        for j in self.__io_queue:
            message = "wants to use"
            j.print_disk(message)
        if not self.__io_queue:
            print ("[empty]")