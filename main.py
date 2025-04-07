import smtplib, ssl
import sys
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# Dados do Gmail
remetente = os.getenv("SENDER")
senha_app = os.getenv("PASSWORD")
destinatario = os.getenv("RECEIVER")

# Informações passadas pelo qBittorrent
nome_arquivo = sys.argv[1] if len(sys.argv) > 1 else "Arquivo desconhecido"

# Montar o e-mail
mensagem = EmailMessage()
mensagem["Subject"] = f"Download concluído: {nome_arquivo}"
mensagem["From"] = remetente
mensagem["To"] = destinatario
mensagem.set_content(f"O download do torrent '{nome_arquivo}' foi concluído com sucesso.")

# Enviar o e-mail
contexto = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
    servidor.login(remetente, senha_app)
    servidor.send_message(mensagem)
