from __future__ import print_function
from Bio import Entrez
from Bio import Medline
from Bio.Entrez import efetch, read

from pandas import *

Entrez.email = 'trivneel211@gmail.com'

max_res = 500

hallmark_queries = ['proliferation receptor',
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
                    'immune system']

final_list = list()

debug_index = len(hallmark_queries)-1

'''handle = Entrez.esearch(db='pubmed', term = hallmark_queries[0] , retmax = max_res)
record = Entrez.read(handle)
handle.close()
idlist = record["IdList"]

handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",retmode="text")
records = Medline.parse(handle)
records = list(records)


for record in records:
    if 'cancer' in record.get("AB", "?"):
        final_list.append([record.get("PMID", "?"), record.get("TI", "?"), "https://www.ncbi.nlm.nih.gov/pubmed/?term=" +
                          record.get("PMID", "?")])'''

for i in range(0, len(hallmark_queries)-1):

    handle = Entrez.esearch(db='pubmed', term = hallmark_queries[i] , retmax = max_res)
    record = Entrez.read(handle)
    handle.close()
    idlist = record["IdList"]

    handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",retmode="text")
    records = Medline.parse(handle)
    records = list(records)


    for record in records:
        if 'cancer' in record.get("AB", "?"):
            final_list.append([record.get("PMID", "?"), record.get("TI", "?"), record.get("AB", "?")])

final_df = pandas.DataFrame(final_list)
column_names = ["PMID", "Title", "Abstract"]
final_df.columns = column_names

print(final_df)

final_df.to_csv('training_set.csv', sep=',',encoding = 'utf-8')