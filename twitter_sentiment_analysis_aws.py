import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import json
# from tfidf import *

# aws module python
import boto3

# full_tweets = []
credentials = {}
with open('secrets.json') as json_file:
    credentials = json.load(json_file)


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
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.detect_sentiment(tweet.text)
                # full_tweets.append(TextBlob(tweet.text))

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
    tweets = api.get_tweets(query = 'bolsonaro', count = 20)

    # for i, blob in enumerate(full_tweets):
    #     print("Top words in document {}".format(i + 1))
    #     scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
    #     sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    # for word, score in sorted_words[:3]:
    #     print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

if __name__ == "__main__":
    # calling main function
    main()
