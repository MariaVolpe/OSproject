##############################
#
# Maria Volpe
# Section 3
#
##############################

#from internal import 

def evaluate(s, obj):

    d = {"A" : new_process, "Q" : time_quantum, "t" : terminate, "S r" : show_cpu, "S i" : show_disk, "S m" : show_memory}

    if s in d:
        d[s]()

    else:
        #d number file_name
        if "d" in s:
            dummy = 0

        #D number
        elif "D" in s:
            dummy = 0

        #m address
        elif "m" in s:
            dummy = 0

        #error
        else:
            dummy = 0


def new_process(obj):
    process = internal.PCB()
    obj.scheduler(process)

def time_quantum(obj):
    dummy = var

def terminate(obj):
    obj.terminate()

def show_cpu(obj):
    obj.show_cpu()

def show_disk(obj):
    obj.show_disk()

def show_memory(obj):
    obj.show_memory()


def main():
    RAM = input("How much RAM?")
    page = input("Size of page?")

    #object of class
    obj =


    while(True):
        s = input()
        s.strip()

        evaluate(s, obj)

if __name__ == "__main__"
    main()