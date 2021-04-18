import os
from dotenv import load_dotenv

""" Módulo de configuração do arquivo .env """

# A partir da lib python-dotenv carregamos as variáveis do .env para dentro da aplicação
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
MONGO_DB_URL = os.getenv("MONGO_DB_URL")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")