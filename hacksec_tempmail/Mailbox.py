import os


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
        email = Email()
        data = data.split("\n")
        for i in data:
            if i.startswith("From:"):
                email.from_email = i.replace("From:", "")
            elif i.startswith("Date:"):
                email.date = i.replace("Date:", "")
            elif i.startswith("Subject:"):
                email.subject = i.replace("Subject:", "")
            elif i.startswith("To:"):
                email.to = i.replace("To:", "")
            elif i.startswith('<div dir="ltr">'):
                email.content = i
            elif i.startswith('<div dir=3D"ltr">'):
                count = data.index(i)
                for i in data:
                    if len(data) == count:
                        break
                    email.content += data[count]
                    count += 1
        return email
