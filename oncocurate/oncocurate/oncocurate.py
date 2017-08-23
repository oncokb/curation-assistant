import click

from calc_features import *
from util import *
from get_data import *
from process_data import *
from termcolor import colored

@click.group()
@click.version_option()
def cli():
    """
    """


@cli.group()
def weekly():
    """Entry point into the weekly system run"""


@weekly.command('sr')#simple HoC ranking
@click.argument('maxres')
@click.argument('keydict')
@click.option('--zero/--no-zero', default=False)
@click.option('--reldate', default=7)
def simple_hoc_rank(maxres, keydict, reldate, zero):#ab-compare average across all queries
    keyword_dict = read_lines_to_list(keydict)
    idlist = pubmed_query(maxres, reldate)
    records = fetch_medline_records(idlist, "text")
    hoc_score_list = get_avg_relations(records, keyword_dict, pmid=True)
    print(hoc_score_list)

@weekly.command

@weekly.command('cftree')#cross-reference disease mentions with Oncotree
@click.argument('maxres')
@click.option('--reldate', default=7)
def oncotree_filter(maxres, reldate):#print abstract ids w/ >= 1 Disease mention in Oncotree
    idlist = pubmed_query(maxres, reldate)
    records = fetch_medline_records(idlist, "text")
    pattern = re.compile(r"Disease\tD\w\w\w\w\w\w")
    filtered_ids = disease_topic_filter(pattern, records)
    print(filtered_ids)

@cli.group()
def svm():
    """Entry point into the svm training feature"""

'''@svm.command('train')
@click.argument('tf')
@click.argument('lab')#should have an option for grid search file path'''

#Change to this: http://scikit-learn.org/dev/auto_examples/model_selection/plot_grid_search_digits.html

@svm.command('grid')
@click.argument('features')#path to calculated features (csv)
@click.argument('labels')#path to label (csv)
@click.argument('teprop')#decimal proportion of test set
def grid_search(features, labels, teprop):
    df_features = pd.DataFrame.from_csv(features)#do these dataframes need to be preserved??
    df_labels = pd.DataFrame.from_csv(labels)

    featureVectors = df_features.values.tolist()
    labels = df_labels.values.tolist()

    partition_point = int(teprop * len(featureVectors))

    packed_shuffle = simul_shuffle(featureVectors, labels)
    featureVectors = list(packed_shuffle[0])#unpacking features from 2-tuple
    labels = list(packed_shuffle[1])#unpacking labels from 2-tuple

    packed_split = split_supervised(featureVectors, labels, partition_point)
    #packed_split = easy_split(featureVectors, labels, test_part) #easier method (see process_data.py)

    df_train_vectors = pd.DataFrame(list(packed_split[0]))
    train_labels = list(packed_split[1])#needs to be a list, otherwise throws y dimensionality error...
    df_test_vectors = pd.DataFrame(list(packed_split[2]))
    df_test_labels = pd.DataFrame(list(packed_split[3]))

    np.set_printoptions(threshold='nan')#prints all of a dataframe or result apparently

    best_params = grid_search_train(df_train_vectors, train_labels, orig=True) #chooses standardization scheme
    print(best_params)

@svm.command('rocsvm')
@click.argument('features')
@click.argument('labels')
@click.argument('grpath')
@click.option('--k', default = 10)
@click.option('--nnoi', default =0)
#MAKE SURE TO FIX MATPLOTLIB.PYPLOT ISSUE AS BELOW:
#cd ~/.matplotlib, nano matplotlibrc, and insert "backend: TkAgg
def roc_svm(features, labels, grpath, k, nnoi):


'''
@svm.command('train')
@click.argument('features')
@click.argument('labels')

@cli.group()
def ner():
   """Entry point into the PubTator features"""

@ner.command('ner')
@click.argument('maxres')'''





