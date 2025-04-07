import smtplib
import ssl
import sys
import os
from email.message import EmailMessage
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QBittorrentEmailSender:
    def __init__(self):
        load_dotenv()
        self.remetente = os.getenv("SENDER")
        self.senha_app = os.getenv("PASSWORD")
        self.destinatario = os.getenv("RECEIVER")

    def send_email(self, nome_arquivo: str) -> None:
        mensagem = EmailMessage()
        mensagem["Subject"] = f"Download concluído: {nome_arquivo}"
        mensagem["From"] = self.remetente
        mensagem["To"] = self.destinatario
        logger.info(
            f"Enviando e-mail para {self.destinatario} com o assunto: {mensagem['Subject']}"
        )
        mensagem.set_content(
            f"O download do torrent '{nome_arquivo}' foi concluído com sucesso."
        )

        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as servidor:
            servidor.login(self.remetente, self.senha_app)
            servidor.send_message(mensagem)
            logger.info(f"E-mail enviado com sucesso para {self.destinatario}")


if __name__ == "__main__":
    sender = QBittorrentEmailSender()
    if len(sys.argv) > 1:
        sender.send_email(sys.argv[1])
    else:
        print("Nenhum arquivo fornecido")
