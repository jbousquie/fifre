# Classe Message  : objet message entre le client et le dispatcher
import uuid

class Message:

    def __init__(self, username, transport, date, domain, content):
        self.username = username
        self.transport = transport
        self.date = date
        self.domain = domain
        self.content = content
        self.msgId = self.generate_unique_id()

    # generate an unique random string
    def generate_unique_id(self):
        id = str(uuid.uuid4())
        return id
