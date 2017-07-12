from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import base64

fromaddr = "trivneel211@gmail.com"
toaddr = "trivneel211@gmail.com"

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Test email using Python"
body = "This is a test of using Python to send email"
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)  # I'm pretty sure 587 is the port?
server.ehlo()
server.starttls()
server.ehlo()
server.login("trivneel211", base64.b64decode("aW50ZWxpNTEx"))  # i think this is pointless tbh but whatever

text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)



