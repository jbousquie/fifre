# Classe Message

class Message:

    def __init__(self, username, transport, date, domain, content):
        self.username = username
        self.transport = transport
        self.date = date
        self.domain = domain
        self.content = content
