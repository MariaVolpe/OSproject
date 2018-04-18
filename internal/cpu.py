from collections import deque
from internal import pcb

class CPU:

    using_CPU = None

    def __init__(self):
        dummy = 0
        self.lvl_0_q = deque()
        self.lvl_1_q = deque()
        self.lvl_2_q = deque()

    def scheduler(self, process):
        #add process to queue and then refresh
        self.lvl_0_q.append(process)
        self.refresh_lvl_0()
        
    def refresh_lvl_0(self):
        #if CPU is idle and there are no processes queued on level 0
        if self.using_CPU == None and len(self.lvl_0_q) == 0:
            self.refresh_lvl_1()

        #if CPU is idle let in a process from level 0
        elif self.using_CPU == None:
            self.using_CPU = self.lvl_0_q.popleft()

        #if level 0 has a queue and CPU is in use by a lower priority process: preempt
        elif self.using_CPU.level != 0 and len(self.lvl_0_q) != 0:
            self.priority_preempt()
            self.using_CPU = self.lvl_0_q.popleft()

    def refresh_lvl_1(self):
        #if CPU is idle and there are no processes queued on level 0, let in a level 1 process
        if self.using_CPU == None and len(lvl_0_q) == 0:
            self.using_CPU = lvl_1_q.popleft()
            #if there are no processes queued on level 0, let in a level 1 process
            if len(self.lvl_1_q) == 0:
                self.refresh_lvl_2()

    def refresh_lvl_2(self):
        #if CPU is idle and there are no higher priority processes, let in a level 2 process
        if self.using_CPU == None and len(lvl_0_q) == 0 and len(lvl_1_q) == 0:
            self.using_CPU = lvl_2_q.popleft()

    def time_quantum(self):
        self.using_CPU.time_quantum +=1
        if self.using_CPU.level == 0:
            self.preempt()
        if self.using_CPU.level == 1 and self.using_CPU.time_quantum == 2:
            self.preempt()

    #preempt if process has exceeded time quantums allowed on for its level
    def preempt(self):
        if self.using_CPU.level == 0:
            lvl_1_q.append(process)
        else:
            lvl_2_q.append(process)
        self.using_CPU = None
        self.refresh_lvl_0()

    #preempt if a higher level process arrives
    def priority_preempt(self):
        if self.using_CPU.level == 1:
            lvl_1_q.appendleft(self.using_CPU)
        if self.using_CPU.level == 2:
            lvl_2_q.appendleft(self.using_CPU)
        self.using_CPU = None

    #terminate process in CPU
    def terminate(self):
        self.using_CPU = None
        #todo: RECLAIM MEMORY

    #"Shows what process is currently using the CPU and what processes are waiting in the ready-queue. "
    def show_cpu(self):
        print("Using CPU:")
        if self.using_CPU != None:
            print(self.using_CPU.pid)
        else:
            print("[empty]")

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