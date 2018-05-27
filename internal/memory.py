class Mem:

    def __init__(self, frame_count):
        self.__frame_count = frame_count
        self.__timestamp = 1

        frame_list = []
        page_list = []
        pid_list = []
        timestamp_list = []

        self.__table = {"Frames" : frame_list, "Page Number" : page_list, "PID" : pid_list, "Timestamp" : timestamp_list}

        #intialize all values
        #frame list is enumerated, 0 to frame_count
        #pages and pid are set to -1
        #timestamp is set to 0
        for i in range(frame_count):
            frame_list.append(i)
            page_list.append(-1)
            pid_list.append(-1)
            timestamp_list.append(0)

    #add the information to frame with smallest timestamp (the least recently used)
    #if any memory is unused it will be placed in the first unused frame because 0 will be least recently used
    def add_to_memory(self, page, pid):
        #if page already belongs to process
        if pid in self.__table["PID"]:
            for i, val in enumerate(self.__table["PID"]):
                if self.__table["PID"][i] == pid:
                    if self.__table["Page Number"][i] == int(page):
                        self.update_timestamp(i)
                        return

        #find frame of smallest timestamp (or first unused frame)
        min_timestamp = float("inf")
        for i, val in enumerate(self.__table["Timestamp"]):
            if self.__table["Timestamp"][i] < min_timestamp:
                min_timestamp = self.__table["Timestamp"][i]
                min_index = i

        #add information to that frame
        self.__table["Timestamp"][min_index] = self.__timestamp
        #increase timestamp
        self.__timestamp += 1
        self.__table["Page Number"][min_index] = int(page)
        self.__table["PID"][min_index] = pid

    #if page already belongs to process, update timestamp
    def update_timestamp(self, index):
        self.__table["Timestamp"][index] = self.__timestamp
        self.__timestamp += 1

    #reclaim memory for a terminated process
    def reclaim_memory(self, pid):
        #check for pid in list of pids and reset values associated with it
        for i, val in enumerate(self.__table["PID"]):
            if self.__table["PID"][i] == pid:
                self.__table["Timestamp"][i] = 0
                self.__table["Page Number"][i] = -1
                self.__table["PID"][i] = -1

    # "Shows the state of memory. For each used frame display the process number that occupies it and the page number stored in it.
    # The enumeration of pages and frames starts from 0.""
    def show_memory(self):
        isEmpty = False
        print ("")
        for i, val in enumerate(self.__table["Frames"]):
            if self.__table["PID"][i] != -1:
                isEmpty = True
                print ("Frame: ", self.__table["Frames"][i], "\t", "Page: ", self.__table["Page Number"][i], "\t", "PID: ", self.__table["PID"][i], "\t", "Timestamp: ", self.__table["Timestamp"][i])

        if isEmpty == False:
            print ("No frames in use to show.")

        print ("")