class Message:

    def __init__(self, origin, destination, messageType, contents, slot):
        self.origin = origin 
        self.destination = destination
        self.messageType = messageType 
        self.contents = contents
        self.slot = slot

    def __str__(self):
        return self.content + '\n' + self.message_type + '\n' + self.origin + '\n'