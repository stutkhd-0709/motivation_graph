import tweepy
import pandas as pd
import datetime
import os

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

#tweepyの設定
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

columns_name=["TW_NO","TW_TIME","TW_TEXT","RT","FAV"]

#ここで取得したいツイッターアカウントIDを指定する
tw_id="Taka_input"

#ツイート取得
def get_tweets():
    tweet_data = []

    for tweet in tweepy.Cursor(api.user_timeline,screen_name = tw_id,exclude_replies = True).items():
        tweet_data.append([tweet.id,tweet.created_at,tweet.created_at+datetime.timedelta(hours=9),tweet.text.replace('\n',''),tweet.favorite_count,tweet.retweet_count])

    df = pd.DataFrame(tweet_data,columns=columns_name)
    df.to_excel('tw_%s.xlsx'%tw_id, sheet_name='Sheet1')
    print("end")

get_tweets()