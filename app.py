import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
from dateutil.relativedelta import relativedelta

from utils import get_motivation, get_tweet, cleaning

st.title('Create Motivation Graph')

tw_id = st.sidebar.text_input('Input Tweeter ID')

if tw_id == '':
    st.warning("Input Tweeter ID")
    st.stop()

@st.cache(allow_output_mutation=True)
def create_motive_df(tw_id):
    get_tweet.create_tw_csv(tw_id)
    df = pd.read_csv('data/tweet.csv', encoding='utf8')
    # indexをdatetimeにする
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    motivation_df = get_motivation.day_motivation_df(df)
    return df, motivation_df

# motivation_df : index:datetime(日付のみ時間は9:00), score(total)
df, motivation_df = create_motive_df(tw_id)

@st.cache(allow_output_mutation=True)
def create_counter(df, motivation_df):
    # # dfからその日のツイートを取得
    count_df = pd.DataFrame({'Timestamp':df.index, 'tweet':df.text})
    count_df['date'] = count_df['Timestamp'].apply(lambda x: '%d-%d-%d' % (x.year, x.month, x.day))
    count_df = count_df.reset_index(drop=True)
    # 日毎のツイート数
    counter = count_df.groupby(['date']).size() # Series
    date_list = list(map(lambda x: '%d-%d-%d' % (x.year, x.month, x.day), motivation_df.index.tolist()))
    motivation_df['date'] = date_list
    return counter, motivation_df

counter, motivation_df = create_counter(df, motivation_df)

# 可視化範囲指定
until = datetime.now()
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
# layout = go.Layout(yaxis=dict(range=[-1,1]), tickformat="%Y-%m-%d")

fig = go.Figure(data=trace0)

fig.update_layout(
            title = dict(text = 'motivation graph'),
            xaxis = dict(title = 'date', type='date', dtick = dtick, tickformat="%Y-%m-%d"),  # dtick: 'M1'で１ヶ月ごとにラベル表示
            yaxis = dict(title = 'motivation score', range=[-1,1]),
            width=1000,
            height = 500
            )

st.plotly_chart(fig)

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
        return emoji_dict['happy']

# 選択した日付のテキストを表示
d = st.sidebar.date_input('When Tweet',min_value=since, max_value=until)
st.write(f'{d}のツイート')
total = motivation_df[pd.to_datetime(motivation_df.date) == pd.to_datetime(d)].score.tolist()
st.write(f'Total_score:{round(total[0], 4)}')
st.write(f'Status:  {sentiment_emoji(total[0])}')
tweets = df[pd.to_datetime(df.index.date) == pd.to_datetime(d)]
tweets = tweets.reset_index(drop=True)
# ここのtextは前処理なしの文章(URLも含む) scoreを出す際はURL除いてる
st.table(tweets[['created_at', 'text', 'score']])