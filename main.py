import smtplib
import ssl
import sys
import os
from email.message import EmailMessage
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path

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
            raise ValueError("Missing required environment variables. Please check your .env file.")

    def send_email(self, filename: str) -> None:
        try:
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
                server.login(self.sender, self.app_password)
                server.send_message(message)
                logger.success(f"Email sent successfully for: {filename}")
                
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication Error: {str(e)}")
            raise
        except smtplib.SMTPException as e:
            logger.error(f"SMTP Error while sending email: {str(e)}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error while sending email: {str(e)}")
            raise


if __name__ == "__main__":
    try:
        sender = QBittorrentEmailSender()
        if len(sys.argv) > 1:
            sender.send_email(sys.argv[1])
        else:
            logger.warning("No filename provided as argument")
            print("No file provided")
    except Exception as e:
        logger.exception("Fatal error in main execution")
        sys.exit(1)
