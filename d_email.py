import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
 
def sendEmail(to, subject, bodymsg):
    fromaddr = "schoomail3@gmail.com"
    toaddr = to
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    
    body = bodymsg
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "hackdis123")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()