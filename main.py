import sys

from dotenv import load_dotenv

from email_sender.logger import logger
from email_sender.qbit import QBittorrentEmailSender

load_dotenv()

if __name__ == "__main__":
    sender = QBittorrentEmailSender()
    if len(sys.argv) > 1:
        sender.send_email(sys.argv[1])
    else:
        logger.warning("No filename provided as argument")
