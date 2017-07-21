from __future__ import print_function
from Bio import Entrez
from Bio import Medline
from Bio.Entrez import efetch, read


import urllib2, json
from itertools import chain
import re

import time
import sys
import getopt

Entrez.email = "trivneel211@gmail.com"

bioconcept = "Gene,Mutation,Disease" #just replace with whatever associations you are making
format = 'PubTator'

max_res = 500
accep_pub_types = ["Journal Article", "Clinical Trial"] #add more if needed


#get all papers from the last week
handle = Entrez.esearch(db="pubmed", term="", reldate=7, rettype ="medline", retmode="text", retmax = max_res)
record = Entrez.read(handle)
handle.close()
idlist = record["IdList"]

handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",retmode="text")
records = Medline.parse(handle)

records = list(records)

pattern = re.compile(r"Disease\tD\w\w\w\w\w\w")

#record.get("PT", "?") -> how to get the publication type as a string
for record in records:
    for pubtype in accep_pub_types: #simple filter, but can be taken out
        if pubtype in record.get("PT", "?"):
            pmid = record.get("PMID", "?")
            url_Submit = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/" + bioconcept + "/" + pmid + "/" + format + "/"
            urllib_result = urllib2.urlopen(url_Submit)#this returns an instance; use read method to get string
            res = urllib_result.read()
            raw_mesh = re.findall(pattern, res)
            cooked_mesh = [mention.replace("Disease\t", "") for mention in raw_mesh] #this is called a list comprehension
            cooked_mesh = list(set(cooked_mesh))#only keep unique disease ids
            #print(cooked_mesh)
            for mention in cooked_mesh:
                oncotree_url = "http://oncotree.mskcc.org/oncotree-mappings/crosswalk?vocabularyId=MSH&conceptId=" + mention
                oncotree_response = urllib2.urlopen(oncotree_url)
                data = json.loads(oncotree_response.read())
                if not data['oncotreeCode']:
                    continue
                else:
                    print(res)


oncotree_ids = list()
mesh_id = "D013584"

oncotree_url = "http://oncotree.mskcc.org/oncotree-mappings/crosswalk?vocabularyId=MSH&conceptId=" + mesh_id
oncotree_response = urllib2.urlopen(oncotree_url)
data = json.loads(oncotree_response.read())
oncotree_ids.append(data['oncotreeCode'])


#...after for loop...
final_ids = list(chain.from_iterable(oncotree_ids))#don't need to do this until empty-list check is done

#if list() = False => there is nothing inside the list