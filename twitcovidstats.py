import json, os
import twitter

class TwitCovidStats:
    def __init__(self):
        with open('auth.json','r') as ff:
            auth = json.load(ff)
            
        self.api = twitter.Api(consumer_key=auth['API_key'],
                        consumer_secret=auth['API_secret_key'],
                        access_token_key=auth['Access_token'],
                        access_token_secret=auth['Access_token_secret'])

    def postUpdate(self,message):
        message = "{} \r\nhttps://github.com/mrkprdo/twitcovidstats".format(message)
        self.api.PostUpdate(message)


if __name__ == "__main__":

    myhost = os.uname()[1]
    tt = TwitCovidStats()
    tt.postUpdate('Test Tweet from {}'.format(myhost))