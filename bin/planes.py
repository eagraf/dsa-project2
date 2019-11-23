class Planes:

    def __init__(self):
        self.allPlanes = [[0, 0]  for i in range(20)]
        self.allUsers = dict()

    def __str__(self):
        s = ""
        for i, pln in enumerate(self.allPlanes):
            s += "Plane " + str(i+1) +":\t"+ str(pln) +"\t\t"
            if(i%2 == 1):
                s+= "\n"
        return s

    def fillPlane(self, eventsLog):
        for event in eventsLog:
            if event.type == "cancel":
                self.deleteReservation(event)
            elif event.type == "reserve":
                self.makeReservation(event)  
    
    def checkSpot(self, event):
        for pln in event.planes:
            if self.allPlanes[pln -1][0] != 0 and self.allPlanes[pln -1][1] != 0:
                return False
        return True

    def makeReservation(self,event):
        for pln in event.planes:
            if self.allPlanes[pln -1][0] == 0 or self.allPlanes[pln -1][0] == event:
                self.allPlanes[pln -1][0] = event
            elif self.allPlanes[pln -1][1] == 0 or self.allPlanes[pln -1][1] == event:
                self.allPlanes[pln -1][1] = event
            #elif self.allPlanes[pln -1][0] != 0 and self.allPlanes[pln -1][1] != 0:
                #print("ERROR!!!!- Log has been double booked!")
                #print(event)
            #else:
            #    print("HUH, should never get here 1")

        if event.user in self.allUsers.keys():
            self.allUsers[event.user].add(tuple(event.planes))
        else:
            self.allUsers[event.user] = set()
            self.allUsers[event.user].add(tuple(event.planes))

        

    def deleteReservation(self, event):
        #if event.user not in self.allUsers.keys():
            #print("ERROR!!!!- Delete not possible!")
            #print(event)
            #return
        #print(self.allUsers[event.user])
        for pln in self.allUsers[event.user]:
            for p in pln:
                if self.allPlanes[p -1][0] !=0 and event.user == self.allPlanes[p -1][0].user:
                    self.allPlanes[p -1][0] = 0
                elif self.allPlanes[p -1][1] !=0 and event.user == self.allPlanes[p -1][1].user:
                    self.allPlanes[p -1][1] = 0
        self.allUsers.pop(event.user)
                
    def getView(self):
        temp = list()
        for key, value in self.allUsers.items():
            l = list()
            for v in value:
                l = l + list(v)
            tup = (key, l)
            temp.append(tup) 
        return sorted(temp)