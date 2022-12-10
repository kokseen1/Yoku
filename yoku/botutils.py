from datetime import datetime

from yoku.consts import KEY_TITLE, KEY_POST_TIMESTAMP, KEY_START_PRICE, KEY_URL


def send_message(chat_id, msg, bot):
    """
    Send a message without throwing
    """

    try:
        bot.sendMessage(chat_id, msg)
    except Exception as e:
        print(f"[TELEGRAM EXCEPTION] {e}")


def notify(chat_id, result, bot):
    """
    Notify a user of a new result
    """

    msg = f"{result[KEY_URL]}\n{result[KEY_TITLE]}\n{datetime.fromtimestamp(result[KEY_POST_TIMESTAMP]).strftime('%d/%m/%Y %I:%M:%S %p')}\n{result[KEY_START_PRICE]}¥"
    send_message(chat_id, msg, bot)
