import os
import subprocess
import logging

from dotenv import load_dotenv

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, ContextTypes, Application, filters

# load Environment variables
load_dotenv()

# Restricted Commands
restricted_commands = ["rm", "shutdown", "reboot", "delete", "kill", "pkill", "killall"]

# Help message
help_text = str(
    "<b> Bot Commands: </b>\n"
    "/start - Initialize the bot and display a welcome message.\n"
    "/help - Show a list of available commands and their descriptions.\n"
    "/get_ip - Retrieve and display the current IP address of the server.\n"
    "/download - Download a specified file from the server.\n"
    "/system - Used to Reboot are Shutdown the System.\n"
    "/services - List the status of system services and allow managing them.\n"
    "/run - Execute a specified shell command on the server and return the output.\n"
    "/takeNote - Save a quick note for later reference.\n"
    "/getNotes - Retrieve and display all saved notes.\n"
    "/torrent - Download a torrent file from the server.\n"
    "/send_file - send a file.\n"
    "/list_files - list all files in the directory\n"
    )

# Telegram bot token and registered users
TOKEN = os.getenv("TOKEN")
USERS = list(set(map(int, os.getenv("USERS").split(","))))
print(TOKEN, USERS)


# Configure logging
logging.basicConfig(filename='logs/bot.log',format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


# Function to check if the user is registered
def is_registered(update: Update):
    return update.effective_user.id in USERS


# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_registered(update):
        logger.warning(f"Unauthorized access denied for {update.effective_user.mention_html()}.")
        await update.message.reply_text(f"Sorry {update.effective_user.name}.\nYou are not authorized to use this bot.")
        return
    logger.info(f"{update.effective_user.name} ({update.effective_user.id}): Started the bot!")
    await update.message.reply_text(f"Hi <b> {update.effective_user.name}! </b>\n\nWelcome to <b>EggPuff</b> Bot.\nUse /help to see the list of available commands.",
                                    parse_mode="HTML")

# Help command
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"{update.effective_user.name} ({update.effective_user.id}): Asked for Help!")
    await update.message.reply_text(help_text, parse_mode="HTML")

# Command to get the IP address
async def getIp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_registered(update):
        logger.warning(f"Unauthorized access denied for {update.effective_user.mention_html()}.")
        await update.message.reply_text(f"Sorry {update.effective_user.name}.\nYou are not authorized to use this bot.")
        return
    try:
        ip = subprocess.check_output("hostname -I", shell=True).decode("utf-8")
        logger.info(f"{update.effective_user.name} ({update.effective_user.id}): Requested for IP Address!")
        await update.message.reply_text(f"IP Address: {ip}")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Error occurred while fetching the IP address.")

