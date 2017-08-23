import numpy as np
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle

import pandas as pd

from sklearn import svm
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from sklearn.decomposition import PCA
from numpy import array
import random

def split_supervised(featureSet, labelSet, partNum):

    np.random.seed(45234)
    indices = np.random.permutation(len(featureSet))
    train_indices = indices[:-(int)(partNum)]

    train_vectors = list()
    train_vectors = index_filter(train_indices, featureSet, train_vectors)

    train_labels = list()
    train_labels = index_filter(train_indices, labelSet, train_labels)

    train_labels = [val for sublist in train_labels for val in sublist]  # flattening the list using a comprehension

    test_indices = indices[-(int)(partNum):]
    test_vectors = list()
    test_vectors = index_filter(test_indices, featureSet, test_vectors)

    test_labels = list()
    test_labels = index_filter(test_indices, labelSet, test_labels)

    test_labels = [val for sublist in test_labels for val in sublist]

    return train_vectors, train_labels, test_vectors, test_labels



def index_filter(indices, inlist, outlist):
    for index, entry in enumerate(inlist):
        if index in indices:
            outlist.append(entry)
    return outlist


featureVectors = pd.DataFrame.from_csv("/Users/ntriv/PycharmProjects/nlp_parsing_engine/get_data/com_featureVectors_balanced.csv")
labels = pd.DataFrame.from_csv("/Users/ntriv/PycharmProjects/nlp_parsing_engine/get_data/balanced_labels.csv")

featureVectors = featureVectors.values.tolist()
labels = labels.values.tolist()

combined = list(zip(featureVectors, labels))
random.shuffle(combined)
featureVectors, labels = zip(*combined)
featureVectors = array(featureVectors)
labels = array(labels)

n_samples = labels.shape[0] #use labels bc. its faster to iterate through???
n_features = featureVectors.shape[1]
n_splits = 10 #should be a command line parameter

# I need to fully understand what this does
random_state = np.random.RandomState(0)
featureVectors = np.c_[featureVectors, random_state.randn(n_samples, 0)]


#Classification and ROC analysis
cv = KFold(n_splits=n_splits)

'''
open the file with grid search parameters (C and gamma) here, and input into SVC decl.
'''
classifier = svm.SVC(kernel='linear', C=1.0, gamma =100.0, probability=True,
                     random_state=random_state)


print featureVectors.shape
print labels.shape


labels = [val for sublist in labels for val in sublist]
labels = array(labels)
print labels

features_train, features_test, labels_train, labels_test = train_test_split(featureVectors, labels, test_size=0.33, random_state=42)

pca = PCA(n_components=6)
pca.fit(features_train)
np_train_features = array(features_train)
decomp_train_features = pca.transform(np_train_features)
decomp_test_features = pca.transform(features_test)


classifier.fit(decomp_train_features, labels_train)
predicted_labels = classifier.predict(decomp_test_features)
print(classification_report(labels_test, predicted_labels, target_names=["0", "1"]))
