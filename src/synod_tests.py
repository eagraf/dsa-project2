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
    a1.promise(um.lastMessageToSite('alpha'))
    a2.promise(um.lastMessageToSite('beta'))
    a3.promise(um.lastMessageToSite('gamma'))
    um.printMessages()

prepareTest()
singleProposal()
