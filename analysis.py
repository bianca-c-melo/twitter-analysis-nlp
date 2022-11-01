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

# load csv
PATH = os.path.dirname(os.path.realpath(__file__))
df1 = pd.read_csv(PATH+"/tweets.csv")

# Remove stopwords


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

    # Normalizando o texto:
    text = (unicodedata.normalize('NFKD', text)
            .encode('ascii', 'ignore')
            .decode('utf-8', 'ignore')
            .lower())

    # Excluindo menções com @:
    text = re.sub('@[^\s]+', '', text)

    # Removendo o a query de pesquisa ja que ela ja foi usada para pesquisar os tópicos
    text = re.sub('diversidade', '', text)

    # Excluindo tags html:
    text = re.sub('<[^<]+?>', '', text)

    # Excluindo os números:
    text = ''.join(x for x in text if not x.isdigit())

    # Excluindo URL's:
    text = re.sub(
        '((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))', '', text)

    # Excluindo pontuação:
    text = ''.join(x for x in text if x not in punctuation)

    return word_tokenize(text)


df1['text'] = df1['text'].apply(
    lambda text: limpar_texto(text))


def generate_ngrams(file, size):
    ngrams_all = []
    for file in file:
        output = list(nltk.ngrams(file, size))
        for ngram in output:
            ngrams_all.append(" ".join(ngram))
    count_ngram = Counter()
    for word in ngrams_all:
        count_ngram[word] += 1
    df = pd.DataFrame.from_dict(count_ngram, orient='index').reset_index()
    df = df.rename(columns={'index': 'words', 0: 'count'})
    df = df.sort_values(by='count', ascending=False).reset_index(drop=True)
    df = df.head(15)
    return df


uni_grams = generate_ngrams(df1['text'], 1)
bi_grams = generate_ngrams(df1['text'], 2)
tri_grams = generate_ngrams(df1['text'], 3)


