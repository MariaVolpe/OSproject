##############################
#
# Maria Volpe
# Section 3
#
##############################

from internal import cpu

def evaluate(s, obj, page_size):

    #todo : exit function

    d = {"A" : new_process, "Q" : time_quantum, "t" : terminate, "S r" : show_cpu, "S i" : show_disk, "S m" : show_memory}

    if s in d:
        d[s](obj)

    #if user accidentally enters empty string, do nothing
    elif s == "":
        dummy = 0
    else:
        special_action(obj, s, page_size)


def special_action(obj, s, page_size):
    arr = s.split()

    #do nothing if too few arguments
    if len(arr) < 2:
        print("Invalid command.")
        return

    #d number file_name
    if arr[0] == "d":
        #do nothing if specified disk isn't an integer
        if not arr[1].isdigit():
            print("Invalid command.")
            return
        #do nothing if too few arguments
        if len(arr) < 3:
            print("Invalid command.")
            return

        obj.request_io(arr[1], arr[2])

    #D number
    elif arr[0] == "D":
        #do nothing if specified disk isn't an integer
        if not arr[1].isdigit():
            print("Invalid command.")
            return
        obj.terminate_io(arr[1])

    #m address
    elif arr[0] == "m":
        if not arr[1].isdigit():
            print("Invalid command.")
            return
        #page number = address/page size
        page = int(arr[1]) / int(page_size)
        obj.access_memory(page)

    #error
    else:
        print("Invalid command.")


def new_process(obj):
    obj.scheduler()


def time_quantum(obj):
    obj.time_quantum()


def terminate(obj):
    obj.terminate()


def show_cpu(obj):
    obj.show_cpu()


def show_disk(obj):
    obj.show_disk()


def show_memory(obj):
    obj.show_memory()


def main():
    
    flag = True
    while (flag):

        RAM = input("How much RAM? ")

        while (not RAM.isdigit()):
            print ("Not a valid value for RAM.")
            RAM = input("How much RAM? ")
        page_size = input("Size of page? ")

        while (not page_size.isdigit()):
            print ("Not a valid value for page size.")
            page_size = input("Size of page? ")

            print ("Not a valid value for page size.")

        if int(RAM) % int(page_size) == 0:
            flag = False
        else:
            print ("Not valid values for RAM and page size.")
            print ("RAM value should be evenly divisible by page size.")

    disk_count = input("Number of disks? ")

    while (not disk_count.isdigit()):
        print ("Not a valid value for number of disks.")
        disk_count = input("Number of disks? ")

    print ("")

    #frame number = ram/page size
    frame_count = int(RAM) / int(page_size)

    #object of class CPU
    obj = cpu.CPU(int(disk_count), frame_count)

    while(True):
        s = input()
        s.strip()

        evaluate(s, obj, page_size)


if __name__ == "__main__":
    main()