import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Configure loguru
log_path = Path(__file__).parent / "logs"
log_path.mkdir(exist_ok=True)
logger.add(
    log_path / "email_notifications.log",
    rotation="1 day",
    retention="7 days",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)

load_dotenv()


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
            logger.success(f"Email sent successfully for: {filename}")


if __name__ == "__main__":
    sender = QBittorrentEmailSender()
    if len(sys.argv) > 1:
        sender.send_email(sys.argv[1])
    else:
        logger.warning("No filename provided as argument")
