import json

#get --config_file argument form command line
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config_file", help="Path to config file", required=False)
parser.add_argument("--model_param_file", help="Path to the model parameter file", required=False)
parser.add_argument("--character_file", help = "Path to the character file", required=False)
args = parser.parse_args()

# check if argument exists
if args.config_file == None:
    print("No config file specified using. config.json")
    config_filename = "config.json"
else:
    config_filename = args.config_file

#open config file
with open(config_filename, "r") as f:
        config = json.load(f)

chat_app = config["chat_app"]

# check chat app
if chat_app == "discord":

    discord_token = config["discord_bot_token"]

elif chat_app == "telegram":

    # Extract telegram token from config
    telegram_token = config["telegram_bot_token"]


use_magister = config["use_magister"]

if use_magister:

    username = config["magister_username"]
    password = config["magister_password"]
    school = config["magister_school"]

model = config["model"]

if args.model_param_file == None:
    print("No model parameter file specified. using model_parameters.json")
    model_param_filename = "model_parameters.json"
else:
    config_filename = args.config_file


with open(model_param_filename, "r") as f:
        model_parameters = json.load(f)

message_context_size = model_parameters["message_context_size"]
repetition_penalty = model_parameters["repetition_penalty"]

if args.character_file == None:
    print("No character file specified. using character.json")
    character_filename = "character.json"
else:
    config_filename = args.character_filename


with open(model_param_filename, "r") as f:
        model_parameters = json.load(f)