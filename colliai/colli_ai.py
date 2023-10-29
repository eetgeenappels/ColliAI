from telegram.telegram_bot import TelegramBot
import credentials
from magister.magister_scraper import Scraper
from textgen import memory
from sd import intent_classefier
from textgen.interference import ConversationalAI
from discord import discord_bot

# open config file with json and pull out username and password
magister_scraper = None
if credentials.use_magister:
    print("Logging in with Magister...")
    magister_scraper = Scraper(credentials.username,credentials.password, credentials.school)

print("Loading Model...")

ai = ConversationalAI()

print("Loading database...")

memory.create_database()
memory.load_model()

print("Loading Intent Classifier...")

intent_classefier.load_model()

if credentials.chat_app == "telegram":

    print("Starting Telegram Bot...")

    TelegramBot(credentials.telegram_token, ai,magister_scraper= magister_scraper).start()

elif credentials.chat_app == "discord":

    print("Starting Discord Bot...")

    discord_bot.DiscordBot(credentials.discord_token, ai, magister_scraper=magister_scraper).start()

    pass
