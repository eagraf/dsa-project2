from message import Message

class Acceptor():

    def __init__(self, processes, messenger):
        self.processes = processes
        self.messenger = messenger
        self.maxPrepare = 0
        self.acceptedProposal = (None, None)

    # Phase 1 of the Synod algorithm
    # Message has contents (prepare', n)
    def promise(self, message):
        if message.contents[0] > self.maxPrepare:
            self.messenger.send(message.origin, 'promise', self.acceptedProposal)

    # Phase 2 of the Synod algorithm
    # Message has contents ('accept', accNum, accVal)
    def accept(self, message):
        if message.contents[0] > self.maxPrepare:
            self.acceptedProposal = (message.contents[0], message.contents[1])         # Accept the proposal
            self.messenger.sendAll('accepted', self.acceptedProposal)                 # Send to all learners accepted proposal