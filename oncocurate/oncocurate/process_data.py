from __future__ import division
from util import *
import numpy as np
import matplotlib.pyplot as plt
from scipy import interp
import pandas as pd
import re
from calc_features import *
from get_data import *

from sklearn import svm
from sklearn.model_selection import StratifiedShuffleSplit #how does compare/is different from K-fold???
from sklearn import preprocessing #various normalization functions
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split

from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
from numpy import array
import random

def get_avg_relations(records, keywords, pmid=False):
    if pmid==False:
        res_relations = list()
        for record in records:
            res_relations.append(calc_features_avg(keywords, record.get("AB", "?")))
        return res_relations
    else:#return pmids with each average
        res_relations = list()
        for record in records:
            res_relations.append([calc_features_avg(keywords, record.get("AB", "?")), record.get("PMID", "?")])
        return res_relations


def disease_topic_filter(pattern, records, accep_pub_types=["Journal Article", "Clinical Trial"]):
    res_idlist = list()
    for record in records:  # filter by Oncotree cancer type
        for pubtype in accep_pub_types:  # simple filter, but can be taken out
            if pubtype in record.get("PT", "?"):
                res = read_url("https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + "Disease" + "/" + record.get("PMID", "?") + "/" + "PubTator" + "/")
                raw_mesh = re.findall(pattern, res)
                cooked_mesh = [mention.replace("Disease\t", "") for mention in
                               raw_mesh]  # this is called a list comprehension
                cooked_mesh = list(set(cooked_mesh))  # only keep unique disease ids
                #print(cooked_mesh)
                for mention in cooked_mesh:
                    oncotree_response = read_url("http://oncotree.mskcc.org/oncotree-mappings/crosswalk?vocabularyId=MSH&conceptId=" + mention)
                    data = json.loads(oncotree_response)
                    if not data['oncotreeCode']:
                        continue
                    else:
                        print(cooked_mesh)
                        print(record.get("PMID", "?"))
               # if check_oncotree_ref(cooked_mesh)==True:#if any disease mentions in Oncotree
                   # res_idlist.append(record.get("PMID", "?"))
               # print(record.get("AB", "?"))
    #return res_idlist

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

def easy_split(featureSet, labelSet, prop):
    train_vectors, train_labels, test_vectors, test_labels = train_test_split(featureSet, labelSet, test_size=prop, random_state=42)
    return train_vectors, train_labels, test_vectors, test_labels

def grid_search_train(df_features, labels, orig = False, std = False, robust = False, maxabs = False):

    print("I got to the grid search function")
    if orig==True:
        print("I'm inside the orig if statements")
        #df_features.apply(lambda x: (x - np.mean(x)) / (np.max(x) - np.min(x)))  # quick normalization -> np.mean = np.amax returns scalar (max element from entire array)\
        df_features = preprocessing.scale(df_features)

    if std==True:#remember the formula for z-score? it's normalizing the distribution... (z = (x-mean)/stdev)
        scaler = preprocessing.StandardScaler().fit(df_features)
        df_features = scaler.transform(df_features)

    if robust==True:
        scaler = preprocessing.RobustScaler().fit(df_features)
        df_features = scaler.transform(df_features)

    if maxabs==True:
        scaler = preprocessing.MaxAbsScaler().fit(df_features)
        df_features = scaler.transform(df_features)

    C_range = np.logspace(-2, 10, 13)
    gamma_range = np.logspace(-9, 3, 13)
    param_grid = dict(gamma=gamma_range, C=C_range)
    cv = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=42)#read more about cross validation (cv) + K-fold vs. Shuffle Split + stratification
    grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv, verbose=5)
    print("right before fitting step")
    df_features = df_features.tolist()
    print(type(labels))

    print("right right before fitting step")
    grid.fit(df_features, labels)
    return grid.best_estimator_ #<class 'sklearn.svm.classes.SVC'>

def roc_svm_train(featureVectors, labels, grpath, n_splits, plot=True):#as numpy arrays

    n_samples = labels.shape[0]
    n_features = featureVectors.shape[1]
    n_splits = get_oncokb_pmids()

    random_state =


    cv = KFold(n_splits=n_splits)


    best_params = read_lines_to_list(grpath)
    best_params = map(float, best_params)
    # currently supports two: best_params

    # BREAK BETWEEN THE FUNCTION

    classifier = svm.SVC(kernel='rbf', C=best_params[0], gamma=best_params[1], probability=True,
                         random_state=random_state)

    tprs = [] # true positive rates
    fprs = []  # false positive rates

    aucs = []
    mean_fpr = np.linspace(0, 1, 100)

    labels = [val for sublist in labels for val in sublist]
    labels = array(labels)

    i = 0
    for train, test in cv.split(featureVectors):
        train_features = list()
    test_features = list()
    print train
    print test
    train_features = index_filter(train, featureVectors, train_features)
    test_features = index_filter(test, featureVectors, test_features)
    probas_ = classifier.fit(train_features, labels[train]).predict_proba(test_features)
    # Compute ROC curve and area the curve
    fpr, tpr, thresholds = roc_curve(labels[test], probas_[:, 1])
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


