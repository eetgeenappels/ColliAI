from TextGeneration.interference import ConversationalAI
from Telegram.telegram_bot import TelegramBot
import Telegram.credentials as credentials
from magister.magister_scraper import Scraper
from TextGeneration import memory

# open config file with json and pull out username and password
magister_scraper = Scraper(credentials.username,credentials.password, credentials.school)

ai = ConversationalAI()
ai.start()

memory.create_database()
memory.load_model()

TelegramBot(credentials.telegram_token, ai, magister_scraper).start()