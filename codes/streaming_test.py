#===============================================================
#@author: Sachin Saligram
#@description: This code is used for testing purposes.
#===============================================================

#Import from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, API
from tweepy import Stream
import json, tweepy, pymongo
from pymongo import MongoClient


#Variables that contains the user credentials to access Twitter API 
access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""


#This is a basic listener that just prints received tweets to stdout.
class streamListener(StreamListener):

    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

    def on_data(self, status):
        #if 'RT @' not in data.text:
        print(json.loads(status))

        client_mongo = MongoClient('localhost', 27017)
        db = client_mongo['dicdatabase']
        coll = db['diccoll']

        result = db.diccoll.insert_one(json.loads(status))
        print(result.inserted_id)

        print(db.diccoll.count())

        #    print()
            #print(status.text)
            #print(status._json)
        #    for hashtag in status.entities['hashtags']:
        #        print (hashtag)
        #        print()
        #        print('#'+hashtag['text'])

        

    def on_error(self, status):
        print status

if __name__ == '__main__':

    #This handles Twitter authetification 
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)

    # Create stream and bind the listener to it
    stream = Stream(auth, listener = streamListener(api))

    #This line filter Twitter Streams to capture data by the keywords
    stream.filter(languages=["en"], track=["#usopen", "#federer", "US Open", "Flushing Meadows", "Federer"])
