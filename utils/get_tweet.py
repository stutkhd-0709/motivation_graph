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

# #ここで取得したいツイッターアカウントIDを指定する
# tw_id="Taka_input"

# # 検索文字
# search_word = 'tweet_id:@' + tw_id + ' exclude:retweets exclude:replies'
# print('Searching:', search_word)

# tweets = tweepy.Cursor(api.user_timeline, count=200, \
#                        user_id=tw_id, \
#                        include_rts=False, \
#                        exclude_replies = True,\
#                        lang='ja').items()

# c = 0
# tweets_list, created_time_list = [], []
# until = datetime.now()
# since = until - relativedelta(years=1)
# for tw in tweets: # tweetsはgenerator
#     created_at = tw.created_at + timedelta(hours=9)
#     # 1年間のデータだけ取得
#     if created_at < since:
#         break
#     # urlがある場合は除く(共有ツイートが多いため) 画像は含まれない
#     if tw.entities['urls']:
#         continue
#     created_time_list.append(created_at)
#     tweets_list.append(tw.text)
#     if c % 100 == 0:
#         print(f'{c} Tweets Done')
#     c += 1
# print(f'Total {c} Tweets')

# df = pd.DataFrame(data={'text':tweets_list, 'created_at':created_time_list})
# df.to_csv('data/tweet.csv', index=False)
# print('Successfully saved tweet.csv')

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
        df.to_csv('data/tweet.csv', index=False)
        print(f'Total {c} tweets')
        return 'Success'
    except tweepy.error.TweepError:
        print('error was happend')
        return 'そのIDは存在しません'