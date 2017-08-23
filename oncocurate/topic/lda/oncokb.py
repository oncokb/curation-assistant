import urllib2

import numpy as np
import pandas as pd
import re

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print "Topic %d:" % (topic_idx)
        print " ".join([feature_names[i]
                        for i in topic.argsort()[:-no_top_words - 1:-1]])

from Bio import Entrez
from Bio import Medline

Entrez.email = "trivneel211@gmail.com"

max_res = 1000 # randomly select 1000 from OncoKB as well

url_Submit = "http://oncokb.org/api/v1/evidences/lookup/"
urllib_result = urllib2.urlopen(url_Submit)
raw = urllib_result.read()
pattern = re.compile(r'"pmid":"\w\w\w\w\w\w\w\w"')
raw_mesh = re.findall(pattern, raw)
cooked_mesh = [mention.replace('"pmid":"', '') for mention in raw_mesh] #isolate numerical pmids
cooked_mesh = [mention.replace('"', '') for mention in cooked_mesh]
idlist = list(set(cooked_mesh))#remove duplicate pmids

handle = Entrez.efetch(db = "pubmed", id=idlist, rettype="medline", retmode="text")
records = Medline.parse(handle)

records = list(records)

oncokb_abstracts = list()

for record in records:
    oncokb_abstracts.append(record.get("AB", "?"))

no_features = 1000

# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tf = tf_vectorizer.fit_transform(oncokb_abstracts)
tf_feature_names = tf_vectorizer.get_feature_names()

no_topics = 20
lda = LatentDirichletAllocation(n_topics=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
no_top_words = 10
display_topics(lda, tf_feature_names, no_top_words)
