# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2016

@author: Kévin Bienvenu
'''

import pandas as pd
import os
import TextProcessing as txtpr
import IOFunctions
import operator

path0 = "C:/Users/Utilisateur/Google Drive/Camelia Tech/Donnees entreprise/Agregation B Reputation"
path0a = "C:/Users/Utilisateur/Documents/GitHub/MotsCles/tests"

path1 = "C:/Users/Kévin/Google Drive/Camelia Tech/Donnees entreprise/Agregation B Reputation"
path1a = "C:/Users/Kévin/Documents/GitHub/MotsCles/tests"

os.chdir(path0)
 
 
direc = os.listdir(".")

for fichier in direc:
    if fichier[:11]!="BRep_Step2_" or fichier[-3:]!="csv":
        continue
    print "extraction du fichier ",fichier,
    db = pd.read_csv(fichier,usecols=['description'])
    print " done"
    print "tokenization..."
    lines = txtpr.tokenizeFromArrayOfTxt(db.values, True)
    print "... done"
    print "computing dictionary...",
    dictStemTokens = {}
    dictStemTokens = txtpr.computeDictToken(lines,dictStemTokens)
    print " done"
    lines = []
    print ""
    
os.chdir(path0a)
    
IOFunctions.saveDict(dictStemTokens, "dicFreqTokens.txt")

# dictStemTokens = IOFunctions.importDict("dicFreqTokens.txt")
# 
# print "sorting...",
#  
# dictStemTokens = sorted(dictStemTokens.items(), key=operator.itemgetter(1),reverse=True)
#  
# print " done"
# 
# for i in range(50):
#     print dictStemTokens[i][0],dictStemTokens[i][1]



