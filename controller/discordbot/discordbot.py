
# discord
import discord
import asyncio

# config
from config import *

class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        if message.content.startswith("!test"):
            counter = 0
            tmp = await message.channel.send("Calculating messages...")
            async for msg in message.channel.history(limit=100):
                if msg.author == message.author:
                    counter += 1

            await tmp.edit(content="You have {} messages.".format(counter))
        elif message.content.startswith("!sleep"):
            with message.channel.typing():
                await asyncio.sleep(5.0)
                await message.channel.send("Done sleeping.")

client = MyClient()
client.run(BOT_TOKEN)

# class DiscordBot():
	
# 	def __init__(self):
# 		self.sock = socket.socket()
# 		self.CHAN = ""
# 		self.PASS = ""
# 		self.NICK = ""
# 		self.HOST = ""
# 		self.PORT = 0




