import tweepy
import pandas as pd
import os
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

#tweepyの設定
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def datetime_format(date):
    format ='%d-%d-%d' % (date.year, date.month, date.day)
    return format

def daterange(_start, _end):
    for n in range((_end - _start).days):
        datetime = _start + timedelta(n)
        yield datetime_format(datetime)

def create_tw_csv(tw_id):
    # tweet_idにすると自分のタイムラインしか取得できない
    tweets = tweepy.Cursor(api.user_timeline, count=200, \
                       screen_name=tw_id, \
                       include_rts=False, \
                       exclude_replies = True,\
                       lang='ja').items()
    c = 0
    tweets_list, created_time_list = [], []
    until = datetime.now()
    since = until - relativedelta(years=1)
    try:
        for tw in tweets: # tweetsはgenerator
            created_at = tw.created_at + timedelta(hours=9)
            # 1年間のデータだけ取得
            if created_at < since:
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
        df['date'] = df['created_at'].apply(datetime_format)
        # indexを補完する
        lost_datetime = [] # datetime型
        tweets_date = set(df.date.tolist()) # 時間はなし
        for date in daterange(since, until):
            if date not in tweets_date:
                lost_datetime.append(pd.to_datetime(date))
        tmp_df = pd.DataFrame(lost_datetime, columns=['created_at'])
        tmp_df['date'] = tmp_df['created_at'].apply(datetime_format)
        df = pd.concat([df, tmp_df])
        df = df.sort_values('created_at')
        df.to_csv('data/tweet.csv', index=False)
        print(f'Total {c} tweets')
        return 'Success'
    except tweepy.error.TweepError as error:
        if '404' in str(error):
            return 'そのIDは存在しません'
        elif '401' in str(error):
            return 'アカウントに鍵がかかっています'