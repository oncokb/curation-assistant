#Command to start StanfordNLP server (see below)
#java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

from pycorenlp import StanfordCoreNLP
import subprocess
import os

nlp = StanfordCoreNLP('http://locahost:9000')

sample_abstract = "OBJECTIVES: To evaluate the association between PSA nadir level and time to nadir (TTN) with biochemical recurrence (BCR) risk after radical prostatectomy (RP) in the SEARCH database. METHODS: Retrospective analysis of 1,939 men from the SEARCH database treated with RP between 1998-2015 with available ultrasensitive PSA nadir within 1-6 months after RP. Uni- and multivariable analyses of PSA nadir and TTN with time from nadir to BCR were done with Cox models (adjusted for demographics, tumor features and preoperative PSA). RESULTS: Among men with an undetectable PSA nadir, the TTN was unrelated to BCR (1-2.9 vs. 3-6 months: HR 0.86, p=0.46). Regardless of TTN, men with detectable nadir had increased risk of BCR (TTN 3-6 months: HR 1.81, p=0.024; TTN 1-2.99 months: HR 3.75, p<0.001 vs. undetectable nadir and TTN 3-6 months). Among men with a detectable PSA at 1-3 months, 53% had a lower follow-up PSA 3-6 months after RP which was undetectable in 32% and lower but still detectable in 21%. CONCLUSIONS: In the post-RP setting, men with both a detectable nadir and a shorter TTN had an increased risk of BCR. Intriguingly, about half of the men with a detectable PSA in the first 3 months after RP had a lower follow-up PSA between 3 and 6 months after RP. If confirmed in future studies, this has important implications for patients considering adjuvant therapy based upon post-operative PSA values in the first 3 months after RP."

#pre-processing regimen: tokenization, sentence-splitting, pos-tagging, lemmatization,

raw_output = nlp.annotate(sample_abstract, properties={'annotators': 'tokenize,ssplit,pos,lemma,parse','outputFormat': 'json'})

import util

def runCmd(cmd):#try to do this directly with the OpenNLP or StanfordNLP server
    print cmd
    p = subprocess.Popen(cmd, stdin=None, stdout = None, shell=True)
    os.popen(cmd)
    p.wait()

#this function has to be HEAVILY revised bc. we are using different tools
def processAbstract_txt(absid, sens, outpath):   #assumes /txt/ directory exisits, and we are processing files from there.
    posInput = preparePOSInput(sens)
    posInputPath = outpath + "/txt/" + absid + ".txt"
    #utility.writeToFile(posInput, posInputPath)
    posOutTemp = outpath + "/posOutTemp/" +absid+".txt"
    posCmd = "~/bin/pos --model ~/BIO/CC/models/pos_bio/ --maxwords 1000 --input " + posInputPath + " --output " + posOutTemp
    runCommand(posCmd)
    #~/bin/parser --parser ~/BIO/CC/models/parser/ --super ~/BIO/CC/models/super_bio/ --input /home/sb895/BIO/data/cc/tagOut.txt --output /home/sb895/BIO/data/cc/parserOut.txt
    parseCCOutPath = outpath + "/ccOut/" + absid + ".cc.txt"
    parseCmd = "~/bin/parser --parser ~/BIO/CC/models/parser/ --super ~/BIO/CC/models/super_bio/ --parser-maxsupercats 900000 --parser-maxwords 1000 --input " + posOutTemp + " --output " + parseCCOutPath
    runCommand(parseCmd)
    [posOut,parseOut]=processCCParse(parseCCOutPath)
    posOutPath = outpath + "/pos/" + absid + ".pos.txt"
    parseOutPath = outpath + "/parse/" + absid + ".parse.txt"
    utility.writeToFile(posOut,posOutPath)
    utility.writeToFile(parseOut,parseOutPath)
    doLemma(posOutPath,absid,outpath)

def start(dataPath,outpath, start_at_middle):

    print"starting cc script!"
    count = 0;
    lines = open(dataPath).read().splitlines()
    newAbsList = []

    util.createDirIfNotExist(outpath + "/txt/")
    util.createDirIfNotExist(outpath + "/pos/")
    util.createDirIfNotExist(outpath + "/parse/")
    util.createDirIfNotExist(outpath + "/lem/")
    util.createDirIfNotExist(outpath + "/posOutTemp/")

    print lines[0]

    for line in lines:
        if(not line.startswith("^")):
           absid = line.strip()
        else:
            count += 1
            if(isNewAbs(absid,outpath)):
                sens = line.split("^")
                sens = cleanInput(sens)
                if(utility.isEmptyList(sens)):
                    print absid + " has empty abstract"
                    continue
                newAbsList.append(abs)

                print str(count) + ": " + absid
                utility.incrmentDic(inputAlignmentDic,absid)
                processAbstract(absid, sens,outpath)
                if(start_at_middle):
                    print "working normal from the middle !!"
                else:
                    print "normal processing !"
            else:
                print str(count) + " skipping: " + absid



    #checkOutputAlignment(inputAlignmentDic)
