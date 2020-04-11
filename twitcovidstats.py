import json, os
import twitter
from datetime import datetime
import requests

class TwitCovidStats:
    def __init__(self):
        with open('auth.json','r') as ff:
            auth = json.load(ff)
            
        self.api = twitter.Api(consumer_key=auth['API_key'],
                        consumer_secret=auth['API_secret_key'],
                        access_token_key=auth['Access_token'],
                        access_token_secret=auth['Access_token_secret'])

    def tweetUpdate(self,message):
        dt = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        source = 'https://api.apify.com/v2/key-value-stores/lFItbkoNDXKeSWBBA/records/LATEST?disableRedirect=true'
        footer = 'This is an automated tweet.'
        message = "{}\r\nas of {}\r\nSource: {}\r\n{}\r\nhttps://github.com/mrkprdo/twitcovidstats".format(message,dt,source,footer)
        post = self.api.PostUpdate(message)

    def getLatestNumber(self):
        respone = requests.get('https://api.apify.com/v2/key-value-stores/lFItbkoNDXKeSWBBA/records/LATEST?disableRedirect=true')
        return respone.json()

if __name__ == "__main__":

    tt = TwitCovidStats()
    latestUpdate = tt.getLatestNumber()
    message = """PH Covid19 UPDATE:

    Infected: {}
    Recovered: {}
    Deceased: {}
    """.format(latestUpdate['infected'],latestUpdate['recovered'],latestUpdate['deceased'])

    tt.tweetUpdate(message)