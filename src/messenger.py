import socket
import pickle
import threading

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

    def send(self, host, message=b"Hello, world"):
        ''' Send a message to another host '''
        self.send_sock.sendto(message, host)

    def singular_send(self, host, message=b"Hello, world"):
        threading.Thread(target = self.send, args = (host,message)).start()


    def send_all(self, hostList, message=b"Hello, world"):
        ''' Send a message a list of host concurrently '''
        threads = list()
        for host in hostList:
            #msg = Message(self.siteID, self.message[0], self.message[1])
            t = threading.Thread(target = self.send, args = (host,message))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()

    def listen(self):
        threads = list()
        while True:
            data, _ = self.recv_sock.recvfrom(1024)
            message = pickle.loads(data)

            t = threading.Thread(target = self.receive, args = (message.siteID, message.message_type, message.content))
            threads.append(t)
            t.start()

    def receive(self, siteID, message_type, content):
        print("SiteId", siteID)
        print("Message_Type", message_type)
        print("Content", content)
        if message_type == "Promise":
            print("Call Proposer Receive")
            #listeners["Proposer"].receive(message.siteID, message.message_type, message.content)
        elif message_type == "Prepare" or message_type == "Accept":
            print("Call Acceptor Receive")
            #listeners["Acceptor"].receive(message.siteID, message.message_type, message.content)
        elif message_type == "Commit":
            print("Call Listener Receive")
            #listeners["Listener"].receive(message.siteID, message.message_type, message.content)