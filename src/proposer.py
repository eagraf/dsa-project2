from message import Message
from functools import reduce

class Proposer():

    def __init__(self, site, processes, messenger):
        self.processes = processes
        self.messenger = messenger
        self.value = None 
        self.maxPropNum = 0
        self.proposalNumber = 0 
        self.index = list(processes).index(site)
        self.promises = dict()                # Dictionary that tells whether a promise has been received from a specific site
        self.accepted = False
        self.slot = 0
        self.resetPromises()

    # Find the next proposal number in the disjoint set for this site
    def nextNum(self):
        round = (self.maxPropNum // len(self.processes)) + 1
        n = (round * len(self.processes)) + self.index
        return n

    # Phase 1 of the Synod algorithm
    def prepare(self, value, slot):
        print("prepare")
        self.proposalNum = self.nextNum()
        self.maxPropNum = self.proposalNum
        self.value = value
        self.slot = slot
        self.resetPromises()

        # Send to all acceptors
        self.messenger.sendAll('prepare', (self.maxPropNum,), slot)

    def receive(self, message):
        if message.messageType == 'promise':
            self.receivePromise(message)

    # Phase 2 of the Synod algorithm
    # Message has the contents ('promise', accNum, accVal)
    def receivePromise(self, message):
        print("receivePromise")
        # Update maxPropNum if necessary
        if message.contents[0] != None:
            if message.contents[0] > self.maxPropNum:
                self.maxPropNum = message.contents[0]

        # Add a received promise
        self.promises[message.origin] = (message.contents[0], message.contents[1])

        # Check if a majority of promises have been received
        #numPromises = 0
        numPromises = reduce((lambda a, b: a + (1 if b != None else 0)), self.promises.values(), 0)
        allNull = reduce((lambda a, b: a and (b == None or b == (None, None))), self.promises.values(), True)  

        print(self.promises)
        print("numPromises, allNull " + str(numPromises) + ", " + str(allNull))
        if numPromises > 0 and not allNull:
            actualPromises = list(filter((lambda a: a[1] != None and a[1][0] != None), list(self.promises.items())))
            maxProcess = actualPromises[0]
            for promise in actualPromises:
                print(promise)
                if promise[1][0] > maxProcess[1][0]:
                    print(promise[1][1])
                    maxProcess = promise 


        # If a majority of sites return promises, send accepted number and value
        if numPromises > len(self.processes) / 2 and self.accepted == False:
            self.accepted = True
            if allNull:
                v = self.value                            # if all promises had null values, use own value
            else:
                v = self.promises[maxProcess[0]][1]          # accVal from promise with largest accNum

            self.messenger.sendAll('accept', (self.proposalNum, v), message.slot)


    # Reset received promises to all be false.
    def resetPromises(self):
        self.accepted = False
        for process in self.processes:
            self.promises[process] = None
