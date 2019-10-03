import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim.models import KeyedVectors
from gensim.models.wrappers import FastText
import gensim.models.wrappers.fasttext
import nltk
import string
import io

def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in fin:
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
    return data

nltk.download('stopwords')
nltk.download('punkt')

# Max length for titles after process is 13. Input in LSTM should consist of 13 input
df = pd.read_csv('data.csv', delimiter='\t')

stop_words = set(stopwords.words('english'))
porter = PorterStemmer()

filename = 'glove.6B.50d.txt.word2vec'
#model = FastText.load_fasttext_format('crawl-300d-2M.vec')
print('LOADING WORD VECTOR MODEL...')
model = KeyedVectors.load_word2vec_format('G:\DATASETS\MODELS')
print('WORD VECTOR MODEL LOADED.')

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
def transform_words(text):
    global total_unknown

    vector = []

    for word in text:
        try:
            numeric_word = model.most_similar(word)
            vector.append(numeric_word)
        except:
            total_unknown += 1
            print(word, 'not found. Total unknown:', total_unknown)



    vector_len = 13-len(vector)
    for i in range(vector_len):
        vector.append(0)

    return vector


def print_max_and_min_titlelength():
    min_len = 100
    max_len = 0
    for i in range(len(df_processed)):
        length = len(df_processed[i])
        if length > max_len:
            max_len = length
        if length < min_len:
            min_len = length
    print(max_len)
    print(min_len)

df_processed = df
df_processed['title'] = df['title'].apply(lambda x: clean_text(x))

print(df_processed.head())

df_processed['title'] = df_processed['title'].apply(lambda x: transform_words(x))
df_processed.to_csv('processed-data.csv', index=False, header=True)

print(df_processed.head())


