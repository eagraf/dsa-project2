from message import Message

class Acceptor():

    def __init__(self, processes, messenger, accProps, maxPreps):
        self.processes = processes
        self.messenger = messenger
        self.maxPrepares = maxPreps
        self.acceptedProposals = accProps

    def receive(self, message):
        if message.messageType == 'prepare':
            self.promise(message)
        elif message.messageType == 'accept':
            self.accept(message)

    # Phase 1 of the Synod algorithm
    # Message has contents (prepare', n)
    def promise(self, message):
        print("promise")
        # Make sure slots are initialized.
        if message.slot >= len(self.acceptedProposals):
            self.initializeSlots(message.slot)

        if message.contents[0] > self.maxPrepares[message.slot]:
            self.maxPrepares[message.slot] = message.contents[0]
            self.messenger.send(message.origin, 'promise', self.acceptedProposals[message.slot], message.slot)

    # Phase 2 of the Synod algorithm
    # Message has contents ('accept', accNum, accVal)
    def accept(self, message):
        print("accept")
        # Make sure slots are initialized.
        if message.slot >= len(self.acceptedProposals):
            self.initializeSlots(message.slot)

        if message.contents[0] >= self.maxPrepares[message.slot]:
            self.acceptedProposals[message.slot] = (message.contents[0], message.contents[1])         # Accept the proposal
            self.messenger.sendAll('accepted', self.acceptedProposals[message.slot], message.slot)                 # Send to all learners accepted proposal

    def initializeSlots(self, slot):
        for i in range(len(self.acceptedProposals), slot+1):
            self.maxPrepares.append(0)
            self.acceptedProposals.append((None, None))