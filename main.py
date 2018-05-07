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
        arr = s.split()

        # todo : throw errors if missing arguments
        #d number file_name
        if arr[0] == "d":
            obj.request_io(arr[1], arr[2])

        #D number
        elif arr[0] == "D":
            obj.terminate_io(arr[1])

        #m address
        elif arr[0] == "m":
            #page number = address/page size
            page = int(arr[1]) / int(page_size)
            obj.access_memory(page)

        #error
        else:
            dummy = 0


def new_process(obj):
    obj.scheduler()

#todo : stop if there are no processes
def time_quantum(obj):
    obj.time_quantum()

def terminate(obj):
    obj.terminate()

def show_cpu(obj):
    obj.show_cpu()

def show_disk(obj):
    obj.show_disk()

#todo : if there are no processes, output a message
def show_memory(obj):
    obj.show_memory()


def main():
    RAM = input("How much RAM? ")
    page_size = input("Size of page? ")

    #frame number = ram/page size
    frame_count = int(RAM) / int(page_size)

    #todo : calculate
    disk_count = 2

    #object of class
    obj = cpu.CPU(disk_count, frame_count)

    while(True):
        s = input()
        s.strip()

        evaluate(s, obj, page_size)

if __name__ == "__main__":
    main()