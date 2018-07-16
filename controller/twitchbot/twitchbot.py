# bot.py
# http://www.instructables.com/id/Twitchtv-Moderator-Bot/
import socket
from time import sleep
import re
from .config import *
import requests

CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

class TwitchBot():
	
	def __init__(self):
		self.sock = socket.socket()
		self.CHAN = ""
		self.PASS = ""
		self.NICK = ""
		self.HOST = ""
		self.PORT = 0

	def chat(self, msg):
		"""
		Send a chat message to the server.
		Keyword arguments:
		sock -- the socket over which to send the message
		msg  -- the message to be sent
		"""
		#self.sock.send("PRIVMSG #{} :{}".format(CHAN, msg))
		# full_msg = "PRIVMSG #{} :{}".format(CHAN, msg)

		full_msg = "PRIVMSG " + self.CHAN + " :" + msg + "\r\n"
		
		msg_encoded = full_msg.encode("utf-8")
		self.sock.send(msg_encoded)


	def ban(self, user):
		"""
		Ban a user from the current channel.
		Keyword arguments:
		sock -- the socket over which to send the ban command
		user -- the user to be banned
		"""
		chat(self.sock, ".ban {}".format(user))

	def timeout(self, user, secs=600):
		"""
		Time out a user for a set period of time.
		Keyword arguments:
		sock -- the socket over which to send the timeout command
		user -- the user to be timed out
		secs -- the length of the timeout in seconds (default 600)
		"""
		chat(self.sock, ".timeout {}".format(user, secs))

	def connect(self, HOST, PASS, PORT, CHANNEL, NICK):
		self.HOST = HOST
		self.PASS = PASS
		self.CHAN = CHAN
		self.NICK = NICK
		self.PORT = PORT

		self.sock.connect((self.HOST, self.PORT))
		self.sock.send("PASS {}\r\n".format(self.PASS).encode("utf-8"))
		self.sock.send("NICK {}\r\n".format(self.NICK).encode("utf-8"))
		self.sock.send("JOIN {}\r\n".format(self.CHAN).encode("utf-8"))

	def stayConnected(self):
		response = "none"
		self.sock.setblocking(False)
		# self.sock.settimeout(0.1)
		try:
			response = self.sock.recv(1024).decode("utf-8")
		except:
			pass
		if(response == "PING :tmi.twitch.tv\r\n"):
			self.sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
			return "none"
		else:
			#username = re.search(r"\w+", response).group(0) # return the entire match
			#message = CHAT_MSG.sub("", response)
			#print(username + ": " + message)
			return response

	def set_title_game(self, title, game):
		scope = "&scope=channel_editor"
		client_id = "&client_id=" + CLIENT_ID
		redirect_uri = "&redirect_uri=https://twitchplaysnintendoswitch.com/8110/auth/twitch/callback"
		response_type = "&response_type=code"
		url = "https://api.twitch.tv/kraken/oauth2/authorize?" + client_id + redirect_uri + response_type + scope
		params = {"Client-ID" : ""+ CLIENT_ID +"",
		          "Accept" : "application/vnd.twitchtv.v5+json"}
		resp = requests.get(url=url, headers=params)
		print(resp)

		#https://twitchplaysnintendoswitch.com/8110/auth/twitch/callback

		url = "https://api.twitch.tv/kraken/channels/twitchplaysconsoles"
		headers = {"Client-ID" : ""+ CLIENT_ID +"", "Authorization": "OAuth " + OAUTH}
		data = {"channel": {"status": "Twitch Plays Nintendo Switch!"}}
		response = requests.put(url=url, headers=headers, params = data)
		print(response)


# Make sure you prefix the quotes with an 'r'!
#CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# while True:

#     response = s.recv(1024).decode("utf-8")
#     if response == "PING :tmi.twitch.tv\r\n":
#         s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
#     else:
#         username = re.search(r"\w+", response).group(0) # return the entire match
#         message = CHAT_MSG.sub("", response)
#         print(username + ": " + message)
#     sleep(0.1)
#     #sleep(1 / RATE)


