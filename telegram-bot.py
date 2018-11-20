from telegram.ext import Updater, MessageHandler, Filters

from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.measure.cosine import CosineMeasure
from simstring.database.dict import DictDatabase
from simstring.searcher import Searcher
import re

db = DictDatabase(CharacterNgramFeatureExtractor(2))

with open('en_US.dic', 'r') as f:
    for word in f.read().split('\n'):
        db.add(re.split('/', word)[0])

searcher = Searcher(db, CosineMeasure())

def is_english(text):
    english = 0
    total = 0
    for token in re.split('[^a-zA-Zа-яА-Я]+', text):
        if not token:
            continue
    
        if searcher.search(token, 0.7):
            english += 1
        total += 1
    return english / total > 0.5

kulish_text = "English speaking is the pride, asset and value of Skoltech. Fluent widespread English makes Skoltech capable of becoming truly international place, attracting international students and building great careers and relationships. Hence we must be paranoid about upholding the tradition and habit of Skoltech speaking English."

def handle_message(bot, update):
    if not is_english(update.message.text):
        update.message.reply_text(kulish_text)

import os

TOKEN = "***REMOVED***"
PORT = int(os.environ.get('PORT', '8443'))
updater = Updater(TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
# add handlers
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
updater.bot.set_webhook("https://kulish-bot.herokuapp.com/" + TOKEN)
updater.idle()