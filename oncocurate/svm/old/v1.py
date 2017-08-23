import urllib2

import pandas as pd
import re

from get_data.calc_features import calc_features

hallmark_queries = ['proliferation receptor',#add fuzzy matching
                    'growth factor',
                    'cell cycle',
                    'contact inhibition',
                    'apoptosis',
                    'necrosis',
                    'autophagy',
                    'senescence',
                    'immortalization',
                    'angiogenesis',
                    'angiogenic factor',
                    'metastasis',
                    'mutation',
                    'DNA repair',
                    'adducts',
                    'DNA damage',
                    'inflammation',
                    'oxidative stress',
                    'warburg effect',
                    'growth',
                    'activation',
                    'immune system']#these should ideally be read in from a txt file

from Bio import Entrez
from Bio import Medline

Entrez.email = "trivneel211@gmail.com"

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

oncokb_featureVectors = list()

zero_count = 0
nonzero_count = 0

for record in records:#individual abstracts
    curr_vector = calc_features(hallmark_queries, record.get("AB", "?"))
    oncokb_featureVectors.append(curr_vector)
    if sum(curr_vector)/len(curr_vector)==0:
        zero_count = zero_count + 1

print(zero_count)
print(len(oncokb_featureVectors))

df = pd.DataFrame(oncokb_featureVectors)
header1 = hallmark_queries #this is cool inception lol - not sure if it's gonna work tho
#df.to_csv('oncokb_featureVectors.csv', index=True, header=header1)


df_cluster = df.values

featureVectors = oncokb_featureVectors

#get some irrelevant abstracts

'''import os
from util import *

rootdir = '/Users/ntriv/Downloads/HoCCorpus'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        path = os.path.join(subdir,file)
        file_text = open(path, 'r').read()
        featureVectors.append(libs(hallmark_queries, file_text))

df2 = pd.DataFrame(featureVectors)
df2.to_csv('featureVectors.csv', index=True, header=header1)'''

'''np.set_printoptions(threshold='nan')

from sklearn import cluster
k_means = cluster.KMeans(n_clusters=2)
k_means.fit(df_cluster)
print(k_means.labels_)'''

