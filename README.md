# Send email after a download finishes in QBitTorrent

This project automatically sends an email notification when a torrent download completes in QBitTorrent. It's particularly useful for monitoring long-running downloads or when you're away from your computer.

## Features

- Automatic email notifications when torrent downloads complete
- Customizable email content with download details
- Secure email sending using Gmail's SMTP server
- Simple setup and configuration
- Environment-based configuration for better security
- Detailed logging for monitoring and debugging
- Object-oriented design for better maintainability

## Prerequisites

- Python 3.9 or higher
- UV (Python package manager) - [Installation Guide](https://github.com/astral-sh/uv)
- QBitTorrent
- A Gmail account with App Password enabled

## Setup

1. Clone this repository to your local machine
2. Install UV if you haven't already:
   ```bash
   pip install uv
   ```
3. Create virtual environment and install dependencies in one step:
   ```bash
   uv sync
   ```
4. Create your environment configuration:
   ```bash
   cp .env.example .env
   ```
5. Edit the `.env` file with your credentials:
   ```env
   SENDER = "your_email@gmail.com"
   PASSWORD = "your_app_password"
   RECEIVER = "recipient_email@example.com"
   ```

## Configuration

In QBitTorrent:
1. Go to Tools > Options > Downloads
2. Under "Run external program on torrent completion", enter the following command:
   ```
   C:\path\to\your\project\.venv\Scripts\python.ex C:\path\to\your\project\main.py "%N"
   ```
   Replace:
   - `C:\path\to\your\project` with the actual path where you cloned the repository
   - `%N` is a QBitTorrent variable that passes the torrent name

For example, if you cloned the repository to `C:\Users\YourUsername\Desktop\email_qbit`, the command would be:
```
C:\Users\YourUsername\Desktop\email_qbit\.venv\Scripts\python.exe C:\Users\YourUsername\Desktop\email_qbit\main.py "%N"
```

## Project Structure

The project is organized in an object-oriented manner:

- `QBittorrentEmailSender` class: Handles all email-related functionality
  - Constructor loads environment variables
  - `send_email()` method sends the notification
  - Includes logging for monitoring and debugging

## Logging

The application includes detailed logging that will help you monitor and debug:
- Logs when an email is being sent
- Logs the recipient and subject of each email
- Confirms successful email delivery
- Logs any errors that might occur during the process

## Security Note

- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore` to prevent accidental commits
- Make sure to enable 2FA on your Gmail account before generating an App Password
- Keep your `.env` file secure and don't share it with others

## How It Works

1. When a torrent download completes, QBitTorrent executes the Python script
2. The script receives the torrent name as a command-line argument
3. The `QBittorrentEmailSender` class is instantiated and loads the configuration
4. The `send_email()` method creates and sends the notification email
5. You receive the notification at your specified email address
6. The process is logged for monitoring and debugging

## Troubleshooting

- Make sure your Gmail account has "Less secure app access" enabled or use an App Password
- Verify that the paths in the QBitTorrent configuration are correct
- Check that your firewall isn't blocking the SMTP connection
- Ensure your Gmail account has 2FA enabled if using App Passwords
- Verify that your `.env` file is properly configured and in the same directory as `main.py`
- Check the logs for any error messages or issues
- Ensure all environment variables in `.env` are properly set with the correct values
- If you encounter any UV-related issues, try updating UV to the latest version
- If the script doesn't run, verify that both the UV executable and main.py paths are correct

