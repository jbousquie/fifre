# Classe Dispatcher

# Le dispatcher récupère les messages des transports/clients, les analyse et les transforme en ordres pour les sous-fifres
from typing import List
from messageFifre import MessageFifre

class Dispatcher:

    domains: List = ['winlog', 'refid']   # liste des domaines acceptés en minuscule
    domain_requester_str: str = '???'    # string de requête de la liste des domaines

    # constructeur
    def __init__(self):
        # liste des sous-fifres connus du dispatcher
        self.ssfifres: List = []



    # Gestion des messages depuis et vers les clients
    # -----------------------------------------------

    # accepte un objet message venant du client et teste immédiatement le domaine demandé. Domaine écrit comme sujet du message
    def accept_message(self, msgObj: MessageFifre) -> None:
        requested_domain: str = msgObj.subject.lower()
        # si demande de la liste des domaines
        if requested_domain == Dispatcher.domain_requester_str:
            msg_text: str = 'Domaines possibles :\n'
            for dom in Dispatcher.domains:
                msg_text: str = msg_text + dom + '\n'
            self.report_to_client(msg_text)
        # si domaine demandé dans la liste des domaines
        elif requested_domain in Dispatcher.domains:
            self.parse_message(msgObj)
        else:
            msg_text: str = 'Domaine demandé "' + requested_domain + '" non connu'
            self.report_to_client(msg_text)
        return

    # analyse un objet message : extraction des commandes
    def parse_message(self, msgObj: MessageFifre) -> None:
        print(msgObj.content)
        return

    # accuse réception auprès du client du message transmis
    def acknowledge_message(self, msgObj: MessageFifre) -> None:
        return
    
    # envoie un message de rapport au client
    def report_to_client(self, msgText: str) -> None:
        return


    # Gestion des sous-fifres
    # -----------------------


    # enregistre les sous-fifres connus dans la liste
    def enroll_ssFifres(self) -> None:
        return

    # ordres donnés au sous-fifre
    def order(self) -> None:
        return

    # sauve un ordre dans la liste des ordres transmis au sous-fifre
    def store_order(self) -> None:
        return

    # retire un ordre sauvé de la liste des ordres transmis
    def remove_order(self) -> None:
        return
    

    

