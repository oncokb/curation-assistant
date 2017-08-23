import urllib2, json
from Bio import Entrez
from Bio import Medline
import re

Entrez.email = "trivneel211@gmail.com"

def get_oncokb_pmids():
    url_Submit = "http://oncokb.org/api/v1/evidences/lookup/"
    urllib_result = urllib2.urlopen(url_Submit)
    raw = urllib_result.read()
    pattern = re.compile(r'"pmid":"\w\w\w\w\w\w\w\w"')
    raw_mesh = re.findall(pattern, raw)
    cooked_mesh = [mention.replace('"pmid":"', '') for mention in raw_mesh]  # isolate numerical pmids
    cooked_mesh = [mention.replace('"', '') for mention in cooked_mesh]
    idlist = list(set(cooked_mesh))  # remove duplicate pmids
    return idlist

def fetch_medline_records(idlist, type):
    handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline", retmode=type)
    records = Medline.parse(handle)

    records = list(records)
    return records

def pubmed_query(max_res, reldate, query=""):
    handle = Entrez.esearch(db="pubmed", term=query, rettype="medline", retmode="text", reldate = reldate, retmax=max_res)
    record = Entrez.read(handle)
    handle.close()
    idlist = record["IdList"]
    return idlist

def read_url(url, as_str=True):
    if as_str:
        urllib_result = urllib2.urlopen(url)
        res = urllib_result.read()
        return res
    else:
        return urllib2.urlopen(url)

