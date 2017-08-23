from __future__ import division
import string
import math

tokenize = lambda doc: doc.lower().split(" ")

document_0 = "In human colorectal adenomas or polyps , cyclooxygenase-2 is expressed predominantly by stromal ( or interstitial ) macrophages . Therefore , we tested the hypothesis that macrophage cyclooxygenase-2 has paracrine pro-tumorigenic activity using in vitro models of macrophage-epithelial cell interactions .We report that macrophages can promote tumorigenic progression of intestinal epithelial cells ( evidenced by decreased cell-cell contact inhibition , increased proliferation and apoptosis , gain of anchorage-independent growth capability , decreased membranous E-cadherin expression , up-regulation of cyclooxygenase-2 expression , down-regulation of transforming growth factor-beta type II receptor expression and resistance to the anti-proliferative activity of transforming growth factor-beta(1) ) in a paracrine , cyclooxygenase-2-dependent manner .Pharmacologically relevant concentrations ( 1-2 microM ) of a selective cyclooxygenase-2 inhibitor had no detectable , direct effect on intestinal epithelial cells but inhibited the macrophage-epithelial cell signal mediating tumorigenic progression .Cyclooxygenase-2-mediated stromal-epithelial cell signalling during the early stages of intestinal tumorigenesis provides a novel target for chemoprevention of colorectal cancer ( and other gastro-intestinal epithelial malignancies , which arise on a background of chronic inflammation , such as gastric cancer ) and may explain the discrepancy between the concentrations of cyclooxygenase inhibitors required to produce anti-neoplastic effects in vitro and in vivo ."
document_1 = "At last, China seems serious about confronting an endemic problem: domestic violence and corruption."
document_2 = "Japan's prime minister, Shinzo Abe, is working towards healing the economic turmoil in his own country for his view on the future of his people."
document_3 = "Vladimir Putin is working hard to fix the economy in Russia as the Ruble has tumbled."
document_4 = "What's the future of Abenomics? We asked Shinzo Abe for his views"
document_5 = "Obama has eased sanctions on Cuba while accelerating those against the Russian Economy, even as the Ruble's value falls almost daily."
document_6 = "Vladimir Putin is riding a horse while hunting deer. Vladimir Putin always seems so serious about things - even riding horses. Is he crazy?"

all_documents = [document_0, document_1, document_2, document_3, document_4, document_5, document_6]


def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection) / len(union)


def term_frequency(term, tokenized_document):
    return tokenized_document.count(term)


def sublinear_term_frequency(term, tokenized_document):
    count = tokenized_document.count(term)
    if count == 0:
        return 0
    return 1 + math.log(count)


def augmented_term_frequency(term, tokenized_document):
    max_count = max([term_frequency(t, tokenized_document) for t in tokenized_document])
    return (0.5 + ((0.5 * term_frequency(term, tokenized_document)) / max_count))


def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents) / (sum(contains_token)))
    return idf_values


def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]
    idf = inverse_document_frequencies(tokenized_documents)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = sublinear_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents

from Bio import Entrez
from Bio import Medline
import re, urllib2

Entrez.email = "trivneel211@gmail.com"

url_Submit = "http://oncokb.org/api/v1/evidences/lookup/"
urllib_result = urllib2.urlopen(url_Submit)
raw = urllib_result.read()
pattern = re.compile(r'"pmid":"\w\w\w\w\w\w\w\w"')
raw_mesh = re.findall(pattern, raw)
cooked_mesh = [mention.replace('"pmid":"', '') for mention in raw_mesh] #isolate numerical pmids
cooked_mesh = [mention.replace('"', '') for mention in cooked_mesh]
idlist = list(set(cooked_mesh))#remove duplicate pmids

Entrez.email = "trivneel211@gmail.com"

print idlist

id_subset = idlist[:10]
print len(id_subset)

handle = Entrez.efetch(db = "pubmed", id=id_subset, rettype="medline", retmode="text")
records = Medline.parse(handle)

records = list(records)

all_documents = list()
for record in records:
    all_documents.append(record.get("AB", "?"))

print("OncoKB abstracts have been retrieved")

all_docs = all_documents[:5]
tfidf_representation = tfidf(all_docs)
for rep in tfidf_representation:
    print(rep)
for doc in all_docs:
    print(doc)
print("Tf-idf is done")

