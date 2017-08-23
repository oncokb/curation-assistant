import urllib2

import numpy as np
import pandas as pd
import re

from oncocurate.calc_features import *

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

mod_queries = [hallmark_queries[0], hallmark_queries[1], hallmark_queries[2]]

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

oncokb_featureVectors = list()

for record in records:#individual abstracts
    oncokb_featureVectors.append(calc_features_avg(mod_queries, record.get("AB", "?")))

df = pd.DataFrame(oncokb_featureVectors)
header1 = mod_queries #this is cool inception lol - not sure if it's gonna work tho
#df.to_csv('oncokb_featureVectors.csv', index=True, header=header1)

#get some irrelevant abstracts

np.set_printoptions(threshold='nan')

df_cluster = df.values

print(df_cluster)

from sklearn import cluster
k_means = cluster.KMeans(n_clusters=2)
k_means.fit(df_cluster)
print(k_means.labels_)