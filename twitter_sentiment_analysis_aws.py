import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from collections import Counter
import unicodedata
import re
import json
import nltk
from pymongo import MongoClient

# aws module python
import boto3

# custom data structure to count words
# from trie import *

credentials = {}
with open('secrets.json') as json_file:
    credentials = json.load(json_file)

# trie = Trie()
all_words = []
stopwords = nltk.corpus.stopwords.words('portuguese')


# mongo connection
# Connection
client = MongoClient('mongodb://hack123:hack123@ds057944.mlab.com:57944/hack_globo')

db = client['hack_globo']

# Creating db
tweets = db.tweets
words = db.words

class TwitterClient(object):

    def __init__(self):

        # keys and tokens from the Twitter Dev Console
        consumer_key = credentials["twitter_consumer_key"]
        consumer_secret = credentials["twitter_consumer_secret"]
        access_token = credentials["twitter_access_token"]
        access_token_secret = credentials["twitter_access_token_secret"]

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")
    # retorna sentimento da frase classificado pela aws
    def detect_sentiment(self,text):
        comprehend = boto3.client(
            'comprehend',
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key'],region_name=credentials['aws_region'])

        return comprehend.detect_sentiment(Text=text, LanguageCode='pt')['Sentiment']

    def get_tweets(self, query, count = 10):

        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.detect_sentiment(tweet.text)
                sem_acento = (''.join(ch for ch in unicodedata.normalize('NFKD', tweet.text) if not unicodedata.combining(ch)))

                minusculo = re.sub(r"[^a-zA-Z0-9]+", ' ', sem_acento.lower())
                # saving sentiment of tweet
                for word in minusculo.split(' '):
                    all_words.append(word)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()

    # calling function to get tweets
    tweets = api.get_tweets(query = '(sétimo guardião) OR (Sétimo Guardião) OR (setimo guardiao) OR (setimoguardiao)', count = 50)

    tweet_words = [x for x in all_words if x not in stopwords]

    # inserting results on mongodb
    db.tweets.insert_many(tweets)
    words = [{'name':key, 'value':value} for key,value in Counter(tweet_words).items()]
    db.words.insert_many(words)

if __name__ == "__main__":
    # calling main function
    main()
