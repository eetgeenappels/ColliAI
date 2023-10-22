from telegram.telegram_bot import TelegramBot
import credentials
from magister.magister_scraper import Scraper
from textgen import memory
from sd import intent_classefier
from textgen.interference import ConversationalAI

# open config file with json and pull out username and password
magister_scraper = None
if credentials.use_magister:
    magister_scraper = Scraper(credentials.username,credentials.password, credentials.school)

ai = ConversationalAI()

memory.create_database()
memory.load_model()

intent_classefier.load_model()

if credentials.chat_app == "telegram":

    TelegramBot(credentials.telegram_token, ai,magister_scraper= magister_scraper).start()

elif credentials.chat_app == "discord":

    # WIP

    pass
