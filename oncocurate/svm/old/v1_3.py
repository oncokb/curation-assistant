from __future__ import division
import pandas as pd

import numpy as np

from sklearn import svm
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.metrics import roc_curve, auc
'''
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

#combine oncokb feature vectors w/ infectious disease feature vectors from PubMed entries
#Question: How to pre-annotate? - annotators NEED to create corpus of labeled data...

max_res = 1000

accep_pub_types = ["Journal Article", "Clinical Trial"] #add more if needed

handle = Entrez.esearch(db="pubmed", term="infectious disease", rettype = "medline", retmode="text", retmax = max_res)
record = Entrez.read(handle)
handle.close()

idlist = record['IdList']

handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",retmode="text")
records = Medline.parse(handle)

records = list(records)

unrelated_feature_vectors = list()

for record in records:
    unrelated_feature_vectors.append(libs(hallmark_queries, record.get("AB", "?")))

header1 = hallmark_queries
df = pd.DataFrame(unrelated_feature_vectors)

df.to_csv('weekly_unrelated_featureVectors.csv', index=True, header=header1)


df1  = pd.DataFrame.from_csv("oncokb_featureVectors.csv")
df2 = pd.DataFrame.from_csv("weekly_unrelated_featureVectors.csv")
to_merge = ["oncokb_featureVectors.csv", "weekly_unrelated_featureVectors.csv"]
merge_csv(to_merge, "combined_featureVectors.csv")'''


featureVectors = pd.DataFrame.from_csv("combined_featureVectors.csv")
labels = pd.DataFrame.from_csv("labels.csv")


featureVectors = featureVectors.values.tolist()
labels = labels.values.tolist()


import random

#randomly shuffle feature vectors and labels the same way
combined = list(zip(featureVectors, labels))
random.shuffle(combined)
featureVectors, labels = zip(*combined)

np.random.seed(45234)
indices = np.random.permutation(len(featureVectors))

train_indices = indices[:-2025] #all indices except the last fifty -> automatically equalize this number????
train_vectors = list()
train_labels = list()

for index, vector in enumerate(featureVectors):
    if index in train_indices:
        train_vectors.append(vector)

for index, label in enumerate(labels):
    if index in train_indices:
        train_labels.append(label)

train_labels = [val for sublist in train_labels for val in sublist]

test_indices = indices[-2025:] #last ten indices
test_vectors = list()
test_labels = list()

for index, vector in enumerate(featureVectors):
    if index in test_indices:
        test_vectors.append(vector)

for index, label in enumerate(labels):
    if index in test_indices:
        test_labels.append(label)

'''df_train_vectors = pd.DataFrame(train_vectors)
df_train_labels = pd.DataFrame(train_labels)
df_test_vectors = pd.DataFrame(test_vectors)
df_test_labels = pd.DataFrame(test_labels)

np.set_printoptions(threshold='nan')

df_train_vectors.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))

C_range = np.logspace(-2, 10, 13)
gamma_range = np.logspace(-9, 3, 13)
param_grid = dict(gamma=gamma_range, C=C_range)
cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)
grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
grid.fit(df_train_vectors, train_labels)

print("The best parameters are %s with a score of %0.2f"
      % (grid.best_params_, grid.best_score_))

# Now we need to fit a classifier for all parameters in the 2d version
# (we use a smaller set of parameters here because it takes a while to train)

C_2d_range = [1e-2, 1, 1e2]
gamma_2d_range = [1e-1, 1, 1e1]
classifiers = []
for C in C_2d_range:
    for gamma in gamma_2d_range:
        clf = SVC(C=C, gamma=gamma)
        clf.fit(train_vectors[:, :2], train_labels)
        classifiers.append((C, gamma, clf))'''
np.set_printoptions(threshold='nan')
#C = 1.0, gamma= 100.0
#C = 1000, gamma = 0.001 - Doesn't work (all 1s)
#C = 100000, gamma = 0.0001 -> grid search best parameters
clf = svm.SVC(kernel="rbf", C=1.0, gamma=100.0, probability=True)
clf.fit(train_vectors, train_labels)
print(train_vectors)
test_results = clf.predict(test_vectors)
print(test_results)
print(clf.predict_proba(test_vectors))
print(len(test_results))


print(test_labels)
print(len(test_labels))

#calculate accuracy
final_results = test_results.tolist()

final_labels = [val for sublist in test_labels for val in sublist]

corres_count = 0
for r, l in zip(final_results, final_labels):
    if r ==l:
        corres_count = corres_count +1

print(corres_count / 2025)

'''from sklearn import cluster
k_means = cluster.KMeans(n_clusters=2)
k_means.fit(df_cluster)
print(k_means.labels_[::100])
print(labels[::100])'''




#combined.to_csv('combined_featureVectors.csv', index=True, header=header1)

