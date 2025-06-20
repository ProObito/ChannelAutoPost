import logging
from telethon import TelegramClient, events, Button

logging.basicConfig(
    level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s"
)
log = logging.getLogger("SimpleSpamBot")

# Hardcoded configuration values
API_ID = 19863702  # Your API ID
API_HASH = "6d48cb362a97a43cfc944fd5c0f917f9"  # Your API Hash
BOT_TOKEN = "8093258063:AAGcnTXrd5bGUab6yMmSUAeW1KrC0Eqt-Qk"  # Your Bot Token

# Start the bot
log.info("Starting...")
try:
    datgbot = TelegramClient(None, API_ID, API_HASH).start(bot_token=BOT_TOKEN)
except Exception as exc:
    log.error("Error in starting the bot: %s", exc)
    log.info("Bot is quitting...")
    exit()

# /start command
@datgbot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply(
        f"Hi {event.sender.first_name}!\n\n"
        "I'm a simple spam bot.\nUse /help or /format to see how to use me.",
        buttons=[
            Button.url("Source Code", url="https://github.com/xditya/ChannelAutoForwarder"),
            Button.url("Developer", url="https://xditya.me"),
        ],
        link_preview=False,
    )

# /help command
@datgbot.on(events.NewMessage(pattern="/help"))
async def helpp(event):
    await event.reply(
        "Help\n\n"
        "I can send a message multiple times.\n"
        "Use the /spam command followed by a number and a message.\n\n"
        "Example: /spam 5 Hello\n\n"
        "This sends 'Hello' 5 times in this chat."
    )

# /format command
@datgbot.on(events.NewMessage(pattern="/format"))
async def format_command(event):
    await event.reply(
        "Usage Format\n\n"
        "/spam <count> <message>\n\n"
        "Where:\n"
        "- <count> = Number of times to send the message (must be a number)\n"
        "- <message> = The text you want to repeat\n\n"
        "Example:\n"
        "/spam 5 Hello World!\n\n"
        "This sends 'Hello World!' 5 times in this chat."
    )

# /spam command
@datgbot.on(events.NewMessage(pattern="/spam"))
async def spam(event):
    try:
        command_parts = event.text.split(" ", 2)
        if len(command_parts) < 3:
            await event.reply("❗ Usage: /spam <count> <message>\nExample: /spam 3 Hello")
            return

        times = int(command_parts[1])
        message = command_parts[2]

        if times > 50:
            await event.reply("⚠ Too many messages! Limit is 50.")
            return

        chat = event.chat_id

        for _ in range(times):
            await datgbot.send_message(chat, message)

        await event.reply(f"✅ Done! Sent the message {times} times.")

    except ValueError:
        await event.reply("❗ Make sure the count is a number.\nExample: /spam 5 Hello")
    except Exception as e:
        log.error("Error in /spam command: %s", e)
        await event.reply("❌ An error occurred. Please try again.")

# Run the bot
log.info("Bot has started. Ready to spam!")
datgbot.run_until_disconnected()
