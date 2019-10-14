from nltk.corpus import PlaintextCorpusReader
from gensim.models.wrappers import FastText
import nltk
from gensim.test.utils import datapath

#reader = PlaintextCorpusReader("CORPUS/", '*.txt')
#corpus = nltk.Text(reader.words())

corpus = datapath('CORPUS/')  # absolute path to corpus

model = FastText(size=4, window=3, min_count=1)  # instantiate
# model.build_vocab(sentences=common_texts)
model.train(sentences=common_texts, total_examples=len(common_texts), epochs=10)  # train