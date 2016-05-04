# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2016

@author: Kévin Bienvenu
'''

import urllib
import urlparse
import codecs
import unidecode
from HTMLParser import HTMLParser

from main.TextProcessing import tokenizeFromArrayOfTxt, nltkprocess



def saveDict(dic,filename):
    with open(filename,'w') as fichier:
        for item in dic.items():
            fichier.write(str(item[0])+"-"+str(item[1])+"\n")

def importDict(filename):
    dic = {}
    with codecs.open(filename,'r','utf-8') as fichier:
        for line in fichier:
            tab = line.split("-")
            s = tab[0]
            for i in range(1,len(tab)-1):
                s+=tab[i]
            dic[s] = tab[-1]
    return dic
            
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
                    
def getNbResultBing(searchword, toPrint=False):
    while searchword.find(" ")!=-1:
        searchword = searchword[:searchword.find(" ")]+"+"+searchword[searchword.find(" ")+1:]
    while searchword.find(",")!=-1:
        searchword = searchword[:searchword.find(",")]+searchword[searchword.find(",")+1:]
    url = ("https://www.bing.com/search?q="+unidecode.unidecode(searchword))
    s = "-1"
    if toPrint:
        print "requete bing:",searchword,"-",
    try:
        page = urllib.urlopen(url)
        for line in page:
            i = line.find(" results<")
            if i!=-1:
                s = line[i-13:i]
                s = s[s.find(">")+1:]
                while s.find(",")!=-1:
                    s = s[:s.find(",")]+s[s.find(",")+1:]
    except:
        print "erreur"
        pass
    if toPrint:
        print int(s),"résultats"
    return int(s)
                   
def saveGraphNode(graphNode, filename):
    with codecs.open(filename,"w","utf-8") as fichier:
        for node in graphNode:
            fichier.write(str(node)+"_"+graphNode[node][0]+"_"+str(graphNode[node][1])+"_")
            for codeNAF in graphNode[node][2]:
                fichier.write(str(codeNAF)+"-"+str(graphNode[node][2][codeNAF]))
                fichier.write(",")
            fichier.write("\n")

def importGraphNode(filename):
    graphNode = {}
    dicIdNode = {}
    with codecs.open(filename,"r","utf-8") as fichier:
        for line in fichier:
            tab = line.split("_")
            dicIdNode[tab[1]] = int(tab[0])
            graphNode[int(tab[0])] = [tab[1],float(tab[2]),{}]
            for element in tab[3].split(','):
                tab1 = element.split("-")
                if len(tab1)>1:
                    graphNode[int(tab[0])][2][tab1[0]] = float(tab1[1])
    return graphNode

def saveGraphEdge(graphEdge, filename):
    with codecs.open(filename,"w","utf-8") as fichier:
        for node in graphEdge:
            fichier.write(str(node[0])+"_"+str(node[1])+"_"+'%.2f' %str(graphEdge[node])+"\n")
                    
def importGraphEdge(filename): 
    graphEdge = {}
    with codecs.open(filename,"r","utf-8") as fichier:
        for line in fichier:
            if len(line)>3:
                tab = line.split("_")
                graphEdge[(tab[0],tab[1])]=int(tab[2])
    return graphEdge
                             
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                