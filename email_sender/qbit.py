import os
import smtplib
import ssl
from email.message import EmailMessage

from email_sender.logger import logger


class QBittorrentEmailSender:
    def __init__(self):
        self.sender = os.getenv("SENDER")
        self.app_password = os.getenv("PASSWORD")
        self.recipient = os.getenv("RECEIVER")

        if not all([self.sender, self.app_password, self.recipient]):
            raise ValueError(
                "Missing required environment variables. Please check your .env file."
            )

    @logger.catch
    def send_email(self, filename: str) -> None:
        message = EmailMessage()
        message["Subject"] = f"Download completed: {filename}"
        message["From"] = self.sender
        message["To"] = self.recipient

        logger.info(f"Preparing to send email for completed download: {filename}")
        logger.debug(f"From: {self.sender}, To: {self.recipient}")

        message.set_content(
            f"The torrent download '{filename}' has been completed successfully."
        )

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            assert self.sender and self.app_password, "Missing sender or app password"

            server.login(self.sender, self.app_password)
            server.send_message(message)
            logger.success(f"Email sent successfully for: {self.recipient}")
