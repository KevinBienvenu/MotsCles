# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2016

@author: Kévin Bienvenu
'''


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