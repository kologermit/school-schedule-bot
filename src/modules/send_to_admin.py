from telebot import TeleBot

def send_to_admin(text: str, bot: TeleBot, admins: list[int|str]):
    if admins:
        bot.send_message(admins[0], text)