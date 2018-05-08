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
        return

    #d number file_name
    if arr[0] == "d":
        #do nothing if specified disk isn't an integer
        if arr[1].isdigit() == False:
            return
        #do nothing if too few arguments
        if len(arr) < 3:
            return

        obj.request_io(arr[1], arr[2])

    #D number
    elif arr[0] == "D":
        #do nothing if specified disk isn't an integer
        if arr[1].isdigit() == False:
            return
        obj.terminate_io(arr[1])

    #m address
    #todo : does address have to be int? maybe isdigit won't work
    elif arr[0] == "m":
        if arr[1].isdigit() == False:
            return
        #page number = address/page size
        page = int(arr[1]) / int(page_size)
        obj.access_memory(page)

    #error
    else:
        dummy = 0


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
    # todo : error if inputted wrong
    # can these be floats?
    
    RAM = input("How much RAM? ")

    while (RAM.isdigit() == False):
        print ("Not a valid value for RAM.")
        RAM = input("How much RAM? ")

    page_size = input("Size of page? ")

    while (page_size.isdigit() == False):
        print ("Not a valid value for page size.")
        page_size = input("Size of page? ")

    disk_count = input("Number of disks? ")

    while (disk_count.isdigit() == False):
        print ("Not a valid value for number of disks.")
        disk_count = input("Number of disks? ")

    print ("")
    
    #frame number = ram/page size
    frame_count = int(RAM) / int(page_size)

    #object of class
    obj = cpu.CPU(int(disk_count), frame_count)

    while(True):
        s = input()
        s.strip()

        evaluate(s, obj, page_size)

if __name__ == "__main__":
    main()