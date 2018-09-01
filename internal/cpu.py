from collections import deque
from internal import pcb
from internal import hdd
from internal import memory


class CPU:
    __using_CPU = None

    def __init__(self, disk_count, frame_count):
        self.__level_queues = [deque() for i in range(3)]
        self.__frame_count = frame_count
        self.__disks = []
        self.__disk_count = disk_count
        self.__memory = memory.Mem(int(frame_count))

        for i in range(disk_count):
            disk = hdd.HDD()
            self.__disks.append(disk)

    def scheduler(self):
        # add process to queue and then refresh
        process = pcb.PCB()
        # allocate memory for process at page 0
        self.__memory.add_to_memory(0, process.pid)
        self.__level_queues[0].appendleft(process)
        self.refresh_lvl_0()

    def refresh_lvl_0(self):
        # if CPU is idle and there are no processes queued on level 0
        if not self.__using_CPU and not self.__level_queues[0]:
            self.refresh_lvl_1()

        # if CPU is idle let in a process from level 0
        elif not self.__using_CPU:
            self.__using_CPU = self.__level_queues[0].pop()

        # if level 0 has a queue and CPU is in use by a lower priority process: preempt
        elif self.__using_CPU.level > 0 and self.__level_queues[0]:
            self.priority_preempt()
            self.__using_CPU = self.__level_queues[0].pop()

        elif self.__using_CPU.level > 1 and self.__level_queues[1]:
            self.priority_preempt()
            self.__using_CPU = self.__level_queues[1].pop()

    # todo : flatten by making the first if a guardian clause
    def refresh_lvl_1(self):
        # if CPU is busy and there are processes waiting on level 0, do nothing
        if self.__using_CPU and self.__level_queues[0]:
            return
        # let in a level 1 process
        if self.__level_queues[1]:
            self.__using_CPU = self.__level_queues[1].pop()
        # if there are no processes queued on level 1, let in a level 2 process
        elif not self.__level_queues[1]:
            self.refresh_lvl_2()

    def refresh_lvl_2(self):
        if self.__using_CPU and self.__level_queues[0] and self.__level_queues[1]:
            return

        # let in a level 2 process
        if self.__level_queues[2]:
            self.__using_CPU = self.__level_queues[2].pop()

    def time_quantum(self):
        if not self.__using_CPU:
            print("Can't increase time quantum. CPU is idle.")
            return

        self.__using_CPU.increment_time_quantum()
        if self.__using_CPU.should_preempt():
            self.preempt()

    # preempt if process has exceeded time quanta allowed on for its level
    # add process to queue one level below its current priority level
    def preempt(self):
        process = self.__using_CPU
        process.preempt()
        self.__level_queues[process.which_queue_post_preempt()].appendleft(process)

        self.__using_CPU = None
        self.refresh_lvl_0()

    # preempt if a higher level process arrives
    # add process to front of it's priority level queue
    def priority_preempt(self):
        if self.__using_CPU.level == 1:
            self.__level_queues[1].append(self.__using_CPU)
        if self.__using_CPU.level == 2:
            self.__level_queues[2].append(self.__using_CPU)
        self.__using_CPU = None

    def terminate(self):
        if not self.__using_CPU:
            print("Can't terminate. CPU is idle.")
            return

        self.__memory.reclaim_memory(self.__using_CPU.pid)
        self.__using_CPU = None
        self.refresh_lvl_0()

    def request_io(self, num, file_name):
        if not self.__using_CPU:
            print("Cannot request I/O. CPU is idle.")
            return
        elif num >= self.__disk_count:
            print("Specified disk number does not exist.")
            return

        self.__disks[num].request_io(file_name, self.__using_CPU)

        self.__using_CPU = None
        self.refresh_lvl_0()

    def terminate_io(self, num):
        if num >= self.__disk_count:
            print("Specified disk number does not exist.")
            return
        elif not self.__disks[num].using_HDD:
            print("Cannot terminate I/O usage for disk {}. Disk is idle.".format(num))
            return

        process = self.__disks[num].terminate_io()

        process.reset_time_quanta()
        # process returned from hdd.terminate_io is put back into ready-queue
        if process.level == 0:
            self.__level_queues[0].append(process)
        elif process.level == 1:
            self.__level_queues[1].append(process)
        else:
            self.__level_queues[2].append(process)
        self.refresh_lvl_0()

    # add a specified page to memory
    def access_memory(self, page):
        if not self.__using_CPU:
            print ("Cannot access memory for process using CPU. CPU is idle.")
            return

        self.__memory.add_to_memory(page, self.__using_CPU.pid)

    # "Shows what process is currently using the CPU and what processes are waiting in the ready-queue. "
    def show_cpu(self):
        print ("")
        print("Using CPU:")
        if self.__using_CPU:
            self.__using_CPU.printCPU()
        else:
            print("[idle]")

        print("\nIn ready-queue: ")
        for i, queue in enumerate(self.__level_queues):
            print("Level {}:".format(i))
            if not queue:
                print("[empty]")
            else:
                for process in queue:
                    process.print()

        print ("")

    # "Shows what processes are currently using the hard disks and what processes are waiting to use them.
    # For each busy hard disk show the process that uses it and show its I/O-queue.
    # Make sure to display the file names (from the d command) for each process.
    # The enumeration of hard disks starts from 0."
    def show_disk(self):
        print ("")
        for i in range(self.__disks[0].hdd_count):
            print("Hard Disk {}:".format(i))
            print("Using disk:")
            if self.__disks[i].using_HDD:
                print("PID", self.__disks[i].using_HDD.pid, "is using", "\"" +
                      self.__disks[i].using_HDD.file_name + "\"")
            else:
                print("[idle]")
            print("In I/O queue:")
            for j in self.__disks[i].io_queue:
                print("PID", j.pid, "wants to use", "\"" + j.file_name + "\"")
            if not self.__disks[i].io_queue:
                print ("[empty]")
            print ("")

    # "Shows the state of memory. For each used frame display the process number that
    # occupies it and the page number stored in it.
    # The enumeration of pages and frames starts from 0.""
    def show_memory(self):
        self.__memory.show_memory()
