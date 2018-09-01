from internal import cpu


class Interface:

    def __init__(self):
        self.page_size = ""
        self.s = ""
        self.obj = self.begin()
        # build list of commands user can input
        self.commands = {"A": self.obj.add_process, "Q": self.obj.time_quantum, "t": self.obj.terminate,
                         "S r": self.obj.show_cpu, "S i": self.obj.show_disk, "S m": self.obj.show_memory}

    def evaluate(self):
        if self.s == "":
            return
        if self.s == "Quit" or self.s == "quit":
            exit()

        # check if user input is in dict of commands and call the command
        # if not call special_action
        self.commands.get(self.s, self.special_action)()

    def special_action(self):
        arr = self.s.split()

        if len(arr) < 2:
            print("Invalid command.")
            return

        # d number file_name
        if arr[0] == "d":
            if not arr[1].isdigit():
                print("Invalid command.")
                return
            if len(arr) < 3:
                print("Invalid command.")
                return

            self.obj.request_io(int(arr[1]), arr[2])

        # D number
        elif arr[0] == "D":
            if not arr[1].isdigit():
                print("Invalid command.")
                return
            self.obj.terminate_io(int(arr[1]))

        # m address
        elif arr[0] == "m":
            if not arr[1].isdigit():
                print("Invalid command.")
                return
            # page number = address/page size
            page = int(arr[1]) / int(self.page_size)
            self.obj.add_to_memory(page)

        else:
            print("Invalid command.")

    def begin(self):
        flag = True
        while flag:
            ram = input("How much RAM? ")

            while not ram.isdigit():
                print ("Not a valid value for RAM.")
                ram = input("How much RAM? ")

            self.page_size = input("Size of page? ")

            while not self.page_size.isdigit():
                print ("Not a valid value for page size.")
                self.page_size = input("Size of page? ")

                print ("Not a valid value for page size.")

            if int(ram) % int(self.page_size) == 0:
                flag = False
            else:
                print ("Not valid values for RAM and page size.")
                print ("RAM value should be evenly divisible by page size.")

        disk_count = input("Number of disks? ")

        while not disk_count.isdigit():
            print ("Not a valid value for number of disks.")
            disk_count = input("Number of disks? ")

        print ("")
        # frame number = ram/page size
        frame_count = int(ram) / int(self.page_size)

        # object of class CPU
        self.obj = cpu.CPU(int(disk_count), frame_count)
        return self.obj

    def run(self):
        while True:
            self.s = input()
            self.s.strip()
            self.evaluate()


def main():
    obj = Interface()
    obj.run()


if __name__ == "__main__":
    main()