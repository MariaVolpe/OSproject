from collections import deque
from internal import pcb
from internal import hdd
from internal import memory

class CPU:

    using_CPU = None

    def __init__(self, disk_count, frame_count):
        self.lvl_0_q = deque()
        self.lvl_1_q = deque()
        self.lvl_2_q = deque()
        self.frame_count = frame_count
        self.disks = []
        self.disk_count = disk_count
        self.memory = memory.Mem(int(frame_count))

        for i in range(disk_count):
            disk = hdd.HDD()
            self.disks.append(disk)

    def scheduler(self):
        #add process to queue and then refresh
        process = pcb.PCB()
        #allocate memory for process at page 0
        self.memory.add_to_memory(0, process.pid)
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
        if self.using_CPU == None and len(self.lvl_0_q) == 0:
            if len(self.lvl_1_q) != 0:
                self.using_CPU = self.lvl_1_q.popleft()
            #if there are no processes queued on level 0, let in a level 1 process
            elif len(self.lvl_1_q) == 0:
                self.refresh_lvl_2()

    def refresh_lvl_2(self):
        #if CPU is idle and there are no higher priority processes, let in a level 2 process
        if self.using_CPU == None and len(self.lvl_0_q) == 0 and len(self.lvl_1_q) == 0:
            if len(self.lvl_2_q) != 0:
                self.using_CPU = self.lvl_2_q.popleft()

    #increase time quantum for process using CPU
    def time_quantum(self):
        #do nothing if CPU is not being used
        if self.using_CPU == None:
            print("Can't increase time quantum. CPU is idle.")
            return

        self.using_CPU.time_quantum +=1
        if self.using_CPU.level == 0:
            self.preempt()
        if self.using_CPU.level == 1 and self.using_CPU.time_quantum == 2:
            self.preempt()
        if self.using_CPU.level == 2:
            print("Increasing time quantum has no effect. Process in CPU belongs to level 2.")

    #preempt if process has exceeded time quantums allowed on for its level
    #add process to queue one level below its current priority level
    def preempt(self):
        #reset time quantums
        self.using_CPU.time_quantum = 0
        process = self.using_CPU
        if self.using_CPU.level == 0:
            process.level = 1
            self.lvl_1_q.append(process)
        elif self.using_CPU.level == 1:
            process.level = 2
            self.lvl_2_q.append(process)
        self.using_CPU = None
        self.refresh_lvl_0()

    #preempt if a higher level process arrives
    #add process to front of it's priority level queue
    def priority_preempt(self):
        if self.using_CPU.level == 1:
            self.lvl_1_q.appendleft(self.using_CPU)
        if self.using_CPU.level == 2:
            self.lvl_2_q.appendleft(self.using_CPU)
        self.using_CPU = None

    #terminate process in CPU
    def terminate(self):
        #do nothing if CPU is not being used
        if self.using_CPU == None:
            print("Can't terminate. CPU is idle.")
            return

        #reclaim memory
        self.memory.reclaim_memory(self.using_CPU.pid)
        self.using_CPU = None
        self.refresh_lvl_0()

    #request I/O for specified disk
    def request_io(self, num, file_name):
        #do nothing if no process is using CPU
        if self.using_CPU == None:
            print("Cannot request I/O. CPU is idle.")
            return
        #do nothing if disk requested does not exist
        elif int(num) >= self.disk_count:
            print("Specified disk number does not exist.")
            return

        self.disks[int(num)].request_io(file_name, self.using_CPU)
        #remove process from CPU
        self.using_CPU = None
        self.refresh_lvl_0()

    #terminate I/O for specified disk
    def terminate_io(self, num):
        #do nothing if disk requested does not exist
        if int(num) >= self.disk_count:
            print("Specified disk number does not exist.")
            return
        #do nothing if disk requested is not being used by any process
        elif self.disks[int(num)].using_HDD == None:
            print("Cannot terminate I/O usage for disk {}. Disk is idle.".format(num))
            return
        
        process = self.disks[int(num)].terminate_io()

        #process returned from hdd.terminate_io is put back into ready-queue
        if process.level == 0:
            self.lvl_0_q.append(process)
        elif process.level == 1:
            self.lvl_1_q.append(process)
        else:
            self.lvl_2_q.append(process)
        self.refresh_lvl_0()


    #add a specified page to memory
    def access_memory(self, page):
        #do nothing if no process is using CPU
        if self.using_CPU == None:
            print ("Cannot access memory for process using CPU. CPU is idle.")
            return

        self.memory.add_to_memory(page, self.using_CPU.pid)

    #"Shows what process is currently using the CPU and what processes are waiting in the ready-queue. "
    def show_cpu(self):
        print ("")
        print("Using CPU:")
        if self.using_CPU != None:
            print("PID", self.using_CPU.pid, "from level", self.using_CPU.level)
        else:
            print("[idle]")

        print ("")
        print("In ready-queue: ")

        print("Level 0: ")
        if len(self.lvl_0_q) == 0:
            print("[empty]")
        else:
            for i in self.lvl_0_q:
                print("PID", i.pid)

        print("Level 1: ")
        if len(self.lvl_1_q) == 0:
            print("[empty]")
        else:
            for i in self.lvl_1_q:
                print("PID", i.pid)

        print("Level 2: ")
        if len(self.lvl_2_q) == 0:
            print("[empty]")
        else:
            for i in self.lvl_2_q:
                print("PID", i.pid)

        print ("")

    # "Shows what processes are currently using the hard disks and what processes are waiting to use them.
    # For each busy hard disk show the process that uses it and show its I/O-queue.
    # Make sure to display the filenames (from the d command) for each process. The enumeration of hard disks starts from 0."
    def show_disk(self):
        print ("")
        for i in range(self.disks[0].hdd_count):
            print( "Hard Disk {}:".format(i) )
            print( "Using disk:")
            if self.disks[i].using_HDD != None:
                print("PID", self.disks[i].using_HDD.pid, "is using", "\"" + self.disks[i].using_HDD.file_name + "\"")
            else:
                print( "[idle]" )
            print( "In I/O queue:")
            for j in self.disks[i].io_queue:
                print("PID", j.pid, "wants to use",  "\"" + j.file_name + "\"")
            if len(self.disks[i].io_queue) == 0:
                print ("[empty]")
            print ("")

    # "Shows the state of memory. For each used frame display the process number that occupies it and the page number stored in it.
    # The enumeration of pages and frames starts from 0.""
    def show_memory(self):
        self.memory.show_memory()