class PCB:

    __pid_count = 1

    def __init__(self):
        self.__pid = PCB.__pid_count
        PCB.__pid_count += 1
        self.__time_quantum = 0
        self.__level = 0
        self.__file_name = ""

    @property
    def pid_count(self):
        return PBC.__pid_count

    @property
    def pid(self):
        return self.__pid

    @property
    def time_quantum(self):
        return self.__time_quantum

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, value):
        self.__level = value

    @property
    def file_name(self):
        return self.__file_name

    @file_name.setter
    def file_name(self, name):
        self.__file_name = name

    def increment_time_quantum(self):
        if self.__level == 2:
            print("Increasing time quantum has no effect. Process in CPU belongs to level 2.")
            return
        self.__time_quantum += 1

    def reset_time_quanta(self):
        self.__time_quantum = 0

    def should_preempt(self):
        if self.__level == 0:
            return True
        elif self.__level == 1 and self.__time_quantum == 2:
            return True

        return False

    def preempt(self):
        self.reset_time_quanta()
        self.__level += 1
    
    def which_queue_post_preempt(self):
        return self.__level + 1

    def printCPU(self):
        print("PID", self.__pid, "from level", self.__level)

    def print(self):
        print("PID", i.pid)
