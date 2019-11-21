from message import Message

class Acceptor():

    def __init__(self, processes, messenger):
        self.processes = processes
        self.messenger = messenger
        self.maxPrepare = 0
        self.acceptedProposal = (None, None)

    def receive(self, message):
        print("hello")
        if message.messageType == 'prepare':
            self.promise(message)
        elif message.messageType == 'accept':
            self.accept(message)

    # Phase 1 of the Synod algorithm
    # Message has contents (prepare', n)
    def promise(self, message):
        print("promise")
        if message.contents[0] > self.maxPrepare:
            self.messenger.send(message.origin, 'promise', self.acceptedProposal, message.slot)

    # Phase 2 of the Synod algorithm
    # Message has contents ('accept', accNum, accVal)
    def accept(self, message):
        print("accept")
        if message.contents[0] > self.maxPrepare:
            self.acceptedProposal = (message.contents[0], message.contents[1])         # Accept the proposal
            self.messenger.sendAll('accepted', self.acceptedProposal, message.slot)                 # Send to all learners accepted proposal