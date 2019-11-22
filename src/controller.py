import sys
import os
import time
import json
import pickle
import random
from event import Event
from messenger import Messenger
from message import Message
from paxos_driver import PaxosDriver


class Controller:

    def __init__(self):
        self.siteID = sys.argv[1]
        with open('knownhosts.json') as hosts_file:
        	self.hosts = json.load(hosts_file)['hosts']

        self.messenger = Messenger(self.hosts[self.siteID], self.hosts, self.siteID)
        self.paxos_driver = PaxosDriver(self.siteID, self.hosts, self.messenger)
        self.handle_user_input()

    def handle_user_input(self):
		#Main loop for handling user input
        command = input().split(" ")
        while command[0] != 'quit':
            if command[0] == "reserve" and len(command) == 3:
                plns = command[2].split(',')
                plns = [int(x) for x in plns]
                id = random.randint(0,1000)
                ev = Event(id, command[0], command[1], plns)
                if not self.paxos_driver.createReservation(ev):
                    print("Cannot create reservation")
            
            elif command[0] == "cancel" and len(command) == 2:
                id = random.randint(0,1000)
                ev = Event(id, command[0], command[1])
                if not self.paxos_driver.cancelReservation(ev):
                    print("Reservation already canceled")

            elif command[0] == "view" and len(command) == 1:
                view = self.paxos_driver.airport.getView()
                for v in view:
                    print(v[0], end = " ")
                    for p in range(len(v[1]) -1):
                        print(v[1][p], end = ", ")
                    print(v[1][-1])
                
            elif command[0] == "log" and len(command) == 1:
                log = self.paxos_driver.learner.log
                for event in log:
                    print(event)

            elif command[0] == "send" and len(command) == 4:
                Message(self.siteID, command[3], command[1], command[2], 0)

                tempHost = self.hosts[command[3]]
                host = (tempHost['ip_address'], tempHost['udp_end_port'])

                self.messenger.send(command[3], command[1], command[2], 0)

                #self.messenger.send(host, pickle.dumps(m))

            elif command[0] == "sendall" and len(command) == 3:
                #m = Message(self.siteID, command[3], command[1], command[2], 0)

                tempHosts = list()
                for _, host in self.hosts.items():
                    tempHosts.append((host['ip_address'], host['udp_end_port']))

                #self.messenger.sendAll(tempHosts, pickle.dumps(m))
                self.messenger.sendAll(command[1], command[2], 0)

            elif command[0] == "prepare":
                self.paxos_driver.testBoi(command[1])

            else:
                print("invalid command")

            # Wait for next command
            command = input().split(" ")
        
        print("exiting...")
        os._exit(0)


def handle_test_file():
	''' Execute a sequence of commands with timings rather than taking user input. '''
	print("Handling test file")

if __name__== "__main__":
	controller = Controller()