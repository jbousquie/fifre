# Mail Transport : IMAP
# uses IMAPCLient : pip install imapClient
# https://imapclient.readthedocs.io/en/2.2.0/api.html

# Le transport Gmail récupère les mails non lus  (IMAP) et en fait autant de messages à destination du dispatcheur
# Un message est un ensemble de commandes écrites dans le corps du mail, chaque ligne précédée d'un caractère d'identification (ex "!")
# Le domaine sur lequel passer ces commandes doit être mentionné dans le sujet du mail
from typing import Dict, List, Tuple

import email
from email.header import Header
from email.mime.text import MIMEText
from email.message import Message

from imapclient.response_types import SearchIds
from imapclient import IMAPClient
from smtplib import SMTP_SSL
import ssl
from datetime import datetime

from dispatcher import Dispatcher
from messageFifre import MessageFifre
from tools import Tools


from pprint import pp as pp



IMAP_HOST = "imap.gmail.com"
IMAP_USER = 'fifre@iut-rodez.fr'
IMAP_PWD = 'Fifre789'

SMTP_HOST = 'smtp.gmail.com'
SMTP_TLSSSL_PORT = 465
SMTP_USER = IMAP_USER
SMTP_PWD = IMAP_PWD

AUTHORIZED = [
    'andre.lasfargues@iut-rodez.fr', 'sylvain.delpech@iut-rodez.fr', 'jerome.bousquie@iut-rodez.fr', 
    'jerome.bousquie@ut-capitole.fr', 'jerome@bousquie.fr'
    ]
#AUTHORIZED = ['jerome@bousquie.fr']



class GmailTransport:

    transport_name = "gmail"
    response_order_not_found = "Aucun ordre trouvé dans le texte du mail."
    log_file = "./transports/gmailTransport.log"
    utf8str: str = 'utf-8'



    # contructeur
    def __init__(self, dispatcher) -> None:
        self.dispatcher: Dispatcher = dispatcher
        pass


    def getMails(self) -> None:
        
        with IMAPClient(IMAP_HOST, 993, True, True) as client:
            client.login(IMAP_USER, IMAP_PWD)
            
            select_info: Dict = client.select_folder('INBOX')
            print('%d messages in INBOX' % select_info[b'EXISTS'])

            charset: str = GmailTransport.utf8str
            querystring: str = self.gmail_querystring(AUTHORIZED)
            messages: SearchIds = client.gmail_search(querystring, charset=charset)
          
            # https://stackoverflow.com/questions/52425681/get-content-of-a-mail-imapclient
            # https://stackoverflow.com/questions/24075732/read-body-of-email-using-imapclient-in-python
            # https://www.timpoulsen.com/2018/reading-email-with-python.html
            # https://docs.python.org/fr/3/library/email.compat32-message.html

            for mail_id, data in client.fetch(messages, ['ENVELOPE', 'BODY[TEXT]']).items():

                envelope = data[b'ENVELOPE']
                raw_body: Message = email.message_from_bytes(data[b'BODY[TEXT]'])

                pp('inbox mail number : ' + str(mail_id))
                msg_date = envelope[0].isoformat()
                subject: str = envelope[1].decode(charset)
                tuple_from: Tuple = envelope[2][0]
                sender: str = tuple_from[2].decode(charset)
                host: str = tuple_from[3].decode(charset)
                msg_id: str = envelope[9].decode(charset)

                
                # traitement du corps du message 
                if raw_body.is_multipart():
                    for part in raw_body.walk():
                        content_type: str = part.get_content_type()
                        if content_type == 'text/plain':
                            text_content: str = part
                            
                else:
                    text_content: str = raw_body
                    
                parsed_body: str = text_content.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                lines = parsed_body.split('\n')
                msg_content: str = ''
                any_order: bool = False
                username: str = sender + "@" + host
                for line in lines:
                    stripped: str = line.strip()
                    if stripped[0:2] == '!!':
                        any_order: bool = True
                        msg_content: str = msg_content + stripped[2:].lstrip() + '\n'

                if any_order:
                    dispatcher_msg:  MessageFifre = MessageFifre(username, GmailTransport.transport_name, IMAP_USER, msg_date, subject, msg_content, msg_id)
                    self.log(dispatcher_msg.to_json())
                    self.dispatcher.accept_message(dispatcher_msg)

                else:
                    self.instant_response(GmailTransport.response_order_not_found)


            # marque les messages comme non lus pour le test suivant
            client.remove_flags(messages, '\Seen')
            #snd_date: str = Tools.stringNow()
            #snd_msg: MessageFifre = MessageFifre(SMTP_USER, GmailTransport.transport_name, username, snd_date, 'Réponse de Fifre', msg_content, 'zzzzz')
            #self.sendMail(snd_msg)



    # Renvoie une querystring gmail de sélection des messages non lus des émetteurs autorisés uniquement
    def gmail_querystring(self, auth_list: List) -> str:
        first: bool = True
        sep: str = ''
        qs: str = 'in:unread from:'
        for auth in auth_list:
            qs = qs + sep + auth
            if first:
                sep = '|'
                first = False
        return qs

    # Envoie directement un mail au client pour le notifier du message passé en paramètre
    # Ou mettre ça côté dispatcher ..?
    def instant_response(self, resp_msg: str) -> None:
        # SMTP
        pass

    # Logue le message dans le fichier de log
    def log(self, msgJson) -> None:
        with open(GmailTransport.log_file, 'a') as log_file:
            line: str = msgJson + '\n'
            log_file.write(line)

    def sendMail(self, msgObj: MessageFifre) -> None:
        msg: MIMEText = MIMEText(msgObj.content)
        msg['Subject'] = Header(msgObj.subject, GmailTransport.utf8str)
        msg['From'] = msgObj.username
        msg['To'] = msgObj.to

        ssl_context: ssl.SSLContext = ssl.create_default_context()
        server: SMTP_SSL = SMTP_SSL(SMTP_HOST, SMTP_TLSSSL_PORT, context=ssl_context)
        server.ehlo_or_helo_if_needed()
        server.login(SMTP_USER, SMTP_PWD)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()

