# Classe Fifre

from dispatcher import Dispatcher
from message import Message
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