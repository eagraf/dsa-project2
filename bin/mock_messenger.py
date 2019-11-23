from message import Message 

# MockMessenger class for unit testing
class MockMessenger():

    def __init__(self, site, processes, universal):
        self.site = site
        self.processes = processes
        self.universal = universal

    def send(self, destination, messageType, contents, slot):
        self.universal.addMessage(Message(self.site, destination, messageType, contents, slot))

    def sendAll(self, messageType, contents, slot):
        for p in self.processes:
            self.universal.addMessage(Message(self.site, p, messageType, contents, slot))


class UniversalMessenger():

    def __init__(self):
        self.messages = list()

    def addMessage(self, message):
        self.messages.append(message)

    def printMessages(self):
        for m in self.messages:
            print('%s -> %s: %s %s' % (m.origin, m.destination, m.messageType, m.contents))

    def lastMessageToSite(self, site, messageType):
        for m in reversed(self.messages):
            if m.destination == site and m.messageType == messageType:
                return m
