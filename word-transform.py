import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models import KeyedVectors, Word2Vec
from gensim.models.wrappers import FastText
import gensim.models.wrappers.fasttext
import nltk
import string
import io

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


nltk.download('stopwords')
nltk.download('punkt')

# Max length for titles after process is 13. Input in LSTM should consist of 13xn input, where n is timesteps.
df = pd.read_csv('~/datasets/fixed_data.csv', delimiter='\t')

stop_words = set(stopwords.words('english'))

model = Word2Vec.load("mashable-titles-word2vec.model")

def clean_text(text):
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]

    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    words = [word for word in stripped if word.isalpha()]
    words = [w for w in words if not w in stop_words]

    #stemmed = [porter.stem(word) for word in words]

    return words

total_unknown = 0
total_known = 0
def transform_words(text):
    global total_unknown
    global total_known

    vector = []

    for word in text:
        try:
            numeric_word = model.wv[word]
            vector.append(numeric_word)
            total_known += 1
        except:
            total_unknown += 1

    vector_len = 13-len(vector)
    for i in range(vector_len):
        vector.append(np.zeros((100,)))

    return vector

df_processed = df
print("START CLEANING TITLES")
df_processed['title_tokenized'] = df['title'].apply(lambda x: clean_text(x))
print("DONE CLEANING TITLES")


print("TRANSFORMING TITLES")
df_processed['title_word_vectors'] = df_processed['title_tokenized'].apply(lambda x: transform_words(x))
print("TRANSFORMING TITLES DONE")

print("Word ratio:", total_known/(total_known+total_unknown), total_unknown/(total_known+total_unknown))

print(df_processed.head())

df_processed.drop(['author'], inplace=True, axis=1)
df_processed.drop(['time_of_post'], inplace=True, axis=1)
df_processed.drop(['content'], inplace=True, axis=1)

print(df_processed.head())

df_processed.to_csv('processed-data-title-url-only.csv', index=False, header=True)
