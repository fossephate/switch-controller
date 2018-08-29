from urllib.parse import urlencode
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, InvalidURL, ConnectionError
import json

# https://www.reddit.com/r/Twitch/comments/6ycems/an_example_python_script_to_retrieve_a_list_of/

def getSubList():

	##########################################################
	#                Configure your stuff here               #
	##########################################################

	clientId="jhopzq3gncn6u41vp7lh9jtvj68wdx"  #Register a Twitch Developer application and put its client ID here
	accessToken="m1n2we1s1v3rxb5e4oiu1n0q0z4vio" #Generate an OAuth token with channel_subscriptions scope and insert your token here

	channelName="twitchplaysconsoles"  #Put your channel name here
	saveLocation = "subscriberList.txt" #Put the location you'd like to save your list here

	###################################################################

	session=Session()
	channelId=""


	channelIdUrl="https://api.twitch.tv/kraken/users?login="+channelName

	retryAdapter = HTTPAdapter(max_retries=2)
	session.mount("https://", retryAdapter)
	session.mount("http://", retryAdapter)

	#Find the Channel ID
	response = session.get(channelIdUrl, headers={
	"Client-ID": clientId,
	"Accept": "application/vnd.twitchtv.v5+json",
	"Content-Type": "application/json"
	})
	try:
		result = json.loads(response.text)
	except:
		result = None

	if (result):
		channelId = result["users"][0]["_id"]

	# print(channelId)

	result = None
	response = None
	offset=0
	limit=100
	sublist=[]

	while (True):
		apiRequestUrl="https://api.twitch.tv/kraken/channels/"+channelId+"/subscriptions?limit="+str(limit)+"&offset="+str(offset)

		#Do the API Lookup
		response = session.get(apiRequestUrl, headers={
		"Client-ID": clientId,
		"Accept": "application/vnd.twitchtv.v5+json",
		"Authorization": "OAuth "+accessToken,
		"Content-Type": "application/json"
		})

		try:
			result = json.loads(response.text)
		except:
			result = None

		if (result):
			for sub in result["subscriptions"]:
				name=sub["user"]["display_name"]
				if name!=channelName:
					# print(name)
					sublist.append(sub["user"]["display_name"])
		else:
			break

		if (len(result["subscriptions"])==limit):
			offset+=limit
		else:
			# print("Done")
			break

	return sublist


# if(result):
# 	f = open(saveLocation,'w')
# 	for sub in sublist:
# 		f.write(sub+"\n")
# 	f.close()