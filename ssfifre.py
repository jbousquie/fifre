# Classe Sous-Fifre
# Le sous-fifre va importer le script dédié à la communication vers le service distant
# et lancer son exécution asynchrone

from messageFifre import MessageFifre


class SousFifre:

    def __init__(self, dispatcher, domain: str):
        self.dispatcher = dispatcher
        self.domain: str = domain
        return

    # Analyse le message de commande sur le domaine
    # Le découpe en ordres
    # Retourne un message de rapport : erreurs ? etc ?
    def accept_commands(msgObj: MessageFifre) -> MessageFifre:

        msg_report: MessageFifre
        return msg_report


    def execute_order(self) -> None:
        return
    
    def report_dispatcher(self) -> None:
        return
    
