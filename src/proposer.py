class Proposer():

    def __init__(self, processes, messenger, value):
        self.processes = processes
        self.messenger = messenger
        self.value = value
        self.maxPropNum = -1
        self.promises = dict()                # Dictionary that tells whether a promise has been received from a specific site
        self.resetPromises()


    # Phase 1 of the Synod algorithm
    def prepare(self):
        self.maxPropNum += 1
        resetPromises()

        # Send to all acceptors
        messenger.sendAll(('prepare', maxPropNum), self.processes)

    # Phase 2 of the Synod algorithm
    def receivePromise(self, message):
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

        if numPromises > len(self.processes) / 2:
            if allNull:
                v = self.value                            # if all promises had null values, use own value
            else:
                v = self.promises[maxProcess][1]          # accVal from promise with largest accNum

            messenger.sendall(('accept', self.maxPropNum, v))


    # Reset received promises to all be false.
    def resetPromises:
        for process in processes:
            self.promises[process] = None
