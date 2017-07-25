import os
import codecs

utf8 = False


def writeToFile(text, filepath):
    print "writing: " + filepath
    if (utf8):
        with codecs.open(filepath, 'w', 'UTF-8') as f:
            f.write(text)
            f.close()
    else:
        with open(filepath, 'w') as f:
            f.write(text)
            f.close()


def convertDicToList(dic):  # sorts the keys in order then returns a list of values according to that order
    retList = []
    sortedKeys = sorted(dic.keys())
    # print "size of sorted keyes: " + str(len(sortedKeys))
    for key in sortedKeys:
        retList.append(dic[key])
    # print "size of returnList " + str(len(retList))
    return retList


def openFileAsLines(filepath):
    return readFileAsString(filepath).splitlines()


def fileExisits(filePath):
    return os.path.isfile(filePath)


def readFileAsString(filePath):
    if (utf8):
        return codecs.open(filePath, "r", 'utf-8').read()
    else:
        return open(filePath).read()


def removeIfExisits(filePath):
    if os.path.isfile(filePath):
        os.remove(filePath)
        print "removed : " + filePath
    else:
        print filePath + " doesn't exist"


def incrmentDic(dic, keyToAdd):
    value = 1
    if (keyToAdd in dic.keys()):
        value = dic[keyToAdd] + 1
    dic[keyToAdd] = value


def listToString(inputlist, delmiter):
    retStr = ""
    for item in inputlist:
        if (not item): continue
        retStr += str(item) + delmiter
    return retStr


def dicToStr(dic):
    retStr = ""
    keys = dic.keys()
    for i in range(0, len(keys)):
        retStr += str(i) + "\t" + str(dic[keys[i]]) + "\t" + keys[i] + "\n"
    return retStr


def removeEmptyItemsFromList(originalList):
    newList = []
    for item in originalList:
        item = item.strip()
        if (item == None or item == ""): continue
        newList.append(item)
    return newList


def stringToDict(dicStr):
    retDic = {}
    for line in dicStr.splitlines():
        splits = line.split("\t")
        key = splits[2].strip()
        value = splits[1].strip()
        retDic[key] = value

    return retDic


def stringToList(inputStr, delemiter, delemiterGoesFirst=False):
    retList = []
    for item in inputStr.split(delemiter):
        item = item.strip()
        retList.append(item)
    if (delemiterGoesFirst):
        retList = retList[1:]  # remove first item which is always empty string
    else:
        retList = retList[:-1]  # remove last item which is always empty string
    return retList


def isEmptyList(alist):
    if not isinstance(alist, list): raise ValueError("instance must be a list")
    if not alist: return 1
    if (len(alist) == 0): return 1
    for item in alist:
        if item.strip() != "":
            return 0
    return 1


def createDirIfNotExist(path):
    if not os.path.exists(path):
        print "creating dir :" + path
        os.makedirs(path)