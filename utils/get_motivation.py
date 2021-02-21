import oseti
import pandas as pd
from . import cleaning

def motivation_score(text):
    analyzer = oseti.Analyzer()
    score_list = analyzer.analyze(text)
    return round(score_list[0], 4)

def day_motivation_df(df):
    df['clean_text'] = df['text'].map(cleaning.format_text)
    df['clean_text'] = df['text'].map(cleaning.normalize)
    df['score'] = df['clean_text'].map(motivation_score)
    # indexをdatetimeにする
    df.index = pd.DatetimeIndex(pd.to_datetime(df['created_at'].map(lambda x: x), format="%Y-%m-%d %H:%M:%S"))
    df.drop('created_at', axis=1, inplace=True)

    # resample : データ集計
    df_1day = df.resample("1D").sum()
    return df_1day