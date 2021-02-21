import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from utils import get_motivation, get_tweet


st.title('Create Motivation Graph')

tw_id = st.sidebar.text_input('Input Tweeter ID')

if tw_id == '':
    st.warning("Input Tweeter ID")
    st.stop()

@st.cache(allow_output_mutation=True)
def create_motive_df(tw_id):
    get_tweet.create_tw_csv(tw_id)
    df = pd.read_csv('data/tweet.csv', encoding='utf8')
    motivation_df = get_motivation.day_motivation_df(df)
    return df, motivation_df

df, motivation_df = create_motive_df(tw_id)

@st.cache()
def change_df(df, motivation_df):
    # dfからその日のツイートを取得
    count_df = pd.DataFrame({'Timestamp':df.index, 'tweet':df.text})
    count_df['date'] = count_df['Timestamp'].apply(lambda x: '%d-%d-%d' % (x.year, x.month, x.day))
    counter = count_df.groupby(['date']).size() # Series
    date_list = list(map(lambda x: '%d-%d-%d' % (x.year, x.month, x.day), motivation_df.index.tolist()))
    motivation_df['date'] = date_list
    return counter, motivation_df

counter, motivation_df = change_df(df, motivation_df)

st.write('motivation_df')
st.table(motivation_df.tail())
for date, count in zip(counter.index,counter.values):
    series = motivation_df[motivation_df.date==date]
    score = series['score'].tolist()[0]
    mean_score = score / count
    index = motivation_df[motivation_df.date==date].index
    motivation_df.at[index, 'score'] = mean_score

st.write('motivation_df')
st.table(motivation_df.tail())

# 可視化
x_coord = motivation_df.index.tolist()
y_coord = motivation_df.score.values.tolist()

trace0 = go.Scatter(x = x_coord, y = y_coord, mode = 'lines', name = 'X')

fig = go.Figure(data=trace0)

fig.update_layout(
            title = dict(text = 'Anual motivation graph'),
            xaxis = dict(title = 'date', type='date', dtick = 'M1'),  # dtick: 'M1'で１ヶ月ごとにラベル表示
            yaxis = dict(title = 'motivation score'),
            )

st.plotly_chart(fig)

until = datetime.now()
since = until - relativedelta(years=1)
# 選択した日付のテキストを表示
d = st.sidebar.date_input('When Tweet',min_value=since, max_value=until)

st.write(f'{d}のツイート')
tweets = df[pd.to_datetime(df.index.date) == pd.to_datetime(d)]
st.table(tweets[['text', 'score']])