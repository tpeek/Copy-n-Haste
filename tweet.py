# -*- coding: utf-8 -*-
import tweepy
from tweepy.api import API

API_KEY = 'OxU59qSyfMzlseWHFBFiv2Hgq'
API_SECRET = 'hide'
ACCESS_TOKEN = '51948357-DAgrNVcLoZGW9SONcLYEoOwGd3lsoCdPSppEV3azw'
ACCESS_TOKEN_SECRET = 'rfWikqA5ZronG8hNHzFKsaZiiQzwyvs9YqCjoxfRJHK1L'
key = tweepy.OAuthHandler(API_KEY, API_SECRET)
key.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

class Stream2Screen(tweepy.StreamListener):
    def __init__(self, api=None):
        self.api = api or API()
        self.n = 0
        self.m = 20

    def on_status(self, status):
        print status.text.encode('utf8')
        self.n = self.n+1
        if self.n < self.m: return True
        else:
            print 'tweets = '+str(self.n)
            return False


class Stream2File(tweepy.StreamListener):
    def __init__(self, api=None):
        self.api = api or API()
        self.n = 0
        self.m = 20
        self.output = open('/Users/jameshemmaplardh/nltk_data/pytextos/tweepy_text.txt', 'w')

    def on_status(self, status):
        self.output.write(status.text.encode('utf8') + "\n")
        self.n = self.n+1
        if self.n < self.m: return True
        else:
            self.output.close()
            print 'tweets = '+str(self.n)
            return False

stream = tweepy.streaming.Stream(key, Stream2Screen())
stream.filter(track=['en'], languages=['en'])

