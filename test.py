from nltk.corpus import PlaintextCorpusReader
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.decomposition import PCA
from matplotlib import pyplot as plt
import numpy as np
from gensim.models.wrappers import FastText
from nltk.stem.porter import PorterStemmer
from gensim.models import Word2Vec
import nltk
import string
import pickle

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

stop_words = set(stopwords.words('english'))


df = pd.read_csv('~/datasets/fixed_data.csv', delimiter='\t')
nltk.download('stopwords')
nltk.download('punkt')


def clean_text(text):
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]

    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]

    words = [word for word in stripped if word.isalpha()]
    words = [w for w in words if not w in stop_words]

    #stemmed = [porter.stem(word) for word in words]

    return words

def clean_text_keep_punct(text):
    tokens = word_tokenize(text)
    tokens = [w.lower() for w in tokens]

    words = [w for w in tokens if not w in stop_words]

    #stemmed = [porter.stem(word) for word in words]

    sentence = ""

    for s in words:
        if sentence == "":
            sentence = s
        elif s in string.punctuation:
            sentence += s
        else:
            sentence += " " + s

    return sentence


def write_data_to_textfile(data):
    for index, row in data.iterrows():
        with open("test_text.txt", "a") as myfile:
            print(str(index) + ' of ' + str(len(data)))
            try:
                title = row['title']
                content = row['content']
                myfile.write(clean_text_keep_punct(title) + '\n\n' + clean_text_keep_punct(content) + '\n\n')
            except:
                continue

        myfile.close()

def write_data_to_textfile_no_proc(data):
    for index, row in data.iterrows():
        with open("CORPUS/corpus_text_" + str(index) + '.txt', "a") as myfile:
            try:
                title = row['title']
                content = row['content']
                myfile.write(title + '\n\n' + content + '\n\n')
            except:
                continue

        myfile.close()

def build_mega_sentence_list(data):
    sentence_list = []

    for index, row in data.iterrows():
        if index % 1000 == 0:
            print(index)
        try:
            title = row['title']
            content = row['content']
            sentence_list.append(clean_text(title))
            sentence_list.append(clean_text(content))
        except:
            continue
    return sentence_list

def build_mega_sentence_list_title_only(data):
    sentence_list = []

    for index, row in data.iterrows():
        if index % 1000 == 0:
            print(index)
        try:
            title = row['title']
            sentence_list.append(clean_text(title))
        except:
            continue
    return sentence_list

titles = build_mega_sentence_list_title_only(df)

model = Word2Vec(titles)
print(model)
words = list(model.wv.vocab)
print(words)
print(model['amazon'])

model.save("mashable-titles-word2vec.model")

embedded_data = model[model.wv.vocab]
print('Word vector shape:', print(np.shape(embedded_data)))

pca = PCA(n_components=2)
reduced_data = pca.fit_transform(embedded_data)

plt.scatter(reduced_data[:,0], reduced_data[:, 1], s=2)

for i, word in enumerate(words):
    plt.annotate(word, xy=(reduced_data[i, 0], reduced_data[i, 1]))
plt.show()





