import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from asari.api import Sonar

from utils import get_motivation, get_tweet, cleaning

st.title('Create Motivation Graph')

tw_id = st.sidebar.text_input('Input Tweeter ID')
st.write('PROGRESS BAR')
percentage = st.empty()
progress_bar = st.progress(0)
if tw_id == '':
    st.warning("Input Tweeter ID")
    st.stop()

@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def get_tweet_df(tw_id):
    with st.spinner('Downloading Tweets...'):
        tweet_df, message = get_tweet.create_tw_df(tw_id)
    if message != 'Success':
        st.warning(message)
        st.stop()
    st.success("Finish!")
    # indexをdatetimeにする
    tweet_df['date'] = pd.to_datetime(tweet_df['date'])
    tweet_df.set_index('date', inplace=True)
    tweet_df['clean_text'] = tweet_df['text'].map(cleaning.format_text)
    tweet_df['clean_text'] = tweet_df['clean_text'].map(cleaning.normalize)
    return tweet_df

@st.cache(suppress_st_warning=True)
def get_sentiment_scores(text_list):
    sonar = Sonar()
    with st.spinner('Wait for Scoring...'):
        response_list = list(map(sonar.ping, text_list))
    st.success('Done!')
    sentiment_scores = []
    total = len(text_list)
    count = 0
    for res in response_list:
        if res['text'] == ' ': #空白にもスコアが追加されてしまうため
            sentiment_scores.append(0)
            count += 1
            continue

        label = res['top_class']
        if label == 'negative':
            index = 0
            score = round(-1 * (res['classes'][index]['confidence']), 4)
        else:
            index = 1
            score = round(res['classes'][index]['confidence'], 4)
        sentiment_scores.append(score)

        # 四捨五入する
        count += 1
        percent = round((count/total) * 100)
        percentage.text(f'Progress: {percent}%')
        progress_bar.progress(percent)
        time.sleep(0.001)

    print('total:', total)
    print('count:', count)
    return sentiment_scores

@st.cache(allow_output_mutation=True)
def create_motivation_df(tweet_df, score_list):
    copy_tweet_df = tweet_df.copy()
    motivation_df = copy_tweet_df.resample("1D").mean()
    return motivation_df

tweet_df = get_tweet_df(tw_id)
sentiment_scores = get_sentiment_scores(tweet_df['clean_text'].tolist())
tweet_df['score'] = sentiment_scores

# motivation_df : index:datetime(日付のみ時間は9:00), score(total)
motivation_df = create_motivation_df(tweet_df, sentiment_scores) # indexの日付は正しい

@st.cache(allow_output_mutation=True)
def create_counter(tweet_df, motivation_df):
    # dfからその日のツイートを取得
    count_df = pd.DataFrame({'Timestamp':tweet_df.index, 'tweet':tweet_df.text})
    count_df['date'] = count_df['Timestamp'].apply(lambda x: '%d-%d-%d' % (x.year, x.month, x.day))
    count_df = count_df.reset_index(drop=True)
    # 日毎のツイート数
    counter = count_df.groupby(['date']).size() # Series
    date_list = list(map(lambda x: '%d-%d-%d' % (x.year, x.month, x.day), motivation_df.index.tolist()))
    motivation_df['date'] = date_list
    return counter, motivation_df

counter, motivation_df = create_counter(tweet_df, motivation_df)

# 可視化範囲指定
until = datetime.now() + timedelta(hours=9)
since = until - relativedelta(years=1)
date_range = st.sidebar.date_input("date range of tweet",
                                    value= [until - relativedelta(days=7), until],
                                    min_value=since, max_value=until)
if len(date_range) < 2:
    st.warning('Select 2 days from sidebar')
    st.stop()

date_span = (date_range[1] - date_range[0]).days
if date_span <= 31:
    dtick = '1D'
elif 31 < date_span <= 60:
    dtick = 3 * 86400000.0
elif 60 < date_span < 120:
    dtick = 7 * 86400000.0
else:
    dtick = '1M'

# 可視化
x_coord = motivation_df.loc[date_range[0]:date_range[1], :].index.tolist()
y_coord = motivation_df.loc[date_range[0]:date_range[1], :].score.values.tolist()

trace0 = go.Scatter(x = x_coord, y = y_coord, mode = 'lines + markers', name = 'X')

fig = go.Figure(data=trace0)

fig.update_layout(
            title = dict(text = 'motivation graph'),
            xaxis = dict(title = 'date', type='date', dtick = dtick, tickformat="%Y-%m-%d"),  # dtick: 'M1'で１ヶ月ごとにラベル表示
            yaxis = dict(title = 'motivation score', range=[-1,1]),
            )

st.plotly_chart(fig , use_container_width=True)

emoji_dict = {'painful':'😭', 'sad':'😢', 'pien': '🥺', 'usual':'😃', 'joy': '😁', 'exciting': '😆', 'happy':'✌😎✌️'}
def sentiment_emoji(score):
    if -1 <= score < -0.7:
        return emoji_dict['painful']
    elif -0.7 <= score < -0.4:
        return emoji_dict['sad']
    elif -0.4 <= score < -0.2:
        return emoji_dict['pien']
    elif -0.2 <= score < 0.2:
        return emoji_dict['usual']
    elif 0.2 <= score < 0.4:
        return emoji_dict['joy']
    elif 0.4 <= score < 0.7:
        return emoji_dict['exciting']
    else:
        st.balloons()
        return emoji_dict['happy']

# 選択した日付のテキストを表示
select_date = st.sidebar.date_input('When Tweet', value=until, min_value=since, max_value=until)
st.write(f'{select_date}のツイート')
total_score = motivation_df[pd.to_datetime(motivation_df.date) == pd.to_datetime(select_date)].score.tolist()
st.write(f'Total_score:{round(total_score[0], 4)}')
st.write(f'Status:  {sentiment_emoji(total_score[0])}')

tweets = tweet_df[pd.to_datetime(tweet_df.index.date) == pd.to_datetime(select_date)]
tweets = tweets.reset_index(drop=True)
# ここのtextは前処理なしの文章(URLも含む) scoreを出す際はURL除いてる
st.table(tweets[['created_at', 'text', 'score']])
