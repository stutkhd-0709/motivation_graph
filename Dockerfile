FROM python:3.8

WORKDIR work

RUN git clone https://github.com/Jefferson-Henrique/GetOldTweets-python \
    && sed -i -e '59s/usernameTweet/re.split("\/", permalink)[1]/g' GetOldTweets-python/got3/manager/TweetManager.py \
    && mv GetOldTweets-python/got3 /usr/local/lib/python3.8/site-packages \
    && rm -rf GetOldTweets-python

RUN pip install --upgrade pip \
    && pip install requests_oauthlib pyquery tweepy pandas