# Command to manage services
async def service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_registered(update):
        logger.warning(f"Unauthorized access denied for {update.effective_user.mention_html()}.")
        await update.message.reply_text(f"Sorry {update.effective_user.name}.\nYou are not authorized to use this bot.")
        return
    try:
        if len(context.args) < 2 or len(context.args) > 2:
            await update.message.reply_text("Wrong Command Usage.\nUsage: /services <action> <service>")
            return
        action = context.args[0].lower()
        service = context.args[1].lower()
        if action == "start":
            logger.info(f"{update.effective_user.name} ({update.effective_user.id}): Started {service}!")
            subprocess.run(f"echo '123' | sudo - systemctl start {service}", shell=True, check=True)
            await update.message.reply_text(f"Starting {service}...")
        elif action == "stop":
            logger.info(f"{update.effective_user.name} ({update.effective_user.id}): Stopped {service}!")
            subprocess.run(f"echo '123' | sudo -S systemctl stop {service}", shell=True, check=True)
            await update.message.reply_text(f"Stopping {service}...")
        elif action == "restart":
            logger.info(f"{update.effective_user.name} ({update.effective_user.id}): restarted {service}!")
            subprocess.run(f"echo '123' | sudo -S systemctl restart {service}", shell=True, check=True)
            await update.message.reply_text(f"Restarting {service}...")   
        elif action == "status":
            logger.info(f"{update.effective_user.name} ({update.effective_user.id}): Got status of {service}!")
            result = subprocess.run(f"echo '123' | sudo -S systemctl status {service}", capture_output=True,shell=True, text=True)
            status = result.stdout.strip().capitalize()
            await update.message.reply_text(f"{service} is {status}")
        else:
            await update.message.reply_text(f"Invalid action - {action}.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"Error occurred while executing {action}.")

# run the command
async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if int(update.effective_user.id) != 7751114901:
        logger.warning(f"Unauthorized access denied for {update.effective_user.mention_html()}.")
        await update.message.reply_text(f"Sorry {update.effective_user.name}.\nYou are not authorized to use this bot.")
        return
    try:
        command = " ".join(context.args)

        # check if args in empty
        if len(context.args) == 0:
            logger.warning(f"Invalid Command usage - /run is empty")
            await update.message.reply_text("<b>Invalid command usage</b>", parse_mode="HTML")
            return
        # check if the command is restricted
        if any(cmd in command for cmd in restricted_commands):
            logger.warning(f"Restricted command form {update.effective_user.name} ({update.effective_user.id}): {command}")
            await update.message.reply_text("Restricted Command.")
            return

        await update.message.reply_text(f"Executing: {command}")

        logger.info(f"{update.effective_user.name} ({update.effective_user.id}): Executing {command}!")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            await update.message.reply_text(result.stdout)
        if result.stderr:
            await update.message.reply_text(result.stderr)
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Error occurred while executing the command.")

# takenote command
async def takeNote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_registered(update):
        logger.warning(f"Unauthorized access denied for {update.effective_user.mention_html()}.")
        await update.message.reply_text(f"Sorry {update.effective_user.name}.\nYou are not authorized to use this bot.")
        return
    try:
        note = " ".join(context.args)
        if not os.path.exists("/home/preran/notes.txt"):
            with open("/home/preran/notes.txt", "w") as file:
                file.write("")

        with open("/home/preran/notes.txt", "a") as file:
            file.write(note + "\n")
        await update.message.reply_text("Note saved.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Error occurred while saving the note.")

# get last 10 note command
async def getNotes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_registered(update):
        logger.warning(f"Unauthorized access denied for {update.effective_user.mention_html()}.")
        await update.message.reply_text(f"Sorry {update.effective_user.name}.\nYou are not authorized to use this bot.")
        return
    try:
        with open("/home/preran/notes.txt", "r") as file:
            notes = file.readlines()
        last_10_notes = notes[-10:]
        await update.message.reply_html("<b>Last 10 notes:</b>\n" + "".join(last_10_notes))
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Error occurred while fetching the notes.")

# to handle invalid commands
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_registered(update):
        logger.warning(f"Unauthorized access denied for {update.effective_user.mention_html()}.")
        await update.message.reply_text(f"Sorry {update.effective_user.name}.\nYou are not authorized to use this bot.")
        return
    await update.message.reply_text("Invalid Command.\nUse /help to see the list of available commands.")

# function to display all files present in the directory
async def list_files(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_registered(update):
        logger.warning(f"Unauthorized access denied for {update.effective_user.mention_html()}.")
        await update.message.reply_text(f"Sorry {update.effective_user.name}.\nYou are not authorized to use this bot.")
        return
    if len(context.args) != 1:
        await update.message.reply_text("Wrong Command Usage.\nUsage: /list_files <file>")
        return
    try:
        path = context.args[0]
        files = os.listdir(path)
        if not files:
            await update.message.reply_text(f"No files found in the <b>{path}</b> directory.", parse_mode="HTML")
        else:
            file_list = "\n".join(files)
            await update.message.reply_text(f"<b>Available files:</b>\n{file_list}",parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"<b>Error listing files:</b>\n{e}",parse_mode="HTML")
            
async def send_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_registered(update):
        await update.message.reply_text(f"Sorry {update.effective_user.name}.\nYou are not authorized to use this bot.")
        return
    if len(context.args) != 2:
        await update.message.reply_text("Wrong Command Usage.\nUsage: /send_file <path> <file>")
        return
    path = context.args[0]
    file = context.args[1]

    file_path = os.path.join(path, file)

    try:
        if os.path.isfile(file_path):
            # Send the file
            with open(file_path, "rb") as f:
                await update.message.reply_document(f)
        else:
            await update.message.reply_text(f"File '{file}' not found in the notebooks directory.")
    except Exception as e:
        await update.message.reply_text(f"Error sending file: {e}")



# Echo the message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_registered(update):
        logger.warning(f"Unauthorized access denied for {update.effective_user.mention_html()}.")
        await update.message.reply_text(f"Sorry {update.effective_user.name}.\nYou are not authorized to use this bot.")
        return
    await update.message.reply_text(update.message.text)

# Main function
def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("get_ip", getIp))
    application.add_handler(CommandHandler("services", service))
    application.add_handler(CommandHandler("run", run))
    application.add_handler(CommandHandler("take_note", takeNote))
    application.add_handler(CommandHandler("get_notes", getNotes))
    application.add_handler(CommandHandler("send_file", send_file))
    application.add_handler(CommandHandler("list_files", list_files))

    #invalid command
    application.add_handler(MessageHandler(filters.COMMAND, error))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
