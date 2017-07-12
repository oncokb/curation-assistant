from __future__ import print_function
from Bio import Entrez
from Bio import Medline
from Bio.Entrez import efetch, read

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import base64

from pandas import *  # pretty printing 2d lists (a.k.a the id/abstract pairs)

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
    <body>
'''
FOOTER = '''
    </body>
</html>
'''

def make_2d_list(row, col):
    a = []
    for row in xrange(row): a += [[0]*col]
    return a


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

    for record in records:
        final_list.append([record.get("PMID", "?"), record.get("AB", "?")])
       # print("PMID:", record.get("PMID", "?"))
       # print("Abstract:", record.get("AB", "?"))
       # print("")  # order the abstracts by number of occurrences (add more metrics later)

    print(DataFrame(final_list))  # this is really nice for data viz on the matrix

    df = pandas.DataFrame(final_list)

    with open('test.html', 'w') as f:
        f.write(HEADER)
        f.write(df.to_html(classes='df'))
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



