import tweepy
from tweepy import OAuthHandler
from harkFAIR.Core import DICT, FILE, DATE
import random

from FLog.LOGGER import Log
Log = Log("Server.Twitter.Tweeter")

# -> @GlewMeTv Setup
glewme_api_key = "Ugb7vMyOb7JFq0Zb7kJKfLQET"
glewme_api_key_secret = "0qYqejLwQIRH4nTV3YmyhjA5dJJ61w09YgGeQG5JMTDhZrakn4"
# glewme_bearer_token = "AAAAAAAAAAAAAAAAAAAAAJOxZgEAAAAA1FcR2jxPdFozhgmqAW2P41%2BtNss%3DIxK10p3nhJ5UkkjQ7G8rmutFK5T0W5N0WKiIJVEIuZ3d5RlGOV"
glewme_access_token = "1452531683463516162-m2PWaOfxnhYdTblfRT3Q8c3YGvTest"
glewme_access_token_secret = "AMt0U9bLmMUUhMVO4JZFFYyU6Vud7bGANXLeJfQ43Obix"
# glewme_client_id = "Y0hVOFN2NXdZbHhiOGpxb2hjSTg6MTpjaQ"
# glewme_client_secret = "nS5z1t88nBJc8m9jyUEWiiTxu-znxraVcd3Asc5GsR6zGoFriF"

# -> TEST ACCOUNT @ChazzCoin
# chazzcoin_api_key = "8w4H21qWCMrKlX3GuFEIZnn1E"
# chazzcoin_api_key_secret = "JOfIJtBzndaEv7sFWi4YeORhmTa16TLCEqwEt8ZB25P879pBNV"
# chazzcoin_access_token = "1296143087815860224-d6Bl838Yge6svvWEs7meBf4lNYpXAJ"
# chazzcoin_access_token_secret = "hIaye2CblbugGnXvXoc7Dz54t6HhKMZ6Q6nrM4583HJ9t"

import os
current = os.getcwd()

data_path = f"{current}/harkDataProvider"
glewme_hashtags = "#MetaverseDaily #TiffanyReport #news"

def getAuth():
    """-> CORE OBJECT <-"""
    # attempt authentication
    try:
        # create OAuthHandler object
        auth = OAuthHandler(glewme_api_key, glewme_api_key_secret)
        # set access token and secret
        auth.set_access_token(glewme_access_token, glewme_access_token_secret)
        # create tweepy API object to fetch tweets
        return tweepy.API(auth)
    except Exception as e:
        Log.e("Error: Authentication Failed", error=e)
        return False

def sendTweet(message):
    """-> CORE SEND FUNCTION <-"""
    api = getAuth()
    api.update_status(message)

def sendHookupTweet(hookup):
    title = DICT.get("title", hookup)
    if hasBeenSent(title):
        return
    category = DICT.get("category", hookup)
    url = DICT.get("url", hookup)
    message = f"{glewme_hashtags} #{category}\n-> {title}\n\n{url}"
    sendTweet(message)

def sendCachedHookup():
    Log.i("Sending Cached Hookup.")
    cache = loadTweetsInCache()
    keys = list(cache.keys())
    count = len(keys)
    ran = random.randint(0, count)
    key = list(cache.keys())[ran]
    tweet = cache[key]
    sendHookupTweet(tweet)
    removeTweetFromCache(key, cache)
    addTweetToSentCache(tweet)
    print(tweet)

def removeTweetFromCache(key, cache):
    newCache = DICT.removeKeyValue(key, cache)
    FILE.save_dict_to_file("hookup_tweets", newCache, data_path)

def addTweetToSentCache(sentTweet):
    Log.i("Adding tweet to sent list file.")
    date = str(DATE.get_log_date_time())
    oldTweets = loadSentTweetsInCache()
    oldTweets[date] = sentTweet
    FILE.save_dict_to_file("hookup_tweets_sent", oldTweets, data_path)

def addHookupsToCache(hookups):
    if len(hookups) > 50:
        hookups = hookups[:50]
    for hookup in hookups:
        source = DICT.get("source", hookup)
        score = DICT.get("score", hookup)
        if str(source).__contains__("investopedia"):
            continue
        elif int(score) < 500:
            continue
        addHookupToCache(hookup)

def addHookupToCache(hookup):
    """ """
    newTweet = convertHookupToTweet(hookup)
    newDate = str(DATE.get_log_date_time())
    tweets = FILE.load_dict_from_file("hookup_tweets", data_path)
    newTitle = DICT.get("title", newTweet)
    if hasBeenSent(newTitle):
        return
    tweets[newDate] = newTweet
    FILE.save_dict_to_file("hookup_tweets", tweets, data_path)

def hasBeenSent(newTitle):
    old_tweets = FILE.load_dict_from_file("hookup_tweets_sent", data_path)
    for oldKey in old_tweets.keys():
        oldItem = old_tweets[oldKey]
        oldTitle = DICT.get("title", oldItem)
        if oldTitle == newTitle:
            Log.i("Hookup has been Tweeted Previously. Avoiding.")
            return True
    return False

def convertHookupToTweet(hookup):
    Log.i("Converting Hookup for Tweet.")
    return {
        "title": DICT.get("title", hookup),
        "category": DICT.get("category", hookup),
        "url": DICT.get("url", hookup)
    }

def loadTweetsInCache():
    """ """
    Log.i("Loading Cached Tweets.")
    return FILE.load_dict_from_file("hookup_tweets", data_path)

def loadSentTweetsInCache():
    """ """
    Log.i("Loading Cached Sent Tweets.")
    return FILE.load_dict_from_file("hookup_tweets_sent", data_path)


if __name__ == '__main__':
    sendCachedHookup()