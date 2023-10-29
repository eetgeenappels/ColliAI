import json

#get --config_file argument form command line
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config_file", help="Path to config file")
args = parser.parse_args()

# check if argument exists
if args.config_file == None:
    print("No config file specified, exiting")
    config_filename = "config.json"
else:
    config_filename = args.config_file

with open(config_filename, "r") as config_file:
    config = json.loads(config_file.read())


chat_app = config["chat_app"]

# check chat app and get app token
if config["chat_app"] == "discord":
    
    discord_bot_token = config["discord_bot_token"]

elif config["chat_app"] == "telegram":

    telegram_bot_token = config["telegram_bot_token"]


# chekc for magister implementation
use_magister = config["use_magister"]

if use_magister:

    username = config["magister_username"]
    password = config["magister_password"]
    school = config["magister_school"]

model = config["model"]

