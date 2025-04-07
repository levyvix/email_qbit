# Send email after a download finishes in QBitTorrent

This project automatically sends an email notification when a torrent download completes in QBitTorrent. It's particularly useful for monitoring long-running downloads or when you're away from your computer.

## Features

- Automatic email notifications when torrent downloads complete
- Customizable email content with download details
- Secure email sending using Gmail's SMTP server
- Simple setup and configuration
- Environment-based configuration for better security

## Prerequisites

- Python 3.x
- QBitTorrent
- A Gmail account with App Password enabled

## Setup

1. Clone this repository to your local machine
2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -e .
   ```
4. Create your environment configuration:
   ```bash
   cp .env.example .env
   ```
5. Edit the `.env` file with your credentials:
   - `SENDER`: Your Gmail address
   - `PASSWORD`: Your Gmail App Password
   - `RECEIVER`: The email address where you want to receive notifications

## Configuration

1. Open `main.py` and modify the following variables:
   - `remetente`: Your Gmail address
   - `senha_app`: Your Gmail App Password
   - `destinatario`: The email address where you want to receive notifications

2. In QBitTorrent:
   - Go to Tools > Options > Downloads
   - Under "Run external program on torrent completion", enter:
     ```
     python path\to\main.py "%N"
     ```
   - Replace `path\to\main.py` with the actual path to your `main.py` file
   - `%N` is a QBitTorrent variable that passes the torrent name

## Security Note

- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore` to prevent accidental commits
- Make sure to enable 2FA on your Gmail account before generating an App Password
- Keep your `.env` file secure and don't share it with others

## How It Works

1. When a torrent download completes, QBitTorrent executes the Python script
2. The script receives the torrent name as a command-line argument
3. It creates an email with the download completion notification
4. The email is sent using Gmail's SMTP server
5. You receive the notification at your specified email address

## Troubleshooting

- Make sure your Gmail account has "Less secure app access" enabled or use an App Password
- Verify that the Python path in QBitTorrent is correct
- Check that your firewall isn't blocking the SMTP connection
- Ensure your Gmail account has 2FA enabled if using App Passwords
- Verify that your `.env` file is properly configured and in the same directory as `main.py`

