import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr


class Email:
    def __init__(self, port, server, sender_name, sender_email, to_recipients, cc_recipients):
        self.port = port
        self.server = server
        self.name = sender_name
        self.sender = sender_email
        self.to_recipients = to_recipients
        self.cc_recipients = cc_recipients

    def send_email(self, subject, content):
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8').encode()
        msg['From'] = formataddr((Header(self.name, 'utf-8').encode(), self.sender))
        msg['To'] = ','.join(self.to_recipients)
        msg['Cc'] = ','.join(self.cc_recipients)
        recipients = self.to_recipients + self.cc_recipients
        server = smtplib.SMTP(self.server, self.port)
        server.sendmail(self.sender, recipients, msg.as_string())
        server.quit()
