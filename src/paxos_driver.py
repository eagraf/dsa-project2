from proposer import Proposer
from acceptor import Acceptor
from learner import Learner
from planes import Planes

class PaxosDriver():

    def __init__(self, site, hosts, messenger):
        self.site = site
        self.hosts = hosts
        self.messenger = messenger

        self.proposer =  Proposer(site, hosts, messenger)
        self.acceptor = Acceptor(hosts, messenger)
        self.learner = Learner(hosts, messenger, self)
        self.airport = Planes()

        self.messenger.addListener(self.proposer)
        self.messenger.addListener(self.acceptor)
        self.messenger.addListener(self.learner)

    def testBoi(self, value):
        self.proposer.prepare(value, 0)

    def fillHoles(self):
        holes = True
        temp = 0
        while holes or temp != 3:
            holes = False
            for i in range(len( self.learner.log )):
                if self.learner.log[i] == None:
                    self.proposer.prepare(None, i)
                    holes = True
            temp += 1

            self.airport.fillPlane(self.learner.log)

    def createReservation(self, event):
        self.fillHoles()
        while (len(self.learner.log) == 0) or (len(self.learner.log) > 0 and self.learner.log[-1] != event): 
            if self.airport.checkSpot(event):
                print("log position is", len(self.learner.log))
                self.proposer.prepare(event, len(self.learner.log))
            else:
                return False
        return True
        
    def cancelReservation(self, event):
        self.fillHoles()
        if event.user in self.airport.allUsers:

            self.proposer.prepare(event, len(self.learner.log))
            return True
        else:
            return False


    
