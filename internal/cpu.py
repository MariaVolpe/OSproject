from collections import deque

class CPU:

    using_CPU = None

    def __init__(self, process):
        dummy = 0
        self.lvl_0_q = deque()
        self.lvl_1_q = deque()
        self.lvl_2_q = deque()

    def scheduler(self, process):
        self.level_0(process)

    def level_0(self, process):
        #add process to queue and then refresh
        lvl_0_q.append(process)
        self.refresh_lvl_0()

    #Todo: will this return an error if queue is empty?
    def refresh_lvl_0(self):
        if self.using_CPU == None:
            self.using_CPU = lvl_0_q.popleft()

    def refresh_lvl_1(self):
        if self.using_CPU == None and len(lvl_0_q) == 0:
            self.using_CPU = lvl_1_q.popleft()

    def refresh_lvl_2(self):
        if self.using_CPU == None and len(lvl_0_q) == 0 and len(lvl_1_q) == 0:
            self.using_CPU = lvl_2_q.popleft()

    #terminate process in CPU
    def terminate(self):
        self.using_CPU = None
        #todo: RECLAIM MEMORY

    #"Shows what process is currently using the CPU and what processes are waiting in the ready-queue. "
    def show_cpu(self):
        print("Using CPU:")
        print(self.using_CPU.pid)

        print("In ready-queue: ")

        print("Level 0: ")
        if len(self.lvl_0_q) == 0:
            print("[empty]")
        else:
            for i in self.lvl_0_q:
                print(i.pid)

        print("Level 1: ")
        if len(self.lvl_1_q) == 0:
            print("[empty]")
        else:
            for i in self.lvl_1_q:
                print(i.pid)

        print("Level 2: ")
        if len(self.lvl_2_q) == 0:
            print("[empty]")
        else:
            for i in self.lvl_2_q:
                print(i.pid)


    #todo
    # "Shows what processes are currently using the hard disks and what processes are waiting to use them.
    # For each busy hard disk show the process that uses it and show its I/O-queue.
    # Make sure to display the filenames (from the d command) for each process. The enumeration of hard disks starts from 0."
    def show_disk(self):
        dummy = 0


    #todo
    # "Shows the state of memory. For each used frame display the process number that occupies it and the page number stored in it.
    # The enumeration of pages and frames starts from 0.""
    def show_memory(self):
        dummy = 0