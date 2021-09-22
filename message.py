# Classe Message  : objet message entre le client et le dispatcher
import uuid

class Message:

    def __init__(self, username, transport, date, domain, content):
        self.username = username
        self.transport = transport
        self.date = date
        self.domain = domain
        self.content = content
        self.msgId = self.generateUniqueId()

    # generate an unique random string
    def generateUniqueId(self):
        id = str(uuid.uuid4())
        return id
