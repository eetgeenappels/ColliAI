import credentials
from textgen import memory
import time
from pprint import pprint
from magister import magister_scraper
from textgen.interference import ConversationalAI
import json


context = []

def init():
    global context
     
    with open("character.json","r") as f:
        context.append(f"{json.loads(f.read())['character_description']}")
    context.append("<start>")

def procces_message(message: str, magister_scraper: magister_scraper.Scraper, model: ConversationalAI):

    memory.add_message(f"### Instruction\n{message}\n")

    if ("school" in message.lower() or "lesson" in message.lower() or "class" in message.lower() or "teacher" in message.lower() or "room" in message.lower()) and credentials.use_magister:
         
         api_prompt = get_magister_rooster_promt(magister_scraper)

    elif "grade" in message.lower() and credentials.use_magister:

        api_prompt = get_magister_grade_prompt()

    st = time.time()

    memory_prompt = memory.get_context(memory.query(memory.get_embedding(message.text))["id"])
    reply = model.generate_response(context + memory.get_last_n_messages(20) ,memory_prompt = memory_prompt, api_prompt = api_prompt)

    et = time.time()

    print(f"Response generated in {et - st} seconds")
    memory.add_message(f"### Colli\n{reply}\n")

    return reply


def get_magister_rooster_promt(magister_scraper):

    subject_hashes = {
            "dr": "Theater",
            "na": "Physics",
            "gs": "History",
            "kmt": "Mentor Hour",
            "la": "Latin",
            "du": "German",
            "en": "English",
            "wi": "Math",
            "wtu": "WTU",
            "fa": "French",
            "lo": "Gym",
            "ak": "Geography",
            "ne": "Dutch",
            "gr": "Greek",
            "sk": "Chemistry"
        }

    rooster = magister_scraper.rooster()
    pprint(rooster)

    formatted_rooster = "These are the current classes of 'You:':\n\n"
    
    for lesson in rooster:
            formatted_rooster += f"The subject is {subject_hashes[lesson['vak']]} with teacher {lesson['docent']} in the room {lesson['lokaal']} in the Lesson hour {lesson['lesuur']})\n"

    return formatted_rooster

def get_magister_grade_prompt(magister_scraper):
     
    last_grade = magister_scraper.cijfers()[-1:][0]

    subject_hashes = {
        "natuurkunde": "Physics",
        "biologie": "Biology",
        "geschiedenis": "History",
        "latijn": "Latin",
        "Duitse taal": "German",
        "Franse taal": "French",
        "aardrijkskunde": "Geography",
        "drama":"Theater",
        "Engelse taal": "English",
        "lichamelijke opvoeding": "Gym",
        "godsdienst/levensbeschouwing": "Religion",
        "Nederlandse taal": "Dutch",
        "Griekse taal en letterkunde": "Greek",
        "wiskunde": "Math",
    }

    last_grade = f"The last grade was {last_grade['cijfer']}/10 in the {subject_hashes[last_grade['vak']]} subject."
     
    return last_grade