from datetime import datetime
import asyncore
from smtpd import SMTPServer
from Mailbox import Mail
import database
import logging
from json import loads
import os

config = {}
try:
    with open("/opt/hacksec_tempmail/hacksec_tempmail/config.json", "r") as config:
        config = loads(config.read())
except:
    print('No config file found. Please create a config.json file.')
    exit()

database = database.db()
logging.basicConfig(
    filename=config["log_path"],
    level=logging.ERROR,
    format='%(levelname)s:%(asctime)s:%(message)s')


class EmlServer(SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None, rcpt_options=None):
        try:
            Email = Mail.formate_email(data.decode('utf-8'))
            database.insert(Email)
        except Exception as e:
            print(e)


def run():
    # start the smtp server on localhost:1025
    foo = EmlServer(('0.0.0.0', 25), None)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()
