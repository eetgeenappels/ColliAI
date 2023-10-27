import discord
import time
import threading
import random
from textgen import message_handler

class DiscordBot:
    def __init__(self, token, model, magister_scraper=None):
        self.token = token
        self.model = model
        self.last_message = time.time()
        self.context = []
        self.magister_scraper = magister_scraper

        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)

    def start(self):
        @self.client.event
        async def on_ready():
            print(f'Logged in as {self.client.user.name}')
            print('------')

        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return

            self.last_message_type = "user_message"
            self.last_message = time.time()

            reply = message_handler.procces_message(message=message.content,magister_scraper= self.magister_scraper, model=self.model)

            if reply:
                await message.channel.send(reply)

        # Create and start the threads
        client_thread = threading.Thread(target=self.client.run, args=(self.token,))
        random_conv_waiter_thread = threading.Thread(target=self.random_conv_waiter)

        client_thread.start()
        random_conv_waiter_thread.start()

        print("Colli Online!!!")

        # Wait for both threads to complete
        client_thread.join()
        random_conv_waiter_thread.join()

    async def random_conv_waiter(self):
        
        # Randomly wait to start a new conversation
        self.last_message = time.time()

        while True:
            if time.time() - self.last_message > 8000 and self.last_message_type != "new_convo":
                time.sleep(60)

                # 1 in 15 chance to start a new conversation
                if random.randint(0, 15) == 0:
                    self.random_conv_start()

    async def random_conv_start(self):
        insert_prompt = "Colli wants to start a new conversation!"
        self.last_message = time.time()
        self.last_message_type = "new_convo"

        # Generate message
        st = time.time()
        reply = self.model.generate_response(self.chat_log, api_prompt=insert_prompt)
        et = time.time()

        self.chat_log.append(f"{reply}\n")

        print(f"sending: {reply}")

        # Send message
        # Replace 'channel_id' with the actual Discord DM channel ID
        channel_id = 'YOUR_CHANNEL_ID'
        channel = self.client.get_channel(channel_id)

        if channel:
            await channel.send(reply)
        else:
            print("Channel not found.")

        print("sent")