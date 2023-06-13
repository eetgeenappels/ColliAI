import telebot
import time
import threading
import random
import json
from TextGeneration import memory

class TelegramBot:
    def __init__(self, token, model, magister_scraper):
        self.bot = telebot.TeleBot(token)
        self.model = model
        self.last_message = time.time()
        self.last_chatid = 0
        self.magister_scraper = magister_scraper
        self.context = []

    def start(self):
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.bot.reply_to(message, "Hi! I'm Colli.")
            chat_id = message.chat.id
            with open("character.json","r") as f:
                context = json.loads(f.read())["character_description"]

            
            self.context.append(f"Context: {context}\n")
            self.context.append("<start>")
            self.last_chatid = chat_id
        
        @self.bot.message_handler(commands=['reset'])
        def handle_reset(message):
            chat_id = message.chat.id
            self.last_chatid = chat_id
            # handle database reset
            memory.reset_db()
            self.bot.reply_to(message, "Database reset.")

        @self.bot.message_handler(commands=['chatlog_raw'])
        def hande_chatlog_raw(message):
            from pprint import pformat
            self.bot.reply_to(message, pformat(self.chat_log))

        @self.bot.message_handler(commands=['chatlog_format'])
        def hande_chatlog_format(message):
            self.bot.reply_to(message, "".join(self.chat_log))

        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):

            self.last_message_type = "user_message"

            chat_id = message.chat.id

            self.last_chatid = chat_id

            self.last_message = time.time()
            
            memory.add_message(f"You: {message.text}\n")
            
            print(f"recieved: {message.text}")

            if "school" in message.text.lower() or "lesson" in message.text.lower() or "class" in message.text.lower() or "teacher" in message.text.lower() or "room" in message.text.lower():
                
                # fetch school data
                rooster = self.magister_scraper.rooster()

                from pprint import pprint
                pprint(rooster)

                formatted_rooster = "These are the current classes of 'You:':\n\n"

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

                for lesson in rooster:
                    formatted_rooster += f"The subject is {subject_hashes[lesson['vak']]} with teacher {lesson['docent']} in the room {lesson['lokaal']} in the Lesson hour {lesson['lesuur']})\n"

                print(formatted_rooster)

                st = time.time()

                memory_prompt = memory.get_context(memory.query(memory.get_embedding(message.text))["id"])
                reply = self.model.generate_response(self.context + memory.get_last_20_messages() ,memory_prompt = memory_prompt, api_prompt = formatted_rooster)

                et = time.time()

                print(f"sending: {reply}\n")

                if not reply == "":
                    self.bot.reply_to(message, reply)
                
                memory.add_message(f"Colli: {reply}")
                
                print(f"sent message")

            elif "grade" in message.text.lower():

                last_grade = self.magister_scraper.cijfers()[-1:][0]

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

                st = time.time()

                memory_prompt = memory.get_context(memory.query(memory.get_embedding(message.text))["id"])
                reply = self.model.generate_response(self.context + memory.get_last_20_messages() ,memory_prompt = memory_prompt, api_prompt = last_grade)

                et = time.time()

                print(f"sending: {reply}\n")

                if not reply == "":
                    self.bot.reply_to(message, reply)
                
                memory.add_message(f"Colli: {reply}")
                
                print(f"sent message")

            else:

                st = time.time()

                memory_prompt = memory.get_context(memory.query(memory.get_embedding(message.text))["id"])
                reply = self.model.generate_response(self.context + memory.get_last_20_messages() ,memory_prompt = memory_prompt)

                et = time.time()

                print(f"response generated in {et - st} seconds")

                print(f"sending: {reply}")

                if not reply == "":
                    self.bot.reply_to(message, reply)

                memory.add_message(f"Colli: {reply}\n")

                print(f"sent message")

        # Create and start the threads
        send_message_thread = threading.Thread(target=self.bot.polling)
        random_conv_waiter_thread = threading.Thread(target=self.random_conv_waiter)

        send_message_thread.start()
        random_conv_waiter_thread.start()

        print("Colli Online!!!")

        # Wait for both threads to complete
        send_message_thread.join()
        random_conv_waiter_thread.join()

    

    def random_conv_waiter(self):

        # randomly wait to start a new conversation

        self.last_message = time.time()

        while True:
            
            if time.time() - self.last_message > 8000 and self.last_message_type != "new_convo":
                time.sleep(60)

                # 1 in 15 chance to start new conversation

                if random.randint(0, 15) == 0:
                    self.random_conv_start()

                

    def random_conv_start(self):
        insert_promt = "Colli wants to start a new conversation!"

        print("sending new convo prompt")

        self.last_message = time.time()
        self.last_message_type = "new_convo"

        # generate message
        st = time.time()

        reply = self.model.generate_response(self.chat_log , api_prompt = insert_promt)

        et = time.time()

        print("message generated in " + str(et - st) + " seconds")

        self.chat_log.append(f"{reply}\n")

        print(f"sending: {reply}")

        # send message
        self.bot.send_message(self.last_chatid, reply)

        print("sent")