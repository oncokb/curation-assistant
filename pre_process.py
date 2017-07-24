#Command to start StanfordNLP server (see below)
#java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://locahost:9000')

sample_abstract = "OBJECTIVES: To evaluate the association between PSA nadir level and time to nadir (TTN) with biochemical recurrence (BCR) risk after radical prostatectomy (RP) in the SEARCH database. METHODS: Retrospective analysis of 1,939 men from the SEARCH database treated with RP between 1998-2015 with available ultrasensitive PSA nadir within 1-6 months after RP. Uni- and multivariable analyses of PSA nadir and TTN with time from nadir to BCR were done with Cox models (adjusted for demographics, tumor features and preoperative PSA). RESULTS: Among men with an undetectable PSA nadir, the TTN was unrelated to BCR (1-2.9 vs. 3-6 months: HR 0.86, p=0.46). Regardless of TTN, men with detectable nadir had increased risk of BCR (TTN 3-6 months: HR 1.81, p=0.024; TTN 1-2.99 months: HR 3.75, p<0.001 vs. undetectable nadir and TTN 3-6 months). Among men with a detectable PSA at 1-3 months, 53% had a lower follow-up PSA 3-6 months after RP which was undetectable in 32% and lower but still detectable in 21%. CONCLUSIONS: In the post-RP setting, men with both a detectable nadir and a shorter TTN had an increased risk of BCR. Intriguingly, about half of the men with a detectable PSA in the first 3 months after RP had a lower follow-up PSA between 3 and 6 months after RP. If confirmed in future studies, this has important implications for patients considering adjuvant therapy based upon post-operative PSA values in the first 3 months after RP."

#pre-processing regimen: tokenization, sentence-splitting, pos-tagging, lemmatization,

def getWordFrequency(self,lines, words):
    for line in lines:
        line = line.strip()
        if line == "": break
        count = 1
        split = line.split("\t")
        if (len(split) == 3):
            lemma = splicountWordt[2].strip().lower()
        else:
          print line
        if (words.has_key(lemma)):
            count = words[lemma] + 1
        words[lemma] = count
    return words