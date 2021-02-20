import streamlit as st
import pandas as pd
from utils import get_motivation, get_tweet
import plotly.graph_objs as go

st.title('Create Motivation Graph')

tw_id = st.sidebar.text_input('Twitter IDを入力してください')

if tw_id == '':
    st.warning("IDを入力してください")
    st.stop()
get_tweet.create_tw_csv(tw_id)
df = pd.read_csv('data/tweet.csv', encoding='utf8')
motivation_df = get_motivation.day_motivation_df(df)

# 可視化
x_coord = motivation_df.index.tolist()
y_coord = motivation_df.score.values.tolist()

trace0 = go.Scatter(x = x_coord, y = y_coord, mode = 'lines', name = 'X')

layout = go.Layout(
            title = dict(text = 'motivation graph for a year'),
            xaxis = dict(title = 'date', type='date', dtick = 'M1'),  # dtick: 'M1'で１ヶ月ごとにラベル表示 
            yaxis = dict(title = 'motivation score'))

fig = go.Figure(data=trace0, layout=layout)
st.plotly_chart(fig)