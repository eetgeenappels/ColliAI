import json
import sys

#get --config_file argument form command line
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--config_file", help="Path to config file")
args = parser.parse_args()

# check if argument exists
if args.config_file is None:
    print("No config file specified, exiting")
    config_filename = "config.json"
else:
    config_filename = args.config_file

with open(config_filename, "r") as f:
    config = json.load(f)

# Extract telegram token from config
telegram_token = config["telegram_token"]
username = config["magister_username"]
password = config["magister_password"]
school = config["magister_school"]
model = config["model"]