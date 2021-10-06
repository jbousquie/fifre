# Classe Dispatcher

# Le dispatcher récupère les messages des transports/clients, les analyse et les transforme en ordres pour les sous-fifres



class Dispatcher:

    # constructeur
    def __init__(self):
        # liste des sous-fifres connus du dispatcher
        self.ssfifres = []



    # Gestion des messages depuis et vers les clients
    # -----------------------------------------------

    def accept_message(self, msg):
        return

    # analyse un message en provenance du client
    def parse_message(self, msg):
        return

    # accuse réception auprès du client du message transmis
    def acknowledge_message(self, msg):
        return
    
    # envoie un message de rapport au client
    def report_to_client(self):
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
    

    

