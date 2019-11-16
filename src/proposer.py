from message import Message

class Proposer():

    def __init__(self, site, processes, messenger):
        self.processes = processes
        self.messenger = messenger
        self.value = None 
        self.maxPropNum = 0
        self.proposalNumber = -1 
        self.index = processes.index(site)
        self.promises = dict()                # Dictionary that tells whether a promise has been received from a specific site
        self.resetPromises()

    # Find the next proposal number in the disjoint set for this site
    def nextNum(self):
        round = (self.maxPropNum // len(self.processes)) + 1
        n = (round * len(self.processes)) + self.index
        return n

    # Phase 1 of the Synod algorithm
    def prepare(self, value):
        self.proposalNum = self.nextNum()
        self.maxPropNum = self.proposalNum
        self.value = value
        self.resetPromises()

        # Send to all acceptors
        self.messenger.sendAll('prepare', (self.maxPropNum,))

    # Phase 2 of the Synod algorithm
    # Message has the contents ('promise', accNum, accVal)
    def receivePromise(self, message):

        # Update maxPropNum if necessary
        if message.contents[0] > self.maxPropNum:
            self.maxPropNum = message.contents[0]

        # Add a received promise
        self.promises[message.site] = (message.contents[0], message.contents[1])

        # Check if a majority of promises have been received
        numPromises = 0
        maxProcess = list(self.promises)[0]
        allNull = True
        for process, promise in self.promises.items:
            if promise != None:
                numPromises += 1
                if self.promises[maxProcess][0] < promise[0]:
                    maxProcess = process
                if promise[1] != None:
                    allNull = False

        # If a majority of sites return promises, send accepted number and value
        if numPromises > len(self.processes) / 2:
            if allNull:
                v = self.value                            # if all promises had null values, use own value
            else:
                v = self.promises[maxProcess][1]          # accVal from promise with largest accNum

            messenger.sendall('accept', (self.proposalNum, v))


    # Reset received promises to all be false.
    def resetPromises(self):
        for process in self.processes:
            self.promises[process] = None
