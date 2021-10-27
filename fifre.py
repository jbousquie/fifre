# Classe Dispatcher

# Le dispatcher récupère les messages des transports/clients, les analyse et les transforme en ordres pour les sous-fifres
from typing import List, Tuple
import importlib
from messageFifre import MessageFifre
from transports.gmailTransport import GmailTransport

from tools import Tools

from pprint import pp as pp


class Dispatcher:

    domains: List = ['winlog', 'refid']   # liste des domaines acceptés en minuscule
    domain_requester_str: str = '???'    # string de requête de la liste des domaines

    # constructeur
    def __init__(self, fifre):
        # liste des sous-fifres connus du dispatcher
        self.fifre: Fifre = fifre
        self.ssfifres: List = []
        self.domains = ['winlog', 'proxmox']


    # Gestion des messages depuis et vers les clients
    # -----------------------------------------------

    # accepte un objet message venant du client et teste immédiatement le domaine demandé. Domaine écrit comme sujet du message
    def accept_message(self, msgObj: MessageFifre) -> None:
        requested_domain: str = (msgObj.subject).lower()
        # si demande de la liste des domaines
        if requested_domain == Dispatcher.domain_requester_str:
            msg_text: str = 'Domaines possibles :\n'
            for dom in Dispatcher.domains:
                msg_text: str = msg_text + dom + '\n'
            self.report_to_client(msg_text)
        # si domaine demandé dans la liste des domaines
        elif requested_domain in Dispatcher.domains:
            self.parse_content(msgObj)
        else:
            msg_text: str = 'Domaine demandé "' + requested_domain + '" non connu'
            self.report_to_client(msg_text)
        return

    # analyse un objet message : extraction des commandes
    # renvoie un message de compte-rendu à retourner au client
    def parse_content(self, msgObj: MessageFifre) -> MessageFifre:
        sender = self.fifre.username
        transport = msgObj.transport
        recipient = msgObj.username
        content = msgObj.content
        domain = (msgObj.subject).lower()

        orders_str = content.split('\n')
        if len(orders_str) > 0:

            # Création du sous-fifre spécialisé dans le domaine
            ssfifre = SousFifre(self, domain)
            for order_str in orders_str:
                if len(order_str) > 0 :
                    order = Order(msgObj, order_str)
                    if ssfifre.parse_order(order):
                        ssfifre.execute_order(order)

        # Message de réponse éventuel ?
        responseDate = Tools.stringNow()    
        msgId = Tools.generate_unique_id()
        msgText = "voici ma réponse"
        msgResponse = MessageFifre(sender, transport, recipient, responseDate, domain, msgText, msgId)
        return msgResponse

    # accuse réception auprès du client du message transmis
    def acknowledge_message(self, msgObj: MessageFifre) -> None:
        return
    
    # envoie un message de rapport au client
    def report_to_client(self, msgObj: MessageFifre) -> None:
        return


# Classe Order
# ordre unique transmis du dispatcher au sous-fifre
class Order:
    def __init__(self, command: MessageFifre, orderStr: str) -> None:
        self.command = command
        self.orderStr = orderStr



# Classe Sous-Fifre
# Le sous-fifre va importer le script dédié à la communication vers le service distant
# et lancer son exécution asynchrone
class SousFifre:

    ssfifres_path = 'ssfifres.'

    def __init__(self, dispatcher: Dispatcher, domain: str):
        self.dispatcher: Dispatcher = dispatcher
        self.domain: str = domain
        module_name = 'ssfifres.' + domain
        self.imported_module = importlib.import_module(module_name)
        self.specialized = self.imported_module.Specialized()
        return

    def parse_order(self, order: Order) -> Tuple[bool, str]:
        order_str = order.orderStr
        parsed, msg = self.specialized.parse_order(order_str)
        return parsed, msg


    def execute_order(self, order: Order) -> None:
        order_str = order.orderStr
        executed = self.specialized.execute_order(order_str)
        return
    
    def report_dispatcher(self) -> None:
        return







# Classe Fifre
# gère l'execution des transports 
class Fifre:
    
    username = 'fifre@iut-rodez.fr'

    # constructeur
    def __init__(self) -> None:
        # récupérer et traiter en premier lieu les retours des sous-fifres ?

        self.dispatcher: Dispatcher = Dispatcher(self)
        gmt: GmailTransport = GmailTransport(self.dispatcher)
        gmt.getMails()


# TEST
fifre = Fifre()