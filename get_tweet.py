import tweepy
import pandas as pd
import os

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

#tweepyの設定
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

columns_name=["TW_NO","TW_TIME","TW_TEXT","RT","FAV"]

#ここで取得したいツイッターアカウントIDを指定する
tw_id="Taka_input"

# 検索文字
search_word = '@' + tw_id + 'exclude:retweets'
print('検索単語:', search_word)

tweets = tweepy.Cursor(api.user_timeline, count=200, \
                       user_id=tw_id, \
                       include_rts=False, \
                       exclude_replies = False,\
                       lang='ja').items()

for tweet in enumerate(tweets):
    print('=================')
    print(tweet.text)
    print('date:', tweet.created_at)


