import re
import os
import pandas as pd
import unicodedata
import nltk
from collections import Counter
from nltk import word_tokenize
from string import punctuation
nltk.download('punkt')
nltk.download('stopwords')


# load csv
PATH = os.path.dirname(os.path.realpath(__file__))
tweets = pd.read_csv(PATH+"/tweets.csv")

# Remove stopwords


def remove_stop_words(x):
    stopwords_add = ['oi', 'bom dia', 'e', 'pra', 'hj', 'hoje', 'hj,', 'porém', 'apesar', 'não', 'desta', 'q', 'e',
                     'bem', 'deu', 'que', 'foi', 'vai', 'muita', 'aí', 'ai', 'ao', 'o', 'a', 'assim', 'né', 'uma',
                     'sim', 'ué', 'quer', 'é', 'quanto', 'sobre', 'dia']
    stop_w = nltk.corpus.stopwords.words('portuguese')
    stop_w.extend(stopwords_add)

    x = [word for word in x.lower().split() if word not in stop_w]
    return ' '.join(x)


tweets['text'] = tweets['text'].apply(
    lambda x: remove_stop_words(x))


def limpar_texto(text):

    # Normalizando o texto:
    text = (unicodedata.normalize('NFKD', text)
            .encode('ascii', 'ignore')
            .decode('utf-8', 'ignore')
            .lower())

    # Excluindo menções com @:
    text = re.sub('@[^\s]+', '', text)

    # Removendo a query de pesquisa ja que ela ja foi usada para pesquisar os tópicos e ficaria redundante
    # nos resultados
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

    # tokenizar o texto:
    text = word_tokenize(text)

    return text


tweets['text'] = tweets['text'].apply(
    lambda text: limpar_texto(text))


def generate_ngrams(file, size):
    array = []
    for file in file:
        output = list(nltk.ngrams(file, size))
        for ngram in output:
            array.append(" ".join(ngram))
    count_ngram = Counter()
    for word in array:
        count_ngram[word] += 1
    n_grams = pd.DataFrame.from_dict(count_ngram, orient='index').reset_index()
    n_grams = n_grams.rename(columns={'index': 'palavras', 0: 'contagem'})
    n_grams = n_grams.sort_values(by='contagem', ascending=False).reset_index(drop=True)
    n_grams = n_grams.head(15)
    return n_grams


uni_grams = generate_ngrams(tweets['text'], 1)
bi_grams = generate_ngrams(tweets['text'], 2)
tri_grams = generate_ngrams(tweets['text'], 3)


