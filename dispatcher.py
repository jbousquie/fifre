# Classe Dispatcher

# Le dispatcher récupère les messages des transports/clients, les analyse et les transforme en ordres pour les sous-fifres


class Dispatcher:

    domains = ['winlog', 'refid']   # liste des domaines acceptés en minuscule
    domain_requester_str = '???'    # string de requête de la liste des domaines

    # constructeur
    def __init__(self):
        # liste des sous-fifres connus du dispatcher
        self.ssfifres = []



    # Gestion des messages depuis et vers les clients
    # -----------------------------------------------

    # accepte un objet message venant du client et teste immédiatement le domaine demandé. Domaine écrit comme sujet du message
    def accept_message(self, msgObj):
        requested_domain = msgObj.subject.lower()
        # si demande de la liste des domaines
        if requested_domain == Dispatcher.domain_requester_str:
            msg_text = 'Domaines possibles :\n'
            for dom in Dispatcher.domains:
                msg_text = msg_text + dom + '\n'
            self.report_to_client(msg_text)
        # si domaine demandé dans la liste des domaines
        elif requested_domain in Dispatcher.domains:
            self.parse_message(msgObj)
        else:
            msg_text = 'Domaine demandé "' + requested_domain + '" non connu'
            self.report_to_client(msg_text)
        return

    # analyse un objet message : extraction des commandes
    def parse_message(self, msgObj):
        print(msgObj.content)
        return

    # accuse réception auprès du client du message transmis
    def acknowledge_message(self, msgObj):
        return
    
    # envoie un message de rapport au client
    def report_to_client(self, msgText):
        return


    # Gestion des sous-fifres
    # -----------------------


    # enregistre les sous-fifres connus dans la liste
    def enroll_ssFifres(self):
        return

    # ordres donnés au sous-fifre
    def order(self):
        return

    # sauve un ordre dans la liste des ordres transmis au sous-fifre
    def store_order(self):
        return

    # retire un ordre sauvé de la liste des ordres transmis
    def remove_order(self):
        return
    

    

