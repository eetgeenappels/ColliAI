import json

#get --config_file argument form command line
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config_file", help="Path to config file")
args = parser.parse_args()

# check if argument exists
if args.config_file == None:
    print("No config file specified using config.json")
    config_filename = "config.json"
else:
    config_filename = args.config_file

#open config file
with open(config_filename, "r") as f:
        config = json.load(f)

# check chat app
if config["chat_app"] == "discord":

    bot_token = config["discord_bot_token"]

elif config["chat_app"] == "telegram":

    # Extract telegram token from config
    telegram_token = config["telegram_bot_token"]


use_magister = config["use_magister"]

if use_magister:

    username = config["magister_username"]
    password = config["magister_password"]
    school = config["magister_school"]

model = config["model"]

