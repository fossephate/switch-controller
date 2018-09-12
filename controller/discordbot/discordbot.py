
# discord
import discord
import asyncio
import threading
import keyboard

# config
try:
	from .config import *
except:
	from config import *

class DiscordBot(discord.Client):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# create the background task and run it in the background
		self.bg_task = self.loop.create_task(self.my_background_task())
		self.channelToSend = None
		self.messageToSend = None

	async def on_ready(self):
		print("Logged in as")
		print(self.user.name)
		print(self.user.id)
		print("------")
		# await self.send_message(self.get_channel("487328538173767692"), "bot starting")
		# await this.send_message(discord.Object(id="487328538173767692"), "bot starting")

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


	async def my_background_task(self):

		await self.wait_until_ready()

		while not self.is_closed():

			# hack:
			if (self.channelToSend != None and self.messageToSend != None):
				channel = self.get_channel(self.channelToSend)
				await channel.send(self.messageToSend)
				self.channelToSend = None
				self.messageToSend = None
			await asyncio.sleep(1) # task runs every 10 seconds

	def send_message(self, channel, message):
		self.channelToSend = channel
		self.messageToSend = message


# discordBot = DiscordBot()
# discordBotThread = threading.Thread(target=discordBot.run, args=(DISCORDBOT_TOKEN,))
# discordBotThread.start()
# discordBot.run(DISCORDBOT_TOKEN)

# sleep(3)

# discordBot.custom_send_message1("487328538173767692", "test message2")


# while True:

# 	try: #used try so that if user pressed other than the given key error will not be shown
# 		if keyboard.is_pressed("q"):#if key 'q' is pressed 
# 			discordBot.custom_send_message1("bot-messages", "test message")
# 		else:
# 			pass
# 	except:
# 		pass









# # discord
# import discord
# import asyncio

# # config
# from config import *

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Logged in as')
#         print(self.user.name)
#         print(self.user.id)
#         print('------')

#     async def on_message(self, message):
#         # don't respond to ourselves
#         if message.author == self.user:
#             return
#         if message.content.startswith('!test'):
#             counter = 0
#             tmp = await message.channel.send('Calculating messages...')
#             async for msg in message.channel.history(limit=100):
#                 if msg.author == message.author:
#                     counter += 1

#             await tmp.edit(content='You have {} messages.'.format(counter))
#         elif message.content.startswith('!sleep'):
#             with message.channel.typing():
#                 await asyncio.sleep(5.0)
#                 await message.channel.send('Done sleeping.')

# client = MyClient()
# client.run(DISCORDBOT_TOKEN)

# class DiscordBot():
	
# 	def __init__(self):
# 		self.sock = socket.socket()
# 		self.CHAN = ""
# 		self.PASS = ""
# 		self.NICK = ""
# 		self.HOST = ""
# 		self.PORT = 0




