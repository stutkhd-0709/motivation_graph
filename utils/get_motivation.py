import oseti
from asari.api import Sonar
import pandas as pd
from . import cleaning

def oseti_motivation_score(text):
    analyzer = oseti.Analyzer()
    score_list = analyzer.analyze(text)
    return round(score_list[0], 4)

def asari_motivation_score(text_list):
    sonar = Sonar()
    A = list(map(sonar.ping, text_list))
    scores = []
    for res in A:
        if res['text'] == ' ': #空白にもスコアが追加されてしまうため
            scores.append(0)
            continue
        label = res['top_class']
        if label == 'negative':
            index = 0
            score = round(-1 * (res['classes'][index]['confidence']), 4)
        else:
            index = 1
            score = round(res['classes'][index]['confidence'], 4)
        scores.append(score)
    return scores

def day_motivation_df(df):
    df['clean_text'] = df['text'].map(cleaning.format_text) #前後の値が違う
    df['clean_text'] = df['clean_text'].map(cleaning.normalize)
    # df['score'] = df['clean_text'].map(oseti_motivation_score)
    text_list = asari_motivation_score(df['clean_text'].tolist())
    df['score'] = text_list
    df_1day = df.resample("1D").mean()
    return df_1day