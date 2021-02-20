import oseti
import pandas as pd
import cleaning

# analyzer = oseti.Analyzer()
# print(analyzer.analyze('今日は疲れました。'))
# print(analyzer.analyze('遅刻したけど楽しかったし嬉しかった。すごく充実した！'))
# print(analyzer.analyze('遅刻したけど楽しかったし嬉しかった。すごく充実した！'))
df = pd.read_csv('data/tweet.csv', encoding='utf8')
df['clean_text'] = df['text'].map(cleaning.format_text)
df['clean_text'] = df['text'].map(cleaning.normalize)

def motivation_score(text):
    analyzer = oseti.Analyzer()
    score_list = analyzer.analyze(text)
    return score_list[0]

# csvに新しくカラム追加する？
df['score'] = df['clean_text'].map(motivation_score)
# print(df.head())
# indexをdatetimeにする
df.index = pd.DatetimeIndex(pd.to_datetime(df['created_at'].map(lambda x: x[:10]), format="%Y-%m-%d"))
df.drop('created_at', axis=1, inplace=True)
# resample : データ集計
df_1day = df.resample("1D").sum()
print(df_1day)