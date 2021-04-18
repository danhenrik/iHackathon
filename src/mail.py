from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from env import SMTP_HOST, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD
 
""" Módulo de envio de email's """

# Função de envio de email, recebe o assunto e a mensagem como parâmetros e envia pelo e para o email definido no env
def send_mail(subject, message):

  msg = MIMEMultipart()
  
  # Parâmetros da mensagem
  password = SMTP_PASSWORD
  msg['From'] = SMTP_EMAIL
  msg['To'] = SMTP_EMAIL
  msg['Subject'] = subject
  
  # Corpo da mensagem
  msg.attach(MIMEText(message, 'plain'))
  
  # Inicializando servidor SMTP
  server = smtplib.SMTP(f'{SMTP_HOST}: {SMTP_PORT}')
  
  server.starttls()
  
  # Login do servidor
  server.login(msg['From'], password)
  
  
  # Envio
  server.sendmail(msg['From'], msg['To'], msg.as_string())
  
  server.quit()