# Classe Fifre
# gère l'execution des transports 

from dispatcher import Dispatcher
from messageFifre import MessageFifre
from order import Order
from ssfifre import SousFifre
from transports.gmailTransport import GmailTransport


class Fifre:
    
    # constructeur
    def __init__(self) -> None:
        self.dispatcher = Dispatcher()
        gmt = GmailTransport(self.dispatcher)
        gmt.getMails()


# TEST
fifre = Fifre()