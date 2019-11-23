import pickle

# TODO make this a wrapper for Wuubern
class StableStorage:

    def __init__(self, pid):
        self.log = None
        self.accProps = None
        self.maxPrep = None
        self.accepts = None
        self.siteID = pid
        

    def store(self, log, accP, maxP, acc):
        ''' Pickle the process state and store in a file. '''
        self.log = log
        self.accProps = accP
        self.maxPreps = maxP
        self.accepts = acc
        pickle.dump(self.log, open('./storage/log' + self.siteID + '.p','wb'))
        pickle.dump(self.accepts, open('./storage/accepts' + self.siteID + '.p','wb'))
        pickle.dump(self.accProps, open('./storage/acceptedProposals' + self.siteID + '.p','wb'))
        pickle.dump(self.maxPreps, open('./storage/maxPrepares' + self.siteID + '.p','wb'))

    #def receive(self, clock, pID, np):
    #    ''' Listener function called whenever messenger receives a new message. '''
    #    self.store()

    def initialize(self):
        try:
            self.log = pickle.load(open('./storage/log' + self.siteID + '.p', 'rb'))
            self.accepts = pickle.load(open('./storage/accepts' + self.siteID + '.p', 'rb'))
            self.accProps = pickle.load(open('./storage/acceptedProposals' + self.siteID + '.p', 'rb'))
            self.maxPreps = pickle.load(open('./storage/maxPrepares' + self.siteID + '.p', 'rb'))
        except FileNotFoundError:
            self.log = list()
            self.accepts = list()
            self.accProps = list()
            self.maxPreps = list()

        return self.log, self.accProps, self.maxPreps, self.accepts