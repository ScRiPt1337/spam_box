import os
import email

class Email:
    def __init__(self):
        self.from_email = ""
        self.date = ""
        self.subject = ""
        self.to = ""
        self.content = ""


class Mail:

    @staticmethod
    def formate_email(data):
        formated_email = Email()
        msg = email.message_from_string(data)
        formated_email.from_email = msg['from']
        formated_email.date = msg["date"]
        formated_email.subject = msg["subject"]
        formated_email.to = msg["to"]
        for payload in msg.get_payload():
            formated_email.content += payload.get_payload()
        return formated_email
