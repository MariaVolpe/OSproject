from collections import deque
from internal import pcb
from internal import hdd
from internal import memory


class CPU:
    __using_CPU = None

    def __init__(self, disk_count, frame_count):
        self.__level_queues = [deque() for i in range(3)]
        self.__disks = []
        self.__disk_count = disk_count
        self.__memory = memory.Mem(frame_count)

        for i in range(disk_count):
            disk = hdd.HDD()
            self.__disks.append(disk)

    def add_process(self):
        process = pcb.PCB()
        
        self.__memory.add_to_memory(0, process)
        self.__level_queues[0].appendleft(process)
        self.refresh_lvl_0()

    def refresh_lvl_0(self):
        # if CPU is idle and there are no processes queued on level 0
        if not self.__using_CPU and not self.__level_queues[0]:
            self.refresh_lvl_1()

        # if CPU is idle let in a process from level 0
        elif not self.__using_CPU:
            self.__using_CPU = self.__level_queues[0].pop()

        for level in range(2):
            if self.should_priority_preempt(level):
                self.priority_preempt()
                self.__using_CPU = self.__level_queues[level].pop()
                break

    def refresh_lvl_1(self):
        if self.__using_CPU and self.__level_queues[0]:
            return
        elif self.__level_queues[1]:
            self.__using_CPU = self.__level_queues[1].pop()
        elif not self.__level_queues[1]:
            self.refresh_lvl_2()

    def refresh_lvl_2(self):
        if self.__using_CPU and self.__level_queues[0] and self.__level_queues[1]:
            return
        elif self.__level_queues[2]:
            self.__using_CPU = self.__level_queues[2].pop()

    def increment_time_quanta(self):
        if not self.__using_CPU:
            print("Can't increase time quanta. CPU is idle.")
            return

        self.__using_CPU.increment_time_quanta()
        if self.__using_CPU.has_exceeded_time_quanta:
            self.preempt()

    def preempt(self):
        process = self.__using_CPU
        process.demote()
        self.__level_queues[process.which_queue].appendleft(process)

        self.__using_CPU = None
        self.refresh_lvl_0()

    def priority_preempt(self):
        self.__level_queues[self.__using_CPU.which_queue].append(self.__using_CPU)
        self.__using_CPU = None

    def terminate_process(self):
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
        process = self.__disks[num].terminate_io()
        if not process:
            print("Cannot terminate I/O usage for disk {}. Disk is idle.".format(num))
            return
        
        process.reset_time_quanta()

        self.__level_queues[process.which_queue].append(process)
        self.refresh_lvl_0()

    def add_to_memory(self, page):
        if not self.__using_CPU:
            print ("Cannot access memory for process using CPU. CPU is idle.")
            return

        self.__memory.add_to_memory(page, self.__using_CPU)

    def should_priority_preempt(self, level):
        if (self.__level_queues[level] and self.__using_CPU.is_lesser_priority_than(level)):
            return True
        return False

    def show_cpu(self):
        print ("")
        print("Using CPU:")
        if self.__using_CPU:
            self.__using_CPU.print_CPU_process()
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

    def show_disk(self):
        print ("")
        for i, disk in enumerate(self.__disks):
            print("Hard Disk {}:".format(i))
            disk.print()
            print ("")

    def show_memory(self):
        self.__memory.show_memory()
