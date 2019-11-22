import pickle

# TODO make this a wrapper for Wuubern
class StableStorage:

    def __init__(self, pid):
        self.log = None
        self.accProps = None
        self.maxPrep = None
        self.siteID = pid
        

    def store(self, log, accP, maxP):
        ''' Pickle the process state and store in a file. '''
        self.log = log
        self.accProps = accP
        self.maxPrep = maxP
        pickle.dump(self.log, open('./storage/log' + self.siteID + '.p','wb'))
        pickle.dump(self.accProps, open('./storage/acceptedProposals' + self.siteID + '.p','wb'))
        pickle.dump(self.maxPrep, open('./storage/maxPrepare' + self.siteID + '.p','wb'))

    #def receive(self, clock, pID, np):
    #    ''' Listener function called whenever messenger receives a new message. '''
    #    self.store()

    def initialize(self):
        try:
            self.log = pickle.load(open('./storage/log' + self.siteID + '.p', 'rb'))
            self.accProps = pickle.load(open('./storage/acceptedProposals' + self.siteID + '.p', 'rb'))
            self.maxPrep = pickle.load(open('./storage/maxPrepare' + self.siteID + '.p', 'rb'))
        except FileNotFoundError:
            self.log = list()
            self.accProps = list()
            self.maxPrep = 0

        return self.log, self.accProps, self.maxPrep