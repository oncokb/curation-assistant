from __future__ import division
import pandas as pd

import numpy as np

from sklearn import svm
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score

import random

featureVectors = pd.DataFrame.from_csv("/Users/ntriv/PycharmProjects/nlp_parsing_engine/get_data/com_featureVectors_balanced.csv")
labels = pd.DataFrame.from_csv("/Users/ntriv/PycharmProjects/nlp_parsing_engine/get_data/balanced_labels.csv")

featureVectors = featureVectors.values.tolist()
labels = labels.values.tolist()

labels = [val for sublist in labels for val in sublist] #list comprehension

#randomize features and labels together
combined = list(zip(featureVectors, labels))
random.shuffle(combined)
featureVectors, labels = zip(*combined)

#manual splitting
features_train, features_test, labels_train, labels_test = train_test_split(featureVectors, labels, test_size=0.3, random_state=0)

clf = svm.SVC(kernel="rbf", C=1, gamma=100.0, probability=True).fit(features_train, labels_train)
score = clf.score(features_test, labels_test)

#ShuffleSplit

cv = ShuffleSplit(n_splits=10, test_size=0.3, random_state=0)

scores = cross_val_score(clf, featureVectors, labels, cv=cv)

#KFold

cv = KFold(n_splits=10, random_state=None, shuffle=False)

scores = cross_val_score(clf, featureVectors, labels, cv=cv)