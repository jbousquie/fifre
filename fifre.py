# Classe Fifre
# gère l'execution des transports 

from dispatcher import Dispatcher
from transports.gmailTransport import GmailTransport


class Fifre:
    
    # constructeur
    def __init__(self) -> None:
        self.dispatcher: Dispatcher = Dispatcher()
        gmt: GmailTransport = GmailTransport(self.dispatcher)
        gmt.getMails()


# TEST
fifre = Fifre()