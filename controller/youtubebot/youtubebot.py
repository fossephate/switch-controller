#!/usr/bin/env python3
import sys
import json
import time
import requests
try:
	from .credentials import Credentials
except:
	from credentials import Credentials

from pprint import pprint


# windows api:
import win32api
import win32con


class YouTubeBot:

	def __init__(self):

		
		self.credentialsBot = Credentials("oauth-tpnsbot.json")
		self.credentialsChannel = Credentials("oauth-fosse.json")

		self.token_str1 = self.credentialsBot.read()
		self.token_str2 = self.credentialsChannel.read()

		self.liveChatID = self.get_livechat_id()
		self.stopped = False
		self.messages = []

		if not self.liveChatID:
			print("[] No livestream found :(")
		else:
			print("Live Chat ID: ", self.liveChatID)

	def handle_msg(self, msg):
		# pprint(msg)
		if msg["snippet"]["type"] != "textMessageEvent":
			print("non text message event")
			return

		# print(msg)
		# print(msg["authorDetails"])
		username = msg["authorDetails"]["displayName"]
		message = msg["snippet"]["displayMessage"]
		# print("<" + username + "> " + message)
		self.messages.append({"username": username, "message": message})

	def main(self):
		nextPageToken = ""
		token_str1 = ""
		token_str2 = ""
		while not self.stopped:
			# Make sure access token is valid before request
			# credentials.read() should refresh the token automatically
			if self.credentialsBot.expired() or token_str1 == "":
				token_str1 = self.credentialsBot.read()

			if self.credentialsChannel.expired() or token_str2 == "":
				token_str2 = self.credentialsChannel.read()

			payload = {"liveChatId": self.liveChatID,
					   "part": "snippet,authorDetails",
					   "pageToken": nextPageToken}
			url = "https://content.googleapis.com/youtube/v3/liveChat/messages"
			headers = {"Authorization": "Bearer " + token_str1}
			r = requests.get(url, headers=headers, params=payload)

			if (r.status_code == 200):
				resp = r.json()
				nextPageToken = resp["nextPageToken"]
				msgs = resp["items"]
				for msg in msgs:
					self.handle_msg(msg)

				delay = resp["pollingIntervalMillis"]/1000
				# delay = 3
			elif (r.status_code == 401):  # Unauthorized
				delay = 10
				if not self.credentials.expired:
					print("Error: Unauthorized. waiting 30 seconds...")
					if (debug >= 1):
						resp = r.json()
						print(json.dumps(resp, indent=4, sort_keys=True))
					delay = 30
			else:
				print("Unrecognized error:\n")
				resp = r.json()
				print(json.dumps(resp, indent=4, sort_keys=True))
				delay = 30
				delay = 3  #FIXME testing

			if win32api.GetAsyncKeyState(ord("Q")):
				print("sending message!")
				self.send_message("test message")

			time.sleep(delay)

	def send_message(self, message):

		url = "https://www.googleapis.com/youtube/v3/liveChat/messages"
		parameters = {"part": "snippet"}
		data = \
		{
		  "snippet": {
			"type": "textMessageEvent",
			"liveChatId": str(self.liveChatID),
			"textMessageDetails": {
				"messageText": message
			}
		  }
		}

		token_str1 = self.credentialsBot.read()
		headers = {"Authorization": "Bearer " + token_str1}

		r = requests.post(url, json=data, headers=headers, params=parameters)
		# print(r.status_code, r.reason, r.content)
		# print(r.status_code, r.reason)

	def get_livechat_id(self):
		token_str2 = self.credentialsChannel.read()
		url = "https://content.googleapis.com/youtube/v3/liveBroadcasts"
		payload = \
		{
			"broadcastStatus": "active",
			"broadcastType": "all",
			"part": "id, snippet, contentDetails"
		}
		headers = {"Authorization": "Bearer " + token_str2}
		r = requests.get(url, headers=headers, params=payload)
		if r.status_code == 200:
			resp = r.json()
			if len(resp["items"]) == 0:
				return False
			else:
				# Should only be 1 item unless YT adds multiple livestreams
				# then we'll assume it's the first for now
				print("Live events:", len(resp["items"]))
				# pprint(resp)
				print("*" * 50)
				streamMeta = resp["items"][0]["snippet"]
				liveChatID = streamMeta["liveChatId"]
				return liveChatID
		else:
			print("Unrecognized error:\n")
			resp = r.json()
			print(json.dumps(resp, indent=4, sort_keys=True))