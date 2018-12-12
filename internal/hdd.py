from collections import deque


class HDD:

    def __init__(self):
        self.__io_queue = deque()
        self.__using_HDD = None

    def request_io(self, new_file, process):
        process.file_name = new_file
        if not self.__using_HDD:
            self.__using_HDD = process
        else:
            self.__io_queue.append(process)

    def terminate_io(self):
        if not self.__using_HDD:
            return None

        process = self.__using_HDD
        process.file_name = ""

        self.__using_HDD = None
        self.manage_disk()

        return process

    def manage_disk(self):
        if not self.__io_queue:
            self.__using_HDD = None
        else:
            self.__using_HDD = self.__io_queue.popleft()

    def print(self):
        print("Using disk:")
        if self.__using_HDD:
            message = "is using"
            self.__using_HDD.print_disk_process(message)
        else:
            print("[idle]")

        print("In I/O queue:")
        for process in self.__io_queue:
            message = "wants to use"
            process.print_disk_process(message)
        if not self.__io_queue:
            print ("[empty]")