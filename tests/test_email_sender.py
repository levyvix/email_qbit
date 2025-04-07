import pytest
import os
from unittest.mock import patch, MagicMock
from main import QBittorrentEmailSender
from email.message import EmailMessage
import smtplib
import ssl


@pytest.fixture
def mock_env_vars():
    with patch.dict(
        os.environ,
        {"SENDER": "test@example.com", "PASSWORD": "test_password", "RECEIVER": "receiver@example.com"},
        clear=True,
    ):
        yield


@pytest.fixture
def email_sender(mock_env_vars):
    return QBittorrentEmailSender()


def test_init_missing_env_vars():
    with pytest.raises(ValueError) as exc_info:
        QBittorrentEmailSender()
    assert "Missing required environment variables" in str(exc_info.value)


def test_init_missing_sender():
    with patch.dict(os.environ, {"PASSWORD": "test_password", "RECEIVER": "receiver@example.com"}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            QBittorrentEmailSender()
        assert "Missing required environment variables" in str(exc_info.value)


def test_init_missing_password():
    with patch.dict(os.environ, {"SENDER": "test@example.com", "RECEIVER": "receiver@example.com"}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            QBittorrentEmailSender()
        assert "Missing required environment variables" in str(exc_info.value)


def test_init_missing_receiver():
    with patch.dict(os.environ, {"SENDER": "test@example.com", "PASSWORD": "test_password"}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            QBittorrentEmailSender()
        assert "Missing required environment variables" in str(exc_info.value)


def test_send_email_success(email_sender):
    filename = "test_file.txt"

    with patch("smtplib.SMTP_SSL") as mock_smtp:
        # Setup mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        # Call the method
        email_sender.send_email(filename)

        # Verify SMTP was called correctly
        mock_smtp.assert_called_once()
        call_args = mock_smtp.call_args
        assert call_args[0][0] == "smtp.gmail.com"
        assert call_args[0][1] == 465
        assert isinstance(call_args[1]["context"], ssl.SSLContext)

        mock_server.login.assert_called_once_with("test@example.com", "test_password")
        mock_server.send_message.assert_called_once()

        # Verify email content
        sent_message = mock_server.send_message.call_args[0][0]
        assert isinstance(sent_message, EmailMessage)
        assert sent_message["Subject"] == f"Download completed: {filename}"
        assert sent_message["From"] == "test@example.com"
        assert sent_message["To"] == "receiver@example.com"


def test_send_email_authentication_error(email_sender):
    filename = "test_file.txt"

    with patch("smtplib.SMTP_SSL") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, "Authentication failed")

        with pytest.raises(smtplib.SMTPAuthenticationError):
            email_sender.send_email(filename)


def test_send_email_smtp_error(email_sender):
    filename = "test_file.txt"

    with patch("smtplib.SMTP_SSL") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        mock_server.send_message.side_effect = smtplib.SMTPException("SMTP error occurred")

        with pytest.raises(smtplib.SMTPException):
            email_sender.send_email(filename)


def test_send_email_unexpected_error(email_sender):
    filename = "test_file.txt"

    with patch("smtplib.SMTP_SSL") as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        mock_server.send_message.side_effect = Exception("Unexpected error")

        with pytest.raises(Exception):
            email_sender.send_email(filename)
