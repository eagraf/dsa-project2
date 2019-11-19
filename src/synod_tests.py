from proposer import Proposer
from acceptor import Acceptor
from mock_messenger import MockMessenger, UniversalMessenger

def prepareTest():
    print("prepareTest")
    processes = ['alpha', 'beta', 'gamma']
    um = UniversalMessenger()
    messenger = MockMessenger('alpha', processes, um)
    p = Proposer('alpha', processes, messenger)
    p.prepare('ABC')
    um.printMessages()

#def promiseTest():
#    processes = ['alpha', 'beta', 'gamma']
#    messenger = MockMessenger('alpha', processes)
#    a = Acceptor(processes, messenger)
#    m = Message()

# Test a single proposal
def singleProposal():
    print("singleProposal")
    processes = ['alpha', 'beta', 'gamma']
    um = UniversalMessenger()
    m1 = MockMessenger('alpha', processes, um)
    m2 = MockMessenger('beta', processes, um)
    m3 = MockMessenger('gamma', processes, um)
    p1 = Proposer('alpha', processes, m1) 
    p2 = Proposer('beta', processes, m2)
    p3 = Proposer('gamma', processes, m3)
    a1 = Acceptor(processes, m1)
    a2 = Acceptor(processes, m2)
    a3 = Acceptor(processes, m3)

    p1.prepare('ABC')
    a1.promise(um.lastMessageToSite('alpha', 'prepare'))
    p1.receivePromise(um.lastMessageToSite('alpha', 'promise'))
    a2.promise(um.lastMessageToSite('beta', 'prepare'))
    p1.receivePromise(um.lastMessageToSite('alpha', 'promise'))
    a3.promise(um.lastMessageToSite('gamma', 'prepare'))
    p1.receivePromise(um.lastMessageToSite('alpha', 'promise'))

    a1.accept(um.lastMessageToSite('alpha', 'accept'))
    a2.accept(um.lastMessageToSite('beta', 'accept'))
    a3.accept(um.lastMessageToSite('gamma', 'accept'))

    um.printMessages()

# Test a proposal after one has already been accepted.
def secondProposal():
    print("secondProposal")
    processes = ['alpha', 'beta', 'gamma']
    um = UniversalMessenger()
    m1 = MockMessenger('alpha', processes, um)
    m2 = MockMessenger('beta', processes, um)
    m3 = MockMessenger('gamma', processes, um)
    p1 = Proposer('alpha', processes, m1) 
    p2 = Proposer('beta', processes, m2)
    p3 = Proposer('gamma', processes, m3)
    a1 = Acceptor(processes, m1)
    a2 = Acceptor(processes, m2)
    a3 = Acceptor(processes, m3)

    p1.prepare('ABC')
    a1.promise(um.lastMessageToSite('alpha', 'prepare'))
    p1.receivePromise(um.lastMessageToSite('alpha', 'promise'))
    a2.promise(um.lastMessageToSite('beta', 'prepare'))
    p1.receivePromise(um.lastMessageToSite('alpha', 'promise'))
    a3.promise(um.lastMessageToSite('gamma', 'prepare'))
    p1.receivePromise(um.lastMessageToSite('alpha', 'promise'))

    a1.accept(um.lastMessageToSite('alpha', 'accept'))
    a2.accept(um.lastMessageToSite('beta', 'accept'))
    a3.accept(um.lastMessageToSite('gamma', 'accept'))

    p2.prepare('XYZ')
    a1.promise(um.lastMessageToSite('alpha', 'prepare'))
    p2.receivePromise(um.lastMessageToSite('beta', 'promise'))
    a2.promise(um.lastMessageToSite('beta', 'prepare'))
    p2.receivePromise(um.lastMessageToSite('beta', 'promise'))
    a3.promise(um.lastMessageToSite('gamma', 'prepare'))
    p2.receivePromise(um.lastMessageToSite('beta', 'promise'))

    um.printMessages()

def rivalProposal():
    print("rivalProposal")
    processes = ['alpha', 'beta', 'gamma']
    um = UniversalMessenger()
    m1 = MockMessenger('alpha', processes, um)
    m2 = MockMessenger('beta', processes, um)
    m3 = MockMessenger('gamma', processes, um)
    p1 = Proposer('alpha', processes, m1) 
    p2 = Proposer('beta', processes, m2)
    p3 = Proposer('gamma', processes, m3)
    a1 = Acceptor(processes, m1)
    a2 = Acceptor(processes, m2)
    a3 = Acceptor(processes, m3)

    p1.prepare('ABC')
    a1.promise(um.lastMessageToSite('alpha', 'prepare'))
    p1.receivePromise(um.lastMessageToSite('alpha', 'promise'))
    a2.promise(um.lastMessageToSite('beta', 'prepare'))
    p1.receivePromise(um.lastMessageToSite('alpha', 'promise'))
    #a3.promise(um.lastMessageToSite('gamma', 'prepare'))
    #p1.receivePromise(um.lastMessageToSite('alpha', 'promise'))

    #a1.accept(um.lastMessageToSite('alpha', 'accept'))
    #a2.accept(um.lastMessageToSite('beta', 'accept'))
    #a3.accept(um.lastMessageToSite('gamma', 'accept'))

    p2.prepare('XYZ') # A majority of these need to be uncommented for XYZ to be accepted
    #a1.promise(um.lastMessageToSite('alpha', 'prepare'))
    #p2.receivePromise(um.lastMessageToSite('beta', 'promise'))
    a2.promise(um.lastMessageToSite('beta', 'prepare'))
    p2.receivePromise(um.lastMessageToSite('beta', 'promise'))
    a3.promise(um.lastMessageToSite('gamma', 'prepare'))
    p2.receivePromise(um.lastMessageToSite('beta', 'promise'))

    a1.accept(um.lastMessageToSite('alpha', 'accept'))
    a2.accept(um.lastMessageToSite('beta', 'accept'))
    a3.accept(um.lastMessageToSite('gamma', 'accept'))

    um.printMessages()

prepareTest()
singleProposal()
secondProposal()
rivalProposal()
