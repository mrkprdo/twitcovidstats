import json, os
import twitter
from datetime import datetime
import requests
import csv

class TwitCovidStats:
    def __init__(self):
        with open('auth.json','r') as ff:
            auth = json.load(ff)
        self.dt = datetime.today().strftime('%Y-%m-%d-%H:%M:%S EDT')
        self.api = twitter.Api(consumer_key=auth['API_key'],
                        consumer_secret=auth['API_secret_key'],
                        access_token_key=auth['Access_token'],
                        access_token_secret=auth['Access_token_secret'])

    def tweetUpdate(self,message):
        source = 'https://api.apify.com/v2/key-value-stores/lFItbkoNDXKeSWBBA/records/LATEST?disableRedirect=true'
        footer = 'I created this to monitor PH Covid Status while on #QuarantineLife'
        message = "{}\r\nas of {}\r\nSource: {}\r\n{}\r\nhttps://github.com/mrkprdo/twitcovidstats".format(message,self.dt,source,footer)
        # print(message)
        post = self.api.PostUpdate(message)

    def getLatestNumber(self):
        response = requests.get('https://api.apify.com/v2/key-value-stores/lFItbkoNDXKeSWBBA/records/LATEST?disableRedirect=true')
        recent_update = response.json()
        with open('last_update.json', 'r') as last_update:
            last_values = json.load(last_update)
        if sorted(last_values.items()) == sorted(recent_update.items()):
            return 'same'
        else:
            with open('archive_data.csv', 'a+', newline='') as archive_data:
                fieldnames = ['date','infected','recovered','deceased']
                writer = csv.DictWriter(archive_data, fieldnames=fieldnames)
                writer.writerow({
                    'date': self.dt,
                    'infected': recent_update['infected'],
                    'recovered': recent_update['recovered'],
                    'deceased': recent_update['recovered'],
                    })
            with open('last_update.json', 'w') as last_update:
                json.dump(recent_update, last_update)
    
            return recent_update

if __name__ == "__main__":

    tt = TwitCovidStats()
    latestUpdate = tt.getLatestNumber()
    if latestUpdate == 'same':
        pass
        # print('No Update')
    else:
        message = """PH Covid19 UPDATE:

        Infected: {}
        Recovered: {}
        Deceased: {}
        """.format(latestUpdate['infected'],latestUpdate['recovered'],latestUpdate['deceased'])

        tt.tweetUpdate(message)