from __future__ import print_function
from Bio import Entrez
from Bio import Medline
from Bio.Entrez import efetch, read

Entrez.email = 'trivneel211@gmail.com'#let NCBI know who you are


def search_by_string(query, max_res):
    handle = Entrez.esearch(db="pubmed", term=query, retmax = max_res)
    record = Entrez.read(handle)
    handle.close()
    idlist = record["IdList"]

    handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",retmode="text")
    records = Medline.parse(handle)

    records = list(records) #makes it much easier, trust me

    for record in records:
        print("PMID:", record.get("PMID", "?"))
        print("Abstract:", record.get("AB", "?"))
        print("") #order the abstracts by number of occurrences (add more metrics later)




def fetch_abstract(pmid):
    handle = efetch(db='pubmed', id=pmid, retmode='xml')
    xml_data = Entrez.read(handle)
    print(xml_data)
    try:
        article = xml_data['MedlineCitation']['Article']
        abstract = article['Abstract']
        return abstract
    except IndexError:
        return None

search_by_string("BRAF", 500)



