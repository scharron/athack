from smtplib import SMTP
from email.mime.text import MIMEText


class _:
    def __init__(self, address, sender=None):
        self.recipient = address
        self.sender = sender

    def __rshift__(self, other_address):
        return _(other_address.recipient, self.recipient)

    def __getattr__(self, other):
        return _(self.recipient + "." + other, self.sender)

    def __sub__(self, other):
        return _(self.recipient + "-" + other.recipient, self.sender)

    def __matmul__(self, other):
        return _(self.recipient + "@" + other.recipient, self.sender)

    def mime(self, content="", subject=None):
        message = MIMEText(content)
        if subject:
            message["Subject"] = subject

        message["From"] = self.sender
        message["To"] = self.recipient

        return message

    def send(self, content, subject=None):
        message = self.mime(content, subject)

        print(message)

        with SMTP("localhost") as smtp:
            smtp.send_message(message)

    def __or__(self, arg):
        if isinstance(arg, dict):
            for subject, content in arg.items():
                self.send(content, subject)
                return self

        return self

    def __str__(self):
        return str(self.mime())

    def __repr__(self):
        return repr(self.mime())


samuel, data, publica, c, radar = _("samuel"), _("data"), _("publica"), _("c"), _("radar")


samuel.charron@c-radar.com >> samuel.charron@data-publica.com | {
    "Sujet":
    "Ca marche ?"
}


# You may need to hack the code to make it work with gmail and other mail providers:
#        with SMTP("smtp.gmail.com:587") as smtp:
#            smtp.starttls()
#            smtp.login(self.sender, "XXX")
