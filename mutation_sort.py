from __future__ import print_function
from Bio import Entrez
from Bio import Medline
from Bio.Entrez import efetch, read

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import urllib2
import pandas as pd


#               Option 1
#
# Run mutation-identifier, then associate it to a gene
#
#               Option 2
#
# search for each mutation, then choose the ones
# that belong to the currently queried gene

# Task list for 7/14/2017
# associate variants to genes

raw_json= urllib2.urlopen("http://oncokb.org/api/v1/utils/allActionableVariants").read()
cooked_variants = pd.read_json(raw_json)

#to get a particular column, just do the following:
gene_series = cooked_variants['gene'] #can be indexed normally
variant_series



fromaddr = "trivneel211@gmail.com"
toaddr = "trivneel211@gmail.com"

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr

Entrez.email = 'trivneel211@gmail.com'  # let NCBI know who you are

HEADER = '''
<html>
    <head>

    </head>
    <body style="color:blue;">
'''
FOOTER = '''
    </body>
</html>
'''

def make_2d_list(row, col):
    a = []
    for row in xrange(row): a += [[0]*col]
    return a

def mutation_classify(gene, max_res):


def search_by_string(query, max_res):
    handle = Entrez.esearch(db="pubmed", term=query, retmax = max_res)
    record = Entrez.read(handle)
    handle.close()
    idlist = record["IdList"]

    handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",retmode="text")
    records = Medline.parse(handle)

    records = list(records)  # makes it much easier, trust me

    msg['Subject'] = query + "Query Results"  # add today's date to the subject later

    final_list = list()

    query_in_title = list()

    query_not_in_title = list()

    # https://www.ncbi.nlm.nih.gov/pubmed/?term=PMID

    for record in records:
        if query in record.get("TI", "?"):
            query_in_title.append([record.get("PMID", "?"), record.get("TI", "?"), "https://www.ncbi.nlm.nih.gov/pubmed/?term=" +
                        record.get("PMID", "?")])
        else:
            query_not_in_title.append([record.get("PMID", "?"), record.get("TI", "?"), "https://www.ncbi.nlm.nih.gov/pubmed/?term=" +
                        record.get("PMID", "?")])

    print(DataFrame(query_in_title))
    print(DataFrame(query_not_in_title))


       # print("PMID:", record.get("PMID", "?"))
       # print("Abstract:", record.get("AB", "?"))
       # print("")  # order the abstracts by number of occurrences (add more metrics later)

    pandas.set_option('display.max_colwidth', -1)

    df_in_title = pandas.DataFrame(query_in_title)
    df_not_title = pandas.DataFrame(query_not_in_title)

    column_names = ["PMID", "Title", "Link to Abstract"]
    df_in_title.columns = column_names
    df_not_title.columns = column_names

    df_in_title = df_in_title.replace({query: '<b>' + query + '</b'}, regex=True)
    df_not_title = df_not_title.replace({query: '<b>' + query + '</b'}, regex=True)


    with open('test.html', 'w') as f:
        f.write(HEADER)
        f.write(df_in_title.to_html(classes='df'))
        f.write(df_not_title.to_html(classes='df'))
        f.write(FOOTER)

    filename = 'test.html'
    f = file(filename)
    attachment = MIMEText(f.read(), 'html')
    msg.attach(attachment)

    server = smtplib.SMTP('smtp.gmail.com', 587)  # I'm pretty sure 587 is the port?
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("trivneel211", "inteli511")  # i think this is pointless tbh but whatever

    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

def fetch_abstract(pmid):  # not really being used at all, just a ref. function
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





