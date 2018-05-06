class memory:

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
        

        #find frame of smallest timestamp (or first unused frame)
        min_timestamp = float("inf")
        for i in range(len(self.table["Timestamp"])):
            if self.table["Timestamp"][i] < min_timestamp:
                min_timestamp = i


        #add information to that frame
        self.table["Timestamp"][min_timestamp] = self.timestamp
        #increase timestamp
        self.timestamp += 1
        self.table["Page Number"][min_timestamp] = page
        self.table["PID"][min_timestamp] = pid
