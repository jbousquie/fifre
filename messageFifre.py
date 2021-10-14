# Classe Message  : objet message entre le client et le dispatcher
import typing
import uuid
import json
from datetime import datetime

class MessageFifre:

    def __init__(self, username, transport, to, msgDate, subject, content, transportMsgId):
        now = datetime.now()
        self.username: str = username
        self.transport: str = transport
        self.to: str = to
        self.msgDate: str = msgDate                          # date du mail
        self.subject: str = subject
        self.content: str = content
        self.transportMsgId: str = transportMsgId            # Id d'origine provenant du transport s'il existe
        self.msgId: str = self.generate_unique_id()          # Id interne à l'application
        self.creationDate = now.strftime('%Y-%m-%d %H:%M:%S')

    # generate an unique random string
    def generate_unique_id(self) -> None:
        id: str = str(uuid.uuid4())
        return id

    def store(self) -> None:
        pass

    # Renvoie une string JSON de l'objet message
    def to_json(self) -> str:
        serialized: str = json.dumps(self.__dict__)
        return serialized
