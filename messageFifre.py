# Classe Message  : objet message entre le client et le dispatcher
import json
from tools import Tools

class MessageFifre:

    def __init__(self, username, transport, to, msgDate, subject, content, transportMsgId):
        self.username: str = username
        self.transport: str = transport
        self.to: str = to
        self.msgDate: str = msgDate                          # date du message
        self.subject: str = subject
        self.content: str = content
        self.transportMsgId: str = transportMsgId            # Id du message d'origine provenant du transport s'il existe
        self.msgId: str = Tools.generate_unique_id()          # Id du message interne à l'application
        self.creationDate = Tools.stringNow()

    def store(self) -> None:
        pass

    # Renvoie une string JSON de l'objet message
    def to_json(self) -> str:
        serialized: str = json.dumps(self.__dict__)
        return serialized
