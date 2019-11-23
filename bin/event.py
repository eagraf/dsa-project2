class Event:

    def __init__(self, i, typ, usr, plnsLst = None):
        self.id = i
        self.type = typ
        self.user = usr
        self.planes = plnsLst
    
    def __str__(self):
        #s = "Id:" + str(self.id) + '\t'
        s = str(self.type) + ' '
        s += self.user
        if(self.planes != None):
            for i in range(len(self.planes) -1):
                s += ' ' + str(self.planes[i]) + ','
            s += ' ' + str(self.planes[-1])

        return s

    __repr__ = __str__
    
    def same(self, other):
        return(
            type(self) == type(other) and
            self.type == other.type and
			self.user == other.user and
			self.planes == other.planes
			)
    
    def __eq__(self, other): 
        return(
            type(self) == type(other) and
            self.id == other.id and
            self.type == other.type and
			self.user == other.user and
			self.planes == other.planes
			)

    def __ne__(self, other):
        return (not self == other)
    
    def __hash__(self):
        return hash((self.type, self.user, self.planes))