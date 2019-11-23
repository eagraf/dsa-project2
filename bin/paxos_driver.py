from proposer import Proposer
from acceptor import Acceptor
from learner import Learner
from planes import Planes
from event import Event
from stablestorage import StableStorage
import random

class PaxosDriver():

    def __init__(self, site, hosts, messenger):
        self.site = site
        self.hosts = hosts
        self.messenger = messenger

        self.store = StableStorage(site)
        log, accProps, maxPrep, accepts = self.store.initialize()

        self.proposer =  Proposer(site, hosts, messenger)
        self.acceptor = Acceptor(hosts, messenger, accProps, maxPrep)
        self.learner = Learner(hosts, messenger, self, log, accepts)
        
        self.airport = Planes()
        self.airport.fillPlane(self.learner.log)

        self.messenger.addListener(self.proposer)
        self.messenger.addListener(self.acceptor)
        self.messenger.addListener(self.learner)

        self.fillToCurrent()
    
    def fillToCurrent(self):
        self.fillHoles()
        id = random.randint(0,1000)
        ev = Event(id, 'filler', self.site)
        while (len(self.learner.log) == 0) or (len(self.learner.log) > 0 and self.learner.log[-1] != ev ):
            l = len(self.learner.log)
            #print("log position is", len(self.learner.log))
            if not self.proposer.prepare(ev, len(self.learner.log)):
                return False
            while l >= len(self.learner.log) or self.learner.log[l] == None:
                continue

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

        if holes:
            return False
        return True

            #self.airport.fillPlane(self.learner.log)

    def createReservation(self, event):
        if not self.fillHoles():
            return False
        while (len(self.learner.log) == 0) or (len(self.learner.log) > 0 and self.learner.log[-1] != event ):
            #print("HEREHERE\nHEREHEREHEREHEREHERE\nHEREHEREHEREHERE") 
            if self.airport.checkSpot(event):
                l = len(self.learner.log)
                #print("log position is", len(self.learner.log))
                if not self.proposer.prepare(event, len(self.learner.log)):
                    return False
                while l >= len(self.learner.log) or self.learner.log[l] == None:
                        continue
            else:
                return False
        #self.store.store()
        return True
        
    def cancelReservation(self, event):
        self.fillHoles()
        while (len(self.learner.log) == 0) or (len(self.learner.log) > 0 and self.learner.log[-1] != event ):
            #print ("here")
            if event.user in self.airport.allUsers:
                l = len(self.learner.log)
                #print("log position is", len(self.learner.log))
                if not self.proposer.prepare(event, len(self.learner.log)):
                    return False
                while l >= len(self.learner.log) or self.learner.log[l] == None:
                        continue
            else:
                return False
        #self.store.store()
        return True
    
    def newSpot(self):
        self.fillHoles()
        self.airport.fillPlane(self.learner.log)
        self.store.store(self.learner.log, self.acceptor.acceptedProposals, self.acceptor.maxPrepares, self.learner.accepts)
        


    
