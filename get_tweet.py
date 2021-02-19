import tweepy
import pandas as pd
import os
from datetime import timedelta

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
search_word = 'tweet_id:@' + tw_id + ' exclude:retweets exclude:replies'
print('Searching:', search_word)

tweets = tweepy.Cursor(api.user_timeline, count=200, \
                       user_id=tw_id, \
                       include_rts=False, \
                       exclude_replies = True,\
                       lang='ja').items()

tweets_list, created_time_list = [], []
c = 0
for i, tw in enumerate(tweets): # tweetsはgenerator
    if tw.entities['urls']: # urlがある場合は除く(共有ツイートが多いため) 画像は含まれない
        continue
    tweets_list.append(tw.text)
    created_at = tw.created_at + timedelta(hours=9)
    created_time_list.append(created_at)
    if i % 500 == 0:
        print(f'{i} Tweets Done')
    c = i
print(f'Total {c} Tweets')

df = pd.DataFrame(data={'text':tweets_list, 'created_at':created_time_list})
df.to_csv('data/tweet.csv')
print('Successfully saved tweet.csv')