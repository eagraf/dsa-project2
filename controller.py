import sys
import os
import time
import json
import pickle
from messenger import Messenger
from message import Message


class Controller:

    def __init__(self):
        self.siteID = sys.argv[1]
        with open('knownhosts.json') as hosts_file:
        	self.hosts = json.load(hosts_file)['hosts']

		#self.hostToID = dict()
        count = 0
        for key in sorted(self.hosts.keys()):
			#self.hostToID[key] = count
            self.hosts[key]['id'] = count
            count += 1
        
        self.messenger = Messenger(self.hosts[self.siteID], self.hosts, self.siteID)
		#self.airport = planes.Planes()

		#self.store = StableStorage()
        if len(sys.argv) >= 3:
            handle_test_file()
        else:
			#wu = imp.Wuubern(len(hosts), hostToID[siteID])
			#wu, self.airport = self.store.initialize(len(self.hosts), self.hosts[self.siteID]['id'])
			#self.messenger.add_listener(wu)
			#self.messenger.add_listener(self.store)
			#self.messenger.add_listener(self.airport)
            self.handle_user_input()


	#def handle_user_input(wu, messenger, hosts, hostToID, siteID, airport, stable_storage):
    def handle_user_input(self):
		#Main loop for handling user input
        command = input().split(" ")
        while command[0] != 'quit':
            if command[0] == "reserve" and len(command) == 3:
                continue

            elif command[0] == "send" and len(command) == 4:
                m = Message(self.siteID, command[1], command[2])

                tempHost = self.hosts[command[3]]
                host = (tempHost['ip_address'], tempHost['udp_end_port'])

                self.messenger.singular_send(host, pickle.dumps(m))

            elif command[0] == "sendall" and len(command) == 3:
                m = Message(self.siteID, command[1], command[2])

                tempHosts = list()
                for _, host in self.hosts.items():
                    tempHosts.append((host['ip_address'], host['udp_end_port']))

                self.messenger.send_all(tempHosts, pickle.dumps(m))

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