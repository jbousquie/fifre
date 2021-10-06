# Mail Transport : IMAP
# uses IMAPCLient : pip install imapClient
# https://imapclient.readthedocs.io/en/2.2.0/api.html

# Le transport Gmail récupère les mails non lus  (IMAP) et en fait autant de messages à destination du dispatcheur
# Un message est un ensemble de commandes écrites dans le corps du mail, chaque ligne précédée d'un caractère d'identification (ex "!")
# Le domaine sur lequel passer ces commandes doit être mentionné dans le sujet du mail

from pprint import pp as pp
import email
from message import Message

IMAP_HOST = "imap.gmail.com"
IMAP_USER = 'fifre@iut-rodez.fr'
IMAP_PWD = 'Fifre789'

AUTHORIZED = [
    'andre.lasfargues@iut-rodez.fr', 'sylvain.delpech@iut-rodez.fr', 'jerome.bousquie@iut-rodez.fr', 
    'jerome.bousquie@ut-capitole.fr', 'jerome@bousquie.fr'
    ]
#AUTHORIZED = ['jerome@bousquie.fr']



class GmailTransport:

    transport_name = "gmail"
    response_order_not_found = "Aucun ordre trouvé dans le texte du mail."

    # contructeur
    def __init__(self, dispatcher) -> None:
        self.dispatcher = dispatcher
        pass


    def getMails(self):
        from imapclient import IMAPClient
        with IMAPClient(IMAP_HOST, 993, True, True) as client:
            client.login(IMAP_USER, IMAP_PWD)
            
            select_info = client.select_folder('INBOX')
            print('%d messages in INBOX' % select_info[b'EXISTS'])

            querystring = self.gmail_querystring(AUTHORIZED)
            messages = client.gmail_search(querystring, charset='UTF-8')
          
            # https://stackoverflow.com/questions/52425681/get-content-of-a-mail-imapclient
            # https://stackoverflow.com/questions/24075732/read-body-of-email-using-imapclient-in-python
            # https://www.timpoulsen.com/2018/reading-email-with-python.html
            # https://docs.python.org/fr/3/library/email.compat32-message.html
            for mail_id, data in client.fetch(messages, ['ENVELOPE', 'BODY[TEXT]']).items():

                envelope = data[b'ENVELOPE']
                raw_body = email.message_from_bytes(data[b'BODY[TEXT]'])

                pp('inbox mail number : ' + str(mail_id))
                msg_date = envelope[0].isoformat()
                subject = envelope[1].decode("utf-8")
                tuple_from = envelope[2][0]
                sender = tuple_from[2].decode("utf-8")
                host = tuple_from[3].decode("utf-8")
                msg_id = envelope[9].decode("utf-8")

                
                # traitement du corps du message 
                charset = "utf-8"
                if raw_body.is_multipart():
                    for part in raw_body.walk():
                        content_type = part.get_content_type()
                        if content_type == 'text/plain':
                            text_content = part
                            
                else:
                    text_content = raw_body
                    
                parsed_body = text_content.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                lines = parsed_body.split('\n')
                msg_content = ''
                any_order = False
                username = sender + "@" + host
                for line in lines:
                    stripped = line.strip()
                    if stripped[0:2] == '!!':
                        any_order = True
                        msg_content = msg_content + stripped[2:].lstrip() + '\n'

                if any_order:
                    dispatcher_msg = Message(username, GmailTransport.transport_name, msg_date, subject, msg_content, msg_id)
                    self.dispatcher.parse_message(dispatcher_msg)

                else:
                    self.instant_response(GmailTransport.response_order_not_found)


            # marque les messages comme non lus pour le test suivant
            client.remove_flags(messages, '\Seen')



    # Renvoie une querystring gmail de sélection des messages non lus des émetteurs autorisés uniquement
    def gmail_querystring(self, auth_list):
        first = True
        sep = ''
        qs = 'in:unread from:'
        for auth in auth_list:
            qs = qs + sep + auth
            if first:
                sep = '|'
                first = False
        return qs

    # Envoie directement un mail au client pour le notifier du message passé en paramètre
    def instant_response(self, resp_msg):
        # SMTP
        pass


