class PCB:

    pid_count = 1

    def __init__(self):
        self.pid = self.pid_count
        PCB.pid_count += 1
        self.time_quantum = 0
        self.level = 0
        self.file_name = ""