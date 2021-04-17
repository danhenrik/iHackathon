from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from env import SMTP_EMAIL, SMTP_PASSWORD
 
def send_mail(message):

  msg = MIMEMultipart()
  
  # setup the parameters of the message
  password = SMTP_PASSWORD
  msg['From'] = SMTP_EMAIL
  msg['To'] = SMTP_EMAIL
  msg['Subject'] = "Sugestão"
  
  # add in the message body
  msg.attach(MIMEText(message, 'plain'))
  
  #create server
  server = smtplib.SMTP('smtp.gmail.com: 587')
  
  server.starttls()
  
  # Login Credentials for sending the mail
  server.login(msg['From'], SMTP_PASSWORD)
  
  
  # send the message via the server.
  server.sendmail(msg['From'], msg['To'], msg.as_string())
  
  server.quit()