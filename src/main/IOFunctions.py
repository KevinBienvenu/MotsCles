# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2016

@author: Kévin Bienvenu
'''

import urllib
import urlparse
import unidecode
from HTMLParser import HTMLParser

from main.TextProcessing import tokenizeFromArrayOfTxt, nltkprocess


def saveDict(dic,filename):
    with open(filename,'w') as fichier:
        for item in dic.items():
            print item[0]
            fichier.write(str(item[0].encode("utf-8"))+"-"+str(item[1])+"\n")

def importDict(filename):
    dic = {}
    with open(filename,'r') as fichier:
        for line in fichier:
            tab = line.split("-")
            dic[tab[0]] = tab[1]
            
def extractNAFDesc(codeNAF):
    page = urllib.urlopen("http://www.insee.fr/fr/methodes/default.asp?page=nomenclatures/naf2008/n5_"+codeNAF+".htm")
    s = page.read().decode("iso8859_1")
    s = HTMLParser().unescape(s)
    toComprend = True
    comprend = []
    comprendpas = []
    pair = 1
    while s.find("<tr>")!=-1:
        if pair%2==0:
            s1 = s[s.find("<tr>")+4:s.find("</tr>")]
            while s1.find("<td>")!=-1:
                if toComprend:
                    comprend.append(s1[s1.find("<td>")+4:s1.find("</td>")])
                else:
                    comprendpas.append(s1[s1.find("<td>")+4:s1.find("</td>")])
                s1 = s1[s1.find("</td>")+6:]
        else:
            s1 = s[s.find("<tr>")+4:s.find("</tr>")]
            toComprend = not("pas" in s1)  
        s = s[s.find("</tr>")+6:]
        pair+=1
    if len(comprend)>0:
        comprend = nltkprocess(comprend[0])
    if len(comprendpas)>0:
        comprendpas = nltkprocess(comprendpas[0])
    return (codeNAF,comprend,comprendpas)
                    
def getNbResultBing(searchword):
    while searchword.find(" ")!=-1:
        searchword = searchword[:searchword.find(" ")]+"+"+searchword[searchword.find(" ")+1:]
    while searchword.find(",")!=-1:
        searchword = searchword[:searchword.find(",")]+searchword[searchword.find(",")+1:]
    url = unidecode.unidecode("https://www.bing.com/search?q="+searchword)
    page = urllib.urlopen(url)
    for line in page:
        i = line.find(" results<")
        if i!=-1:
            s = line[i-13:i]
            s = s[s.find(">")+1:]
            while s.find(",")!=-1:
                s = s[:s.find(",")]+s[s.find(",")+1:]
    return int(s)
                   
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                