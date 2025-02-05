# EggPuff Telegram Bot

EggPuff is a Telegram bot built in Python that offers various system management and utility functions such as fetching IP, managing system services, executing shell commands, saving and retrieving notes, file handling, and more.

## Features

- **System Commands**: 
  - `/get_ip` - Fetch the server's IP address.
  - `/services` - Manage system services (start, stop, restart, status).
  - `/run` - Run custom shell commands on the server.
  - `/system` - Shutdown or reboot the system.
  
- **Notes**:
  - `/takeNote` - Save a quick note.
  - `/getNotes` - Retrieve saved notes.
  
- **File Management**:
  - `/send_file` - Send files from the server.
  - `/list_files` - List files in a specific directory.

- **Help**: 
  - `/help` - Display available commands.
  
## Requirements

- Python 3.7 or above
- `python-dotenv` (for environment variables)
- `python-telegram-bot` (for Telegram bot functionality)

## Installation

### 1. Clone this repository:
```bash
git clone https://github.com/yourusername/eggpuff-telegram-bot.git
cd eggpuff-telegram-bot
```

### 2. Set up Virtualenv:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install required dependencies:
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a .env file in the project directory and add the following:
```bash
TOKEN=your_telegram_bot_token
USERS=user_id_1,user_id_2  # Comma-separated list of authorized user IDs
```