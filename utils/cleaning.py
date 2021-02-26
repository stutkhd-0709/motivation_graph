import re
import unicodedata
import pandas as pd
import emoji

def format_text(text):
    if pd.isnull(text):
        text = ' '
    else:
        text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
        text=re.sub(r'[!-~]', "", text)#半角記号,数字,英字
        text=re.sub(r'[︰-＠]', "", text)#全角記号
        text=re.sub('\n', " ", text)#改行文字
        # 絵文字削除
        text = ''.join(['' if c in emoji.UNICODE_EMOJI['en'] else c for c in list(text)])
    return text

def normalize(text):
    text = text.lower()
    text = unicodedata.normalize('NFKC', text)

    return text

def date_format(date):
    format ='%d-%d-%d' % (date.year, date.month, date.day)
    return format

x_coood = motivation_df.loc[date_range[0]:date_range[1], :].index.tolist()
y_coord = motivation_df.loc[date_range[0]:date_range[1], ['score']]values.tolist()