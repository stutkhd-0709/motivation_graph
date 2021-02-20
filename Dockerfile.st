FROM python:3.7
USER root

EXPOSE 8501

WORKDIR /streamlit-docker

RUN apt-get update \
    && apt-get install -y mecab mecab-utils libmecab-dev \
    && pip install -U pip

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git /mecab-ipadic-neologd \
    && /mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -u -n -y -p /var/lib/mecab/dic/mecab-ipadic-neologd \
    && update-alternatives --install /var/lib/mecab/dic/debian mecab-dictionary /var/lib/mecab/dic/mecab-ipadic-neologd 100 \
    && rm -rf /mecab-ipadic-neologd

COPY requirements_st.txt /streamlit-docker

RUN pip install -r requirements_st.txt

CMD streamlit run app.py

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN mkdir -p /root/.streamlit
RUN bash -c 'echo -e "\
            [general]\n\
            email = \"\"\n\
            " > /root/.streamlit/credentials.toml'

RUN bash -c 'echo -e "\
            [server]\n\
            enableCORS = false\n\
            " > /root/.streamlit/config.toml'