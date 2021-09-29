# Motivation Graph
Tweetから1年以内のあなたのモチベーションを可視化します。

# 説明
自己分析の一種, モチベーショングラフをTweetをもとに作成するために作りました。  
1年以内の期間を選択することで、その期間のモチベーショングラフを可視化することができます。  
また、選択した日付のツイートとそのツイートのモチベーションスコアも一覧で見ることができます。  
感情分析のスコアリングがボトルネックになっており、ツイートによってはかなり遅いです。  

# Deploy Link
https://share.streamlit.io/stutkhd/motivation_graph/app.py  
(streamlit deployのシステム上でgit cloneできないためneologdは使用してない)

# Requirements
 - python==3.7
 - mecab-python3==0.7
 - streamlit==0.89.0
 - pandas==1.2.2
 - plotly==4.14.3
 - requests_oauthlib==1.3.0
 - pyquery==1.4.3
 - tweepy==3.10.0
 - asari==0.0.4
 - janome == 0.3.7
 - scikit-learn==0.23.0
 - emoji==1.2.0
 - python-dotenv==0.16.0