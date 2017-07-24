from __future__ import print_function
from Bio import Entrez
from Bio import Medline
from Bio.Entrez import efetch, read

import urllib2, json
from itertools import chain
import re

Entrez.email = "trivneel211@gmail.com"

bioconcept = "Gene,Mutation,Disease"
format = "PubTator"

max_res= 500
accep_pub_types = ["Journal Article", "Clinical Trial"]

#get all papers from the last week (defined as 7 days)
handle = Entrez.esearch(db="pubmed", term="", reldate=7, rettype ="medline", retmode="text", retmax = max_res)
record = Entrez.read(handle)
handle.close()
idlist = record["IdList"]

handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",retmode="text")
records = Medline.parse(handle)

records = list(records)

pattern = re.compile(r"Disease\tD\w\w\w\w\w\w")

