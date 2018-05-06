class Mem:

    def __init__(self, frame_count):
        self.frame_count = frame_count
        self.timestamp = 1

        frame_list = []
        page_list = []
        pid_list = []
        timestamp_list = []

        self.table = {"Frames" : frame_list, "Page Number" : page_list, "PID" : pid_list, "Timestamp" : timestamp_list}

        #intialize all values
        #frame list is enumerated
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
        index = -1
        if pid in self.table["PID"]:
            for i in range(len(self.table["PID"])):
                if self.table["PID"][i] == pid:
                    index = i
            if self.table["Page Number"][index] == page:
                self.update(index)

        #find frame of smallest timestamp (or first unused frame)
        min_timestamp = float("inf")
        for i in range(len(self.table["Timestamp"])):
            if self.table["Timestamp"][i] < min_timestamp:
                min_timestamp = self.table["Timestamp"][i]
                min_index = i

        #add information to that frame
        self.table["Timestamp"][min_index] = self.timestamp
        #increase timestamp
        self.timestamp += 1
        self.table["Page Number"][min_index] = page
        self.table["PID"][min_index] = pid

    #if page already belongs to process, update timestamp
    def update(self, index):
        self.table["Timestamp"][index] = self.timestamp
        self.timestamp += 1

    #reclaim memory for a terminated process
    def reclaim_memory(self, pid):
        #check for pid in list of pids and reset values associated with it
        for i in range(len(self.table["PID"])):
            if self.table["PID"][i] == pid:
                self.table["Timestamp"][i] = 0
                self.table["Page Number"][i] = -1
                self.table["PID"][i] = -1

    # "Shows the state of memory. For each used frame display the process number that occupies it and the page number stored in it.
    # The enumeration of pages and frames starts from 0.""
    def show_memory(self):
        for i in range(len(self.table["Frames"])):
            if self.table["PID"][i] != -1:
                print ("Frame: ", self.table["Frames"][i], "\t", "Page: ", self.table["Page Number"][i], "\t", "PID: ", self.table["PID"][i])