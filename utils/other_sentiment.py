import oseti

def oseti_motivation_score(text):
    analyzer = oseti.Analyzer()
    score_list = analyzer.analyze(text)
    return round(score_list[0], 4)

def bert_motivation_score(text_list):
    from transformers import pipeline, AutoModelForSequenceClassification, BertJapaneseTokenizer
    model = AutoModelForSequenceClassification.from_pretrained('daigo/bert-base-japanese-sentiment')
    tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
    nlp = pipeline("sentiment-analysis",model=model,tokenizer=tokenizer)
    scores = []
    for text in text_list:
        if text == ' ':
            scores.append(0)
            continue
        result = nlp(text)[0]
        if result['label'] == 'ネガティブ':
            score = round(-1 * result['score'], 4)
        else:
            score = round(result['score'], 4)
        scores.append(score)
    return scores