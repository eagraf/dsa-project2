class Message:
    
    def __init__(self, siteID, message_type, cntnt="Hello, world!"):
        self.content = cntnt
        self.message_type = message_type
        self.siteID = siteID

    def __str__(self):
        return self.content + '\n' + self.message_type + '\n' + self.siteID + '\n'