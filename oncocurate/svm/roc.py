#READ BELOW FOR IMPORTANT INFO IF YOU ARE USING A VIRTUALENV AND PYTHON 2
#MAKE SURE TO FIX MATPLOTLIB.PYPLOT ISSUE AS BELOW:
#cd ~/.matplotlib, nano matplotlibrc, and insert "backend: TkAgg"

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
classifier = svm.SVC(kernel='rbf', C=1.0, gamma =100.0, probability=True,
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
for train, test in cv.split(featureVectors):#this produces indices, not vectors
    train_features = list()
    test_features = list()
    print train
    print test
    train_features = index_filter(train, featureVectors, train_features)
    test_features = index_filter(test, featureVectors, test_features)
    probas_ = classifier.fit(train_features, labels[train]).predict_proba(test_features)    # Compute ROC curve and area the curve
    fpr, tpr, thresholds = roc_curve(labels[test], probas_[:, 1])
    print "Thresholds Below"
    print thresholds
    tprs.append(interp(mean_fpr, fpr, tpr))
    tprs[-1][0] = 0.0
    roc_auc = auc(fpr, tpr)
    aucs.append(roc_auc)
    plt.plot(fpr, tpr, lw=1, alpha=0.3,
             label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))

    i += 1
plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r',
         label='Luck', alpha=.8)

mean_tpr = np.mean(tprs, axis=0)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
std_auc = np.std(aucs)
plt.plot(mean_fpr, mean_tpr, color='b',
         label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
         lw=2, alpha=.8)

std_tpr = np.std(tprs, axis=0)
tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                 label=r'$\pm$ 1 std. dev.')

plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()
