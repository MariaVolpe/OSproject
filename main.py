from internal import cpu


class Interface:

    def __init__(self):
        self.__page_size = ""
        self.__input = ""
        self.__cpu = self.initialize()
        self.__commands = {
            "A": self.__cpu.add_process,
            "Q": self.__cpu.increment_time_quanta,
            "t": self.__cpu.terminate_process,
            "S r": self.__cpu.show_cpu,
            "S i": self.__cpu.show_disk,
            "S m": self.__cpu.show_memory,
        }

    def evaluate(self):
        if self.__input == "":
            return
        if self.__input == "Quit" or self.__input == "quit":
            exit()

        # check if user input is in dict of commands and call the command
        # if not call special_action
        self.__commands.get(self.__input, self.special_action)()

    def special_action(self):
        arr = self.__input.split()

        if len(arr) < 2:
            print("Invalid command.")
            return

        # d number file_name
        if arr[0] == "d":
            if not arr[1].isdigit() or len(arr) < 3:
                print("Invalid command.")
                print("Disk usage: d disk_number file_name")
                return

            self.__cpu.request_io(int(arr[1]), arr[2])

        # D number
        elif arr[0] == "D":
            if not arr[1].isdigit():
                print("Invalid command.")
                print("Disk termination usage: D disk_number")
                return
            self.__cpu.terminate_io(int(arr[1]))

        # m address
        elif arr[0] == "m":
            if not arr[1].isdigit():
                print("Invalid command.")
                return
            # page number = address/page size
            page = int(arr[1]) / int(self.__page_size)
            self.__cpu.add_to_memory(int(page))

        else:
            print("Invalid command.")

    def initialize(self):
        flag = True
        while flag:
            ram = input("How much RAM? ")

            while not ram.isdigit():
                print ("Not a valid value for RAM.")
                ram = input("How much RAM? ")

            self.__page_size = input("Size of page? ")

            while not self.__page_size.isdigit():
                print ("Not a valid value for page size.")
                self.__page_size = input("Size of page? ")

                print ("Not a valid value for page size.")

            if int(ram) % int(self.__page_size) == 0:
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
        frame_count = int(ram) / int(self.__page_size)

        self.__cpu = cpu.CPU(int(disk_count), int(frame_count))
        return self.__cpu

    def run(self):
        while True:
            self.__input = input()
            self.__input.strip()
            self.evaluate()


def main():
    interface = Interface()
    interface.run()


if __name__ == "__main__":
    main()