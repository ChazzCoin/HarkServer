import tweepy
from tweepy import OAuthHandler
from FSON import DICT
from FList import LIST
from FDate import DATE
from harkDataProvider import Provider
from Jarticle import jArticleProvider as jap
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

data_path = Provider.data_path
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

# -> Master Send
def sendTweet(message):
    """-> CORE SEND FUNCTION <-"""
    api = getAuth()
    api.update_status(message)

# -> Master Tweeter Function
def sendMetaverseArticle(depth: int):
    if depth >= 5:
        return False
    Log.i(f"Sending Cached Article. Depth=[ {depth} ]")
    tweet = get_metaverse_article()
    if postArticleToTwitter(tweet):
        addTweetToSentCache(tweet)
        print(tweet)
        return True
    return sendMetaverseArticle(depth+1)

# -> Attempt to Post Tweet
def postArticleToTwitter(article):
    if not article:
        return False
    title = DICT.get("title", article)
    if hasBeenSent(title):
        return False
    category = DICT.get("category", article, False)
    url = DICT.get("url", article, False)
    if not category or not url:
        return False
    message = f"{glewme_hashtags} #{category}\n-> {title}\n\n{url}"
    sendTweet(message)
    return True

# -> Get Random Metaverse Article
def get_metaverse_article():
    arts = jap.get_categories("metaverse")
    full_count = len(arts)
    random_index = random.randint(0, full_count)
    potential_art = LIST.get(random_index, arts, False)
    return potential_art

# -> Cache
def addTweetToSentCache(sentTweet):
    st = convertHookupToTweet(sentTweet)
    Log.i("Adding tweet to sent list file.")
    date = str(DATE.get_log_date_time_dt())
    oldTweets = loadSentTweetsInCache()
    oldTweets[date] = st
    Provider.save_dict_to_file("hookup_tweets_sent", oldTweets, data_path)

# -> Cache
def loadSentTweetsInCache():
    """ """
    Log.i("Loading Cached Sent Tweets.")
    return Provider.load_dict_from_file("hookup_tweets_sent", data_path)

# -> Helper
def hasBeenSent(newTitle):
    old_tweets = Provider.load_dict_from_file("hookup_tweets_sent", data_path)
    for oldKey in old_tweets.keys():
        oldItem = old_tweets[oldKey]
        oldTitle = DICT.get("title", oldItem)
        if oldTitle == newTitle:
            Log.i("Hookup has been Tweeted Previously. Avoiding.")
            return True
    return False

# -> Helper
def convertHookupToTweet(article):
    Log.i("Converting Hookup for Tweet.")
    return {
        "title": DICT.get("title", article),
        "category": DICT.get("category", article),
        "url": DICT.get("url", article)
    }

if __name__ == '__main__':
    sendMetaverseArticle(0)