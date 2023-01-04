import tweepy
import pandas as pd
from config import *
from datetime import datetime

# We can add filtering functions here, after gathering all the tweet data necessary. 
# Filtering option might be to get a list of bearish keywords vs bullish keywords
# Self learning train:
# 1. Get list of all the words, store them in dictionary, along with the # of times they've been used.
# 2. Remove useless words and keys that have been used less than N times.
# 3. Have someone help you with the sentiment analysis:
#       - Classify the keywords into BEARISH, BULLISH, NONE
#       - After having enough sample size, we can now have a list of keywords that tell us the market sentiment based on these keywords.

def initialize(apikey, apisecret, accesstoken, accesstokensecret):
    auth = tweepy.OAuth1UserHandler(apikey, apisecret, accesstoken, accesstokensecret)
    api = tweepy.API(auth)
    return api

def getTimelineTweets(api: tweepy.API, count):
    return tweepy.Cursor(api.home_timeline, count=200, tweet_mode="extended").items(count)

def searchTweetByHashtag(api: tweepy.API, searchtag, count, result_type='mixed'):
    '''Search by hashtag. result_type can be mixed,popular or recent.'''
    return tweepy.Cursor(api.search_tweets, q=f"#{searchtag}", count=100, lang="en", result_type=result_type, tweet_mode="extended").items(count)

def searchTweetByUsername(api: tweepy.API, usertag, count, result_type='mixed'):
    '''Search by username. result_type can be mixed,popular or recent.'''
    return tweepy.Cursor(api.search_tweets, q=f"@{usertag}", count=100, lang="en", result_type=result_type, tweet_mode="extended").items(count)

def getTweetsOfUser(api: tweepy.API, username,count):
    return tweepy.Cursor(api.user_timeline, screen_name=username, count=200, tweet_mode="extended").items(count)

def toDataFrame(tweet_sample):
    columns = ['username','datetime','tweet']
    data = []
    for tweet in tweet_sample:
        data.append([tweet.user.screen_name,tweet.created_at,tweet.full_text])
    return pd.DataFrame(data, columns=columns)

def streamByKeywords(bearertoken, keywords):
    '''Gets live tweets based on keywords. Keywords is a list (e.g. ["#ETH","#BTC"]'''
    class Listener(tweepy.StreamingClient):
        def on_connect(self):
            print("Connected.")
        def on_tweet(self, tweet):
            print(tweet.text)
    streamer = Listener(bearertoken)
    for rule in streamer.get_rules()[0]:
        streamer.delete_rules(rule.id)
    for word in keywords:
        streamer.add_rules(tweepy.StreamRule(word))
    streamer.filter()

if __name__ == '__main__':
    api = initialize(APIKEY, APISECRET, ACCESSTOKEN, ACCESSTOKENSECRET)
    #search_sample = searchTweetByUsername(api, "Kwebbelkop", 100)
    #df = toDataFrame(search_sample)
    #print(df)
    #df.to_csv("out.csv")
    #streamByKeywords(BEARERTOKEN,["#BTC","#ETH"])
