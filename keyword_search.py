from __future__import print_functon
from Bio import Entrez
from Bio import Medline

from pandas import *

import urllib2, json
from itertools import chain
import re

Entrez.email = "trivneel211@gmail.com"

bioconcept = "Gene,Mutation,Disease" #just replace with whatever associations you are making
format = 'PubTator'

max_res = 500
accep_pub_types = ["Journal Article", "Clinical Trial"] #add more if needed

handle = Entrez.esearch(db="pubmed", term="", reldate=7, rettype ="medline", retmode="text", retmax = max_res)
record = Entrez.read(handle)
handle.close()
idlist = record["IdList"]

handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",retmode="text")
records = Medline.parse(handle)

records = list(records)

pattern = re.compile(r"Disease\tD\w\w\w\w\w\w")




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


