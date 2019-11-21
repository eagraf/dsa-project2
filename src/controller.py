import sys
import os
import time
import json
import pickle
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
                continue

            elif command[0] == "send" and len(command) == 4:
                m = Message(self.siteID, command[3], command[1], command[2], 0)

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
                self.paxos_driver.testBoi()

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