import os
import time
from random import randint
from threading import Thread

import telegram
from telegram.ext import Updater, CommandHandler

from yoku.consts import BOT_TOKEN_ENVVAR
from yoku.database import add_query, remove_query, search_and_notify, list_queries
from yoku.botutils import send_message

from pathlib import Path


# Retrieve environment variables
BOT_TOKEN = os.environ.get(BOT_TOKEN_ENVVAR)
if not BOT_TOKEN:
    print(f"`{BOT_TOKEN_ENVVAR}` environment variable not set")
    exit(1)

bot = telegram.Bot(BOT_TOKEN)


def get_message_data(update):
    """
    Parse Telegram `update` object and return chat ID and query text
    """

    message_json = update.message
    chat_id = str(message_json["chat"]["id"])
    message_full = message_json["text"]
    query_text = " ".join(message_full.split()[1:])

    return chat_id, query_text


def add(update, context):
    """
    Add a query for user
    """

    chat_id, query_text = get_message_data(update)
    if not query_text:
        return

    add_query(chat_id, query_text)


def rm(update, context):
    """
    Remove a query for user
    """

    chat_id, query_text = get_message_data(update)
    if not query_text:
        return

    remove_query(chat_id, query_text)


def ls(update, context):
    """
    List queries of a user
    """

    chat_id, _ = get_message_data(update)
    queries = list_queries(chat_id)
    if not queries:
        return

    send_message(chat_id, "\n".join(queries), bot)


def force(update, context):
    """
    Force fetch queries 
    """

    search_and_notify(bot)


def main_loop():
    while True:
        search_and_notify(bot)
        s = randint(1000, 10000)
        print(f"Sleeping for {s}s")
        time.sleep(s)


def main():
    # Initialize Telegram bot
    updater = Updater(BOT_TOKEN)

    # Add command handlers
    updater.dispatcher.add_handler(CommandHandler("add", add))
    updater.dispatcher.add_handler(CommandHandler("rm", rm))
    updater.dispatcher.add_handler(CommandHandler("ls", ls))
    updater.dispatcher.add_handler(CommandHandler("force", force))

    # Start the api polling loop in a thread
    Thread(target=main_loop).start()

    # Start the Telegram bot
    updater.start_polling()

    print(f"Bot started")
    updater.idle()


if __name__ == "__main__":
    main()
