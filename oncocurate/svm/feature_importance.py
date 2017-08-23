import numpy as np
from scipy import interp
import matplotlib.pyplot as plt
from itertools import cycle

import pandas as pd

from sklearn import svm
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
from numpy import array
import random

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


def index_filter(indices, inlist, outlist):
    for index, entry in enumerate(inlist):
        if index in indices:
            outlist.append(entry)
    return outlist

def plot_coefficients(classifier, feature_names=hallmark_queries, top_features=11):
    coef = classifier.coef_.ravel()
    top_positive_coefficients = np.argsort(coef)[-top_features:]
    top_negative_coefficients = np.argsort(coef)[:top_features]
    top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
    # create plot
    plt.figure(figsize=(15, 5))
    colors = ['red' if c < 0 else 'blue' for c in coef[top_coefficients]]
    plt.bar(np.arange(2 * top_features), coef[top_coefficients], color=colors, align='center')
    feature_names = np.array(feature_names)
    plt.xticks(np.arange(0, 2 * top_features), feature_names[top_coefficients], rotation=60, ha='right', fontsize=10, fontweight='bold')
    plt.ylabel('Relative Coefficient Importance Score', fontsize=10)
    plt.xlabel('Feature (Keyword) Name', fontsize=15)
    plt.title('Relative Feature Importance of HoC Dict #1 During SVM Relevance Classification', fontsize=15)
    plt.subplots_adjust(bottom=0.3)
    plt.show()

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

tprs = []
aucs = []
mean_fpr = np.linspace(0, 1, 100)

print featureVectors.shape
print labels.shape


labels = [val for sublist in labels for val in sublist]
labels = array(labels)
print labels


i = 0
for train, test in cv.split(featureVectors):
    train_features = list()
    test_features = list()
    print train
    print test
    train_features = index_filter(train, featureVectors, train_features)
    test_features = index_filter(test, featureVectors, test_features)
    probas_ = classifier.fit(train_features, labels[train]).predict_proba(test_features)
    plot_coefficients(classifier)

    i += 1
