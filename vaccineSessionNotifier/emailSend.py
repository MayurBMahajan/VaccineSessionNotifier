import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendEmail(source,password,response):
    msg = MIMEMultipart()
    msg['From'] = source
    msg['To'] = source
    msg['Subject'] = 'Vaccine Session Found'
    message = response
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP('smtp.gmail.com',587)
    # identify ourselves to smtp gmail client
    mailserver.ehlo()
    # secure our email with tls encryption
    mailserver.starttls()
    # re-identify ourselves as an encrypted connection
    mailserver.ehlo()
    mailserver.login(source, password)
    mailserver.sendmail(source,source,msg.as_string())
    mailserver.quit()