from proposer import Proposer
from acceptor import Acceptor
from learner import Learner

class PaxosDriver():

    def __init__(self, site, hosts, messenger):
        self.site = site
        self.hosts = hosts
        self.messenger = messenger

        self.proposer =  Proposer(site, hosts, messenger)
        self.acceptor = Acceptor(hosts, messenger)
        self.learner = Learner(hosts, messenger)

        self.messenger.addListener(self.proposer)
        self.messenger.addListener(self.acceptor)
        self.messenger.addListener(self.learner)

    def testBoi(self, value):
        self.proposer.prepare(value, 0)