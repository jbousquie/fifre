# Classe Message  : objet message entre le client et le dispatcher
import uuid
import json
from datetime import datetime

class MessageFifre:

    def __init__(self, username, transport, to, msgDate, subject, content, transportMsgId):
        now = datetime.now()
        self.username = username
        self.transport = transport
        self.to = to
        self.msgDate = msgDate                          # date du mail
        self.subject = subject
        self.content = content
        self.transportMsgId = transportMsgId            # Id d'origine provenant du transport s'il existe
        self.msgId = self.generate_unique_id()          # Id interne à l'application
        self.creationDate = now.strftime('%Y-%m-%d %H:%M:%S')

    # generate an unique random string
    def generate_unique_id(self):
        id = str(uuid.uuid4())
        return id

    def store(self):
        pass

    # Renvoie une string JSON de l'objet message
    def to_json(self):
        serialized = json.dumps(self.__dict__)
        return serialized
