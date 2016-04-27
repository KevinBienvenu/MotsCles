# -*- coding: utf-8 -*-
'''
Created on 27 avr. 2016

@author: Kévin Bienvenu
'''

import codecs
import os
from main import IOFunctions

path0 = "C:/Users/Utilisateur/Documents/GitHub/MotsCles"

path1 = "C:/Users/KevinBienvenu/Documents/GitHub/MotsCles"

os.chdir(path1)

# first step compute normalization of kompass terms
dicMainClasses = {}
dicSubClasses = {}
dicArborescence = {}
with codecs.open("mots-cles-kompass.txt","r","utf-8") as fichier:
    total = len(fichier.readlines())
with open("mots-cles-kompass.txt","r") as fichier:
    lastClass = ""
    percent = 1
    j=0
    for line in fichier:
        j+=1
        if 100.0*j/total>percent:
            print percent,"% -",
            percent+=1
            if percent%10==0:
                print ""
        if len(line)>10 and line[:4]=="    " and line[4:8]!="    ":
            term = line[4:-1].lower()
            lastClass = term
            dicMainClasses[term] = max([IOFunctions.getNbResultBing(term) for i in range(10)])
        elif len(line)>10 and line[:8]=="        ":
            term = line[8:-1].lower()
            dicArborescence[term] = lastClass
            dicSubClasses[term] = max([IOFunctions.getNbResultBing(term) for i in range(5)])
print "done"
IOFunctions.saveDict(dicMainClasses, "dicMainClasses.txt")
IOFunctions.saveDict(dicSubClasses, "dicSubClasses.txt")
IOFunctions.saveDict(dicArborescence, "dicArborescence.txt")
