import smtplib, ssl
import sys
from email.message import EmailMessage

# Dados do Gmail
remetente = "qbittorrent9@gmail.com"
senha_app = "apmz fqha iqrj juav"  # <-- Substitua pela sua senha de app
destinatario = "levy.vix@gmail.com"

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
