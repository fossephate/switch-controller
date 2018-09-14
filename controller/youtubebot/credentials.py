import sys
import os.path
import httplib2
from oauth2client import client

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Credentials:


    

    def __init__(self, credentialsFileName=None):
        self.credentials = {}
        self.credentialsFileName = credentialsFileName

    def expired(self):
        # print(self.credentials)
        expired = ""
        try:
            expired = self.credentials.access_token_expired
        except:
            expired = ""
        return expired

    def read(self):
        if not os.path.isfile(os.path.join(__location__, self.credentialsFileName)):
            print("Auth first")
            sys.exit(1)

        credentialsFile = open(os.path.join(__location__, self.credentialsFileName), "r")
        credentialsJSON = credentialsFile.read()

        self.credentials = client.OAuth2Credentials.from_json(credentialsJSON)

        token_obj = self.credentials.get_access_token()
        token_str = str(token_obj.access_token)
        return token_str

    def auth(self):
        if os.path.isfile("OAuthCredentials.json"):
            print("Trying to auth but OAuthCredentials.json exists")
            return
        flow = client.flow_from_clientsecrets(
            "client_secrets.json",
            scope="https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/youtube.force-ssl",
            redirect_uri="https://twitchplaysnintendoswitch.com/8110/auth/youtube/callback/")

        auth_uri = flow.step1_get_authorize_url()
        # print(auth_uri)
        # print(auth_uri + "&access_type=offline&approval_prompt=force")
        print(auth_uri + "&approval_prompt=force")

        print("Open the shown link")
        auth_code = input('Enter the auth code: ')

        self.credentials = flow.step2_exchange(auth_code)
        self.credentials.authorize(httplib2.Http())

        outFile = open("OAuthCredentials.json", "w")
        outFile.write(str(self.credentials.to_json()))
        outFile.close()


if __name__ == '__main__':
    c = Credentials()
    c.auth()
