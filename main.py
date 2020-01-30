import logging
import os
import random
import sys
import threading


from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from utils.name_matcher import upload_song_configs

TOKEN = '<telegram_bot_token>'

threading.Lock()
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
bot = updater.bot


class ChatMachine():
    def __init__(self, configs):
        self.state = "idle"
        self.configs = configs


text_configs = upload_song_configs('./static/configs/song_names.json')
machine = ChatMachine(text_configs)

lock = threading.Lock()


def start(_, update):
    logging.info(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text=f"привет кожаный ублюдок. создатель у меня тот еше кент, "
                                                          f"поэтому я только в команды могу пока что."
                                                          f"набери /help и я тебе все расскажу хех")


def helper(_, update):
    bot.send_message(chat_id=update.message.chat_id, text=f"/start - из вере ви олл беги\n "
                                                          f"/help - это инструкция по командам\n"
                                                          f"/song - рандомная песенка(пока в разработке)\n"
                                                          f"/text - получить текст песни(я спрошу какой йо)\n"
                                                          f"/song - рандомная песенка из нашего репертуара\n")


def text_command(_, update):
    bot.send_message(chat_id=update.message.chat_id, text="какой текст ты хочешь-то?")
    with lock:
        machine.state = "text_request"


def song_command(_, update):
    songs = os.listdir('./static/content/audio')
    if songs:
        item = random.sample(songs, 1)[0]
        bot.send_audio(chat_id=update.message.chat_id, audio=open(os.path.join('./static/content/audio', item), 'rb'))
    else:
        bot.send_message(chat_id=update.message.chat_id, text='чет по ходу песен нету ни одной о_О. Админ уже выехал')


def text(bot, update):
    resp = None
    if machine.state == "text_request":
        name = machine.configs.get(update.message.text)
        if name:
            with open("./static/content/texts/" + name + ".txt", 'r') as f:
                resp = f.read()
        with lock:
            machine.state = "idle"
    resp = resp or "не понимать. или такого текста нет, или ты чет не то делаешь. набери /help"
    bot.send_message(chat_id=update.message.chat_id, text=resp)


text_handler = MessageHandler(Filters.text, text)
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', helper)
text_command_handler = CommandHandler('text', text_command)
song_command_handler = CommandHandler('song', song_command)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(text_handler)
dispatcher.add_handler(song_command_handler)
dispatcher.add_handler(text_command_handler)
updater.start_polling()