#these three are needed for any NLP w/ NLTK
from __future__ import division
import nltk, re, pprint
from nltk import word_tokenize


#Data-Grab from OncoKB
from urllib2 import urlopen

url = "http://oncokb.org/api/v1/utils/allVariants.txt"
response = urlopen(url)
raw = response.read().decode('utf8')

type(raw)#for debugging purposes, should return unicode if Python 2, str if Python 3

len(raw)#allActionableVariants = 54345 (July 5, 2017)

tokens = word_tokenize(raw)
type(tokens)
len(tokens)
tokens[1024:1056]#just to make sure

text = nltk.Text(tokens)
type(text)
text.collocations()#finds common n-grams that occur together in the file

