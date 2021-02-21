import oseti
import pandas as pd
from . import cleaning

def oseti_motivation_score(text):
    analyzer = oseti.Analyzer()
    score_list = analyzer.analyze(text)
    return round(score_list[0], 4)

def asari_motivation_score(text_list):
    from asari.api import Sonar
    sonar = Sonar()
    # res = sonar.ping(text=text)
    # label = res['top_class']
    A = list(map(sonar.ping, text_list))
    scores = []
    for res in A:
        label = res['top_class']
        if label == 'negative':
            index = 0
            score = round(-1 * (res['classes'][index]['confidence']), 4)
        else:
            index = 1
            score = round(res['classes'][index]['confidence'], 4)
        scores.append(score)
        print(res)
    return scores

def day_motivation_df(df):
    df['clean_text'] = df['text'].map(cleaning.format_text)
    df['clean_text'] = df['text'].map(cleaning.normalize)
    # df['score'] = df['clean_text'].map(oseti_motivation_score)
    text_list = asari_motivation_score(df['clean_text'].tolist())
    df['score'] = text_list
    # indexをdatetimeにする
    df.index = pd.DatetimeIndex(pd.to_datetime(df['created_at'].map(lambda x: x), format="%Y-%m-%d %H:%M:%S"))
    df.drop('created_at', axis=1, inplace=True)
    # resample : データ集計
    df_1day = df.resample("1D").sum()
    return df_1day