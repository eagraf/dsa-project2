import socket
import pickle
import threading
from message import Message

class Messenger:

    def __init__(self, host, hosts, siteID):
        self.send_address = (host['ip_address'], host['udp_start_port'])
        self.recv_address = (host['ip_address'], host['udp_end_port'])

        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.send_sock.bind(self.send_address)
        self.recv_sock.bind(self.recv_address)

        self.listeners = dict()
        self.hosts = hosts
        self.siteID = siteID

        threading.Thread(target = self.listen).start()

    def add_listener(self, listener):
        temp = type(listener)
        temp = temp.strip('<').strip('>')
        temp = temp.split(" ")
        temp = temp[1].strip("'")
        temp = temp.split(".")
        print("Listener Type", temp[1])
        self.listeners[temp[1]] = listener

    def sendMessage(self, host, message=b"Hello, world"):
        ''' Send a message to another host '''
        self.send_sock.sendto(pickle.dumps(message), host)

    def send(self, destination, messageType, contents, slot):
        message = Message(self.siteID, destination, messageType, contents, slot)
        host = (self.hosts[destination]['ip_address'], self.hosts[destination]['udp_end_port'])
        threading.Thread(target = self.sendMessage, args = (host, message)).start()

    #sendAll(self, messageType, contents, slot):
    def sendAll(self, messageType, contents, slot): 
        ''' Send a message a list of host concurrently '''
        threads = list()
        for key, host in self.hosts.items():
            message = Message(self.siteID, key, messageType, contents, slot)
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
        print("SiteId", message.origin)
        print("Message_Type", message.messageType)
        print("Content", message.contents)
        if message.messageType == "Promise":
            print("Call Proposer Receive")
            #listeners["Proposer"].receive(message.siteID, message.message_type, message.content)
        elif message.messageType == "Prepare" or message.messageType == "Accept":
            print("Call Acceptor Receive")
            #listeners["Acceptor"].receive(message.siteID, message.message_type, message.content)
        elif message.messageType == "Commit":
            print("Call Listener Receive")
            #listeners["Listener"].receive(message.siteID, message.message_type, message.content)