import smtplib
from smtplib import SMTPServerDisconnected
from email.message import EmailMessage
import mimetypes
import os
import logging


class MailClient(object):
    """
    Example mail client using SMTPlib
    Uses config
    """
    def __init__(self, config=None, logger=None):
        self.mailserver = None
        self.logger = logger if logger else logging.getLogger("MailClient")
        self.C = config
        self.fromaddr = self.C["mail.connection.user"]
        self.connect()

    def connect(self):
        self.mailserver = smtplib.SMTP(self.C["mail.connection.host"], self.C["mail.connection.port"])
        self.mailserver.ehlo()
        self.mailserver.starttls()
        self.mailserver.login(self.fromaddr, self.C["mail.connection.passwd"])
        self.logger.info("self.Connected successfully to mail server.")

    @staticmethod
    def add_attachment(msg, fpath):
        """
        Liberated from docs
        """
        ctype, encoding = mimetypes.guess_type(fpath)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        with open(fpath, "rb") as f:
            msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=os.path.basename(fpath))

    def compose_mail(self, title, body, attachments=None, to=None):
        msg = EmailMessage()
        msg.set_content(body)
        msg["To"] = to if to else ", ".join(self.C["mail.recipients"])
        msg["From"] = self.fromaddr
        msg["Subject"] = title
        if attachments:
            if not isinstance(attachments, list):
                attachments = [attachments]
            self.logger.info("Found {} attachment. Processing".format(len(attachments)))
            for attachment in attachments:
                self.logger.info("Attaching \"{}\"".format(attachment))
                self.add_attachment(msg, attachment)
                self.logger.debug("Attached \"{}\"".format(attachment))
        return msg

    def send(self, msg):
        try:
            self.mailserver.send_message(msg)
            self.logger.info("Mail sent to the {} recipients".format(len(self.C["mail.recipients"])))
        except SMTPServerDisconnected:
            self.logger.warning("Mail server disconnected. Reconnecting.")
            self.connect()
            self.send(msg)


if __name__ == '__main__':
    from src.config.config import Config

    c = Config("mail.yaml")
    m = MailClient(config=c)
    mail = m.compose_mail("test mail",
                          "this is a test mail. \n Please ignore the content",
                          attachments=["attachments/1.txt", "attachments/2.txt"])

    m.send(mail)
