from message import Message
from functools import reduce
import time
import signal

class Proposer():

    def __init__(self, site, processes, messenger):
        self.processes = processes
        self.messenger = messenger
        self.proposals = list()
        self.maxPropNum = 0
        self.index = list(processes).index(site)

    # Find the next proposal number in the disjoint set for this site
    def nextNum(self):
        round = (self.maxPropNum // len(self.processes)) + 1
        n = (round * len(self.processes)) + self.index
        return n

    # Phase 1 of the Synod algorithm
    def prepare(self, value, slot, counter=0):
        print("prepare")

        # Make sure slots are initialized.
        if slot >= len(self.proposals):
            self.initializeSlots(slot)

        proposal = dict()
        proposal['value'] = value
        proposal['proposalNum'] = self.nextNum()
        proposal['accepted'] = False
        proposal['counter'] = counter
        proposal['promises'] = dict()
        for process in self.processes:
            proposal['promises'][process] = None

        self.proposals[slot] = proposal

        # Send to all acceptors
        self.messenger.sendAll('prepare', (proposal['proposalNum'],), slot)
        #self.proposalTime = time.time()

        # Set a 5 second timeout, retry up to 3 times.
        #if counter < 3:
        #    signal.signal(signal.SIGALRM, self.timeout)
        #    signal.alarm(5)

    def timeout(self, signum, frame):
        self.prepare(self.value, self.slot, )

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

        proposal = self.proposals[message.slot]

        # Add a received promise
        proposal['promises'][message.origin] = (message.contents[0], message.contents[1])

        # Check if a majority of promises have been received
        #numPromises = 0
        numPromises = reduce((lambda a, b: a + (1 if b != None else 0)), proposal['promises'].values(), 0)
        allNull = reduce((lambda a, b: a and (b == None or b == (None, None))), proposal['promises'].values(), True)  

        print(proposal['promises'])
        print("numPromises, allNull " + str(numPromises) + ", " + str(allNull))
        if numPromises > 0 and not allNull:
            actualPromises = list(filter((lambda a: a[1] != None and a[1][0] != None), list(proposal['promises'].items())))
            maxProcess = actualPromises[0]
            for promise in actualPromises:
                print(promise)
                if promise[1][0] > maxProcess[1][0]:
                    print(promise[1][1])
                    maxProcess = promise 


        # If a majority of sites return promises, send accepted number and value
        if numPromises > len(self.processes) / 2 and proposal['accepted'] == False:
            proposal['accepted'] = True
            if allNull:
                v = proposal['value']                            # if all promises had null values, use own value
            else:
                v = proposal['promises'][maxProcess[0]][1]          # accVal from promise with largest accNum

            self.messenger.sendAll('accept', (proposal['proposalNum'], v), message.slot)


    def initializeSlots(self, slot):
        for i in range(len(self.proposals), slot+1):
            self.proposals.append(None)