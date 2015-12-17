import os
# import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itcadre.settings")
from django.conf import settings
# from spike import spike_defaults

# from spike import models
import datetime


#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from spike.models import DataRecord
from spike.services import retreive_drug_names
#Variables that contains the user credentials to access Twitter API
access_token = "2752976021-8rJUndwyC8ht3Wgo7pMkeKiUMtadBdywMCBBClQ"
access_token_secret = "TOJfMSjFdWGX4CLxdtwB2jSopNEejCwMb9MY8txpn8BQv"
consumer_key = "n9AZKcRscz8XaXePL96YOQotN"
consumer_secret = "mAzTYTPfYAoFKj8CskcfbKxVkZv2bOwohZ3QkmyAFY0TCgSjYv"

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        # print(data)
        if "text" in data and "source" in data :
            tweet = data.split(',"text":"')[1].split('","source')[0]
            today = datetime.datetime.today()
            try:
                d = DataRecord(raw_data=tweet, data_src='twitter', submitted_date=today)
                d.save()
            except:
                print(" this message "+tweet+"  skipped")
            # print(tweet)
            # print('data saved')
        else:
            print('bad data')
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    drugs = retreive_drug_names(5)

    mydrugs = []
    for result in drugs["results"]:
        mydrugs.append(result["term"])


    # settings.configure(default_settings=spike_defaults, DEBUG=True)
    # django.setup()
    # settings.configure()
    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=mydrugs)