import tweepy
import pandas as pd
import os
from os.path import join, dirname
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from . import cleaning
import streamlit as st

# dotenv_path = '/streamlit-docker/.env' # 絶対パスじゃないとエラー出る
# load_dotenv(dotenv_path)

# CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
# CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
# ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
# ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')

CONSUMER_KEY = st.secrets['CONSUMER_KEY']
CONSUMER_SECRET = st.secrets['CONSUMER_SECRET']
ACCESS_TOKEN = st.secrets['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = st.secrets['ACCESS_TOKEN_SECRET']

#tweepyの設定
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def daterange(_start, _end):
    for n in range(((_end+timedelta(days=1)) - _start).days):
        if n == 366:
            break
        datetime = _start + timedelta(n)
        yield cleaning.date_format(datetime)

def create_tw_df(tw_id):
    # tweet_idにすると自分のタイムラインしか取得できない
    tweets = tweepy.Cursor(api.user_timeline, count=200, \
                       screen_name=tw_id, \
                       include_rts=False, \
                       exclude_replies = True,\
                       lang='ja').items()
    c = 0
    tweets_list, created_time_list = [], []
    until = datetime.now() + timedelta(hours=9) # 日本時刻に合わせる
    since = until - relativedelta(years=1)
    message = ''
    try:
        for tw in tweets: # tweetsはgenerator
            created_at = tw.created_at + timedelta(hours=9) # 日本時刻になっている
            # 1年間のデータだけ取得
            if created_at < since: # error
                break
            # urlがある場合は除く(共有ツイートが多いため) 画像は含まれない
            if tw.entities['urls']:
                continue
            created_time_list.append(created_at)
            tweets_list.append(tw.text)
            if c % 100 == 0:
                print(f'{c} Tweets Done')
            c += 1
        df = pd.DataFrame(data={'text':tweets_list, 'created_at':created_time_list})
        df['date'] = df['created_at'].apply(cleaning.date_format)
        # indexを補完する
        lost_datetime = [] # datetime型
        tweets_date = set(df.date.tolist()) # 時間はなし
        for date in daterange(since, until):
            if date not in tweets_date:
                lost_datetime.append(pd.to_datetime(date))
        tmp_df = pd.DataFrame(lost_datetime, columns=['created_at'])
        tmp_df['date'] = tmp_df['created_at'].apply(cleaning.date_format)
        df = pd.concat([df, tmp_df])
        df = df.sort_values('created_at')
        print(f'Total {c} tweets')
        # sort_valueすると、時間が9時間進む
        df['created_at'] = df['created_at'].apply(lambda x: x - timedelta(hours=9))
        message = 'Success'
        return df, message

    except tweepy.error.TweepError as error:
        if '404' in str(error):
            message = 'そのIDは存在しません'
            return 'error', message
        elif '401' in str(error):
            message = 'アカウントに鍵がかかっています'
            return 'error', message