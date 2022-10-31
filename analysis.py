import re
import spacy
from collections import Counter
import pandas as pd
from nltk import word_tokenize
from string import punctuation
import unicodedata
import nltk
import os
nltk.download('punkt')
nltk.download('stopwords')

nlp = spacy.load("pt_core_news_sm")

PATH = os.path.dirname(os.path.realpath(__file__))
df1 = pd.read_csv(PATH+"/tweets.csv")

# Filter the stopword
def remove_stop_words(x):
    stopwords_add = ['oi', 'bom dia', 'e', 'pra', 'hj', 'hoje', 'hj,', 'porém', 'apesar', 'não', 'desta', 'q', 'e',
                     'bem', 'deu', 'que', 'foi', 'vai', 'muita', 'aí', 'ai', 'ao', 'o', 'a', 'assim', 'né', 'uma',
                     'sim', 'ué', 'quer', 'é', 'quanto', 'sobre', 'dia']
    stop_w = nltk.corpus.stopwords.words('portuguese')
    stop_w.extend(stopwords_add)

    x = [word for word in x.lower().split() if word not in stop_w]
    return ' '.join(x)


df1['text'] = df1['text'].apply(
    lambda x: remove_stop_words(x))


def limpar_texto(text):

    # Colocando todas as letras do texto em caixa baixa:
    text = (unicodedata.normalize('NFKD', text)
            .encode('ascii', 'ignore')
            .decode('utf-8', 'ignore')
            .lower())
    # Excluindo citações com @:
    text = re.sub('@[^\s]+', '', text)
    # Excluindo html tags:
    text = re.sub('diversidade', '', text)

    text = re.sub('<[^<]+?>', '', text)
    # Excluindo os números:
    text = ''.join(c for c in text if not c.isdigit())
    # Excluindo URL's:
    text = re.sub(
        '((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', text)
    # Excluindo pontuação:
    text = ''.join(c for c in text if c not in punctuation)

    return word_tokenize(text)


df1['text'] = df1['text'].apply(
    lambda text: limpar_texto(text))


def countNgrams(file, size):
    ngrams_all = []
    for file in file:
        output = list(nltk.ngrams(file, size))
        for ngram in output:
            ngrams_all.append(" ".join(ngram))
    cnt_ngram = Counter()
    for word in ngrams_all:
        cnt_ngram[word] += 1
    df = pd.DataFrame.from_dict(cnt_ngram, orient='index').reset_index()
    df = df.rename(columns={'index': 'words', 0: 'count'})
    df = df.sort_values(by='count', ascending=False).reset_index(drop=True)
    df = df.head(15)
    return df


unigrams = countNgrams(df1['text'], 1)
bigrams = countNgrams(df1['text'], 2)
trigrams = countNgrams(df1['text'], 3)

print(bigrams)
print(unigrams)
print(trigrams)



# df1.to_csv(r'/Users/biancacamargodepaulamelo/PycharmProjects/pythonProject1/tweets_clean.csv', header=True)

