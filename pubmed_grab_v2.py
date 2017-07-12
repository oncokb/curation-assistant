import re
import sys
import traceback
from bs4 import BeautifulSoup
import requests


class PubMedObject(object):
    soup = None
    url = None

    # pmid is a PubMed ID
    # url is the url of the PubMed web page
    # search_term is the string used in the search box on the PubMed website
    def __init__(self, pmid=None, url='', search_term=''):
        if pmid:
            pmid = pmid.strip()
            url = "http://www.ncbi.nlm.nih.gov/pubmed/%s" % pmid
        if search_term:
            url = "http://www.ncbi.nlm.nih.gov/pubmed/?term=%s" % search_term
        page = requests.get(url).text
        self.soup = BeautifulSoup(page, "html.parser")

        # set the url to be the fixed one with the PubMedID instead of the search_term
        if search_term:
            try:
                url = "http://www.ncbi.nlm.nih.gov/pubmed/%s" % self.soup.find("dl",class_="rprtid").find("dd").text
            except AttributeError as e:  # NoneType has no find method
                print("Error on search_term=%s" % search_term)
        self.url = url

    def get_title(self):
        return self.soup.find(class_="abstract").find("h1").text

    #auths is the string that has the list of authors to return
    def get_authors(self):
        result = []
        author_list = [a.text for a in self.soup.find(class_="auths").findAll("a")]
        for author in author_list:
            lname, remainder = author.rsplit(' ', 1)
            #add periods after each letter in the first name
            fname = ".".join(remainder) + "."
            result.append(lname + ', ' + fname)

        return ', '.join(result)

    def get_citation(self):
        return self.soup.find(class_="cit").text

    def get_external_url(self):
        url = None
        doi_string = self.soup.find(text=re.compile("doi:"))
        if doi_string:
            doi = doi_string.split("doi:")[-1].strip().split(" ")[0][:-1]
            if doi:
                url = "http://dx.doi.org/%s" % doi
        else:
            doi_string = self.soup.find(class_="portlet")
            if doi_string:
                doi_string = doi_string.find("a")['href']
                if doi_string:
                    return doi_string

        return url or self.url

    def render(self):
        template_text = ''
        with open('template.html','r') as template_file:
            template_text = template_file.read()

        try:
            template_text = template_text.replace("{{ external_url }}", self.get_external_url())
            template_text = template_text.replace("{{ citation }}", self.get_citation())
            template_text = template_text.replace("{{ title }}", self.get_title())
            template_text = template_text.replace("{{ authors }}", self.get_authors())
            template_text = template_text.replace("{{ error }}", '')
        except AttributeError as e:
            template_text = template_text.replace("{{ external_url }}", '')
            template_text = template_text.replace("{{ citation }}", '')
            template_text = template_text.replace("{{ title }}", '')
            template_text = template_text.replace("{{ authors }}", '')
            template_text = template_text.replace("{{ error }}", '<!-- Error -->')

        return template_text.encode('utf8')

def start_table(f):
    f.write('\t\t\t\t\t\t\t\t\t<div class="resourcesTable">\n');
    f.write('\t\t\t\t\t\t\t\t\t\t<table border="0" cellspacing="0" cellpadding="0">\n');

def end_table(f):
    f.write('\t\t\t\t\t\t\t\t\t\t</table>\n');
    f.write('\t\t\t\t\t\t\t\t\t</div>\n');

def start_accordion(f):
    f.write('\t\t\t\t\t\t\t\t\t<div class="accordion">\n');

def end_accordion(f):
    f.write('\t\t\t\t\t\t\t\t\t</div>\n');

def main(args):
    try:
        # program's main code here
        print("Parsing pmids.txt...")
        with open('result.html', 'w') as sum_file:
            sum_file.write('<!--\n')
        with open('pmids.txt','r') as pmid_file:
        with open('result.html','a') as sum_file:
        for pmid in pmid_file:
            sum_file.write(pmid)
        sum_file.write('\n-->\n')
        with open('pmids.txt','r') as pmid_file:
            h3 = False
            h4 = False
            table_mode = False
            accordion_mode = False
            with open('result.html', 'a') as sum_file:
                for pmid in pmid_file:
                    if pmid[:4] == "####":
                        if h3 and not accordion_mode:
                            start_accordion(sum_file)
                            accordion_mode = True
                        sum_file.write('\t\t\t\t\t\t\t\t\t<h4><a href="#">%s</a></h4>\n' % pmid[4:].strip())
                        h4 = True
                    elif pmid[:3] == "###":
                        if h4:
                            if table_mode:
                                end_table(sum_file)
                                table_mode = False
                            end_accordion(sum_file)
                            h4 = False
                            accordion_mode = False
                        elif h3:
                            end_table(sum_file)
                            table_mode = False
                        sum_file.write('\t\t\t\t\t\t\t\t<h3><a href="#">%s</a></h3>\n' % pmid[3:].strip())
                        h3 = True
                    elif pmid.strip():
                        if (h3 or h4) and not table_mode:
                            start_table(sum_file)
                            table_mode = True
                        if pmid[:4] == "http":
                            if pmid[:18] == "http://dx.doi.org/":
                                sum_file.write(PubMedObject(search_term=pmid[18:]).render())
                            else:
                                print("url=%s" % pmid)
                                p = PubMedObject(url=pmid).render()
                                sum_file.write(p)
                                print(p)
                        elif pmid.isdigit():
                            sum_file.write(PubMedObject(pmid).render())
                        else:
                            sum_file.write(PubMedObject(search_term=pmid).render())
                if h3:
                    if h4:
                        end_table(sum_file)
                        end_accordion(sum_file)
                    else:
                        end_table(sum_file)
            pmid_file.close()
        print("Done!")

    except BaseException as e:
        print traceback.format_exc()
        print "Error: %s %s" % (sys.exc_info()[0], e.args)
        return 1
    except:
        # error handling code here
        print "Error: %s" % sys.exc_info()[0]
        return 1  # exit on error
    else:
        raw_input("Press enter to exit.")
        return 0  # exit errorlessly

if __name__ == '__main__':
    sys.exit(main(sys.argv))