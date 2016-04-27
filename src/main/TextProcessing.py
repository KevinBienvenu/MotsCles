# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2016

@author: Kévin Bienvenu
'''

import codecs
from nltk.corpus import stopwords
import nltk.stem.snowball
import numpy as np

def extractFromTxt(filename,toDisplay = False):
    '''
    function that extract text from a textfile and return an array of strings
    '''
    with codecs.open(filename,'r','utf-8') as fichier:
        lines = []
        if toDisplay:
            print "reading file",filename
        for line in fichier:
            lines.append(line)
        if toDisplay:
            print "...done"
    return lines

def tokenizeFromArrayOfTxt(array, toDisplay=False):
    lines = []
    percent = 1
    total = len(array)
    i = 0
    for stri in array:
#         if i>10:
#             break
        i+=1
        if toDisplay and 100.0*i/total>percent:
            print percent,".",
            if percent%10==0:
                print ""
            percent+=1
        if str(stri[0])!="nan":
            lines.append(nltkprocess(str(stri[0])))
    return lines

def nltkprocess(srctxt):
    french_stopwords = set(stopwords.words('french'))
    stem = nltk.stem.snowball.FrenchStemmer()
    tokens = nltk.word_tokenize(srctxt.decode('utf8').lower(),'french')
    tokens = [token for token in tokens if len(token)>1 and token not in french_stopwords]
    stems = []
    for token in tokens:
        stems.append(stem.stem(token))
    return stems
     
def computeDictToken(lines, dictToken = {}):  
    for line in lines:
        for word in line:
            if not(word in dictToken):
                dictToken[word] = 0
            dictToken[word] += 1
    toRemove = []
    for entry in dictToken.items():
        if entry[1]<=2:
            toRemove.append(entry[0])
            continue
        for c in entry[0]:
            try:
                int(c)
                toRemove.append(entry[0])
            except:
                continue
    for toR in toRemove:
        if toR in dictToken.keys():
            del dictToken[toR]
    return dictToken

                         

    