import socket
import pickle
import threading
import sys
from message import Message

class Messenger:

    def __init__(self, host, hosts, siteID):
        self.send_address = (host['ip_address'], host['udp_start_port'])
        self.recv_address = (host['ip_address'], host['udp_end_port'])

        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.send_sock.bind(self.send_address)
        self.recv_sock.bind(self.recv_address)

        self.listeners = list()
        self.hosts = hosts
        self.siteID = siteID

        threading.Thread(target = self.listen).start()

    def addListener(self, listener):
        self.listeners.append(listener)

    def sendMessage(self, host, message=b"Hello, world"):
        ''' Send a message to another host '''
        self.send_sock.sendto(pickle.dumps(message), host)

    def send(self, destination, messageType, contents, slot):
        message = Message(self.siteID, destination, messageType, contents, slot)
        host = (self.hosts[destination]['ip_address'], self.hosts[destination]['udp_end_port'])
        print("sending %s %s to %s" % (message.messageType, message.contents, destination), file=sys.stderr)
        threading.Thread(target = self.sendMessage, args = (host, message)).start()

    #sendAll(self, messageType, contents, slot):
    def sendAll(self, messageType, contents, slot): 
        ''' Send a message a list of host concurrently '''
        threads = list()
        for key, host in self.hosts.items():
            message = Message(self.siteID, key, messageType, contents, slot)
            print("sending %s %s to all sites" % (message.messageType, message.contents), file=sys.stderr)
            t = threading.Thread(target = self.sendMessage, args = ((host['ip_address'], host['udp_end_port']), message))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()

    def listen(self):
        threads = list()
        while True:
            data, _ = self.recv_sock.recvfrom(1024)
            message = pickle.loads(data)

            t = threading.Thread(target = self.receive, args = (message,))
            threads.append(t)
            t.start()

    def receive(self, message):
        #print("SiteId", message.origin)
        #print("Message_Type", message.messageType)
        #print("Content", message.contents)
        print("received %s %s from %s" % (message.messageType, message.contents, message.origin), file=sys.stderr)
        for listener in self.listeners:
            listener.receive(message) 
