#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API
access_token = "2752976021-8rJUndwyC8ht3Wgo7pMkeKiUMtadBdywMCBBClQ"
access_token_secret = "TOJfMSjFdWGX4CLxdtwB2jSopNEejCwMb9MY8txpn8BQv"
consumer_key = "n9AZKcRscz8XaXePL96YOQotN"
consumer_secret = "mAzTYTPfYAoFKj8CskcfbKxVkZv2bOwohZ3QkmyAFY0TCgSjYv"

drug_list = ['hcl','humira','aspirin','sodium']
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=drug_list)