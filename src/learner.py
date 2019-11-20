class Learner():

    def __init__(self, processes, messenger):
        self.processes = processes
        self.messenger = messenger
        self.accepts = list()
        self.log = list()

    def receiveAccepted(self, message):
        accNum, accVal = message.contents

        # Make sure slots are initialized.
        if message.slot >= len(self.log):
            self.initializeSlots(message.slot)

        # Return if a value has already been committed.
        if self.log[message.slot] != None:
            return

        # Add accept to set.
        if accNum not in self.accepts[message.slot]:
            self.accepts[message.slot][accNum] = set()
        self.accepts[message.slot][accNum].add(message.origin)

        # If a majority of accepts are received for the given proposal, commit to log
        if len(self.accepts[message.slot][accNum]) > len(self.processes)/2:
            print("Commit " + accVal)
            self.log[message.slot] = accVal

    def initializeSlots(self, slot):
        for i in range(len(self.log), slot+1):
            accepts = dict()
            self.accepts.append(accepts)
            self.log.append(None)


