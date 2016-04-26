# -*- coding: utf-8 -*-
'''
Created on 25 avr. 2016

@author: Kévin Bienvenu
'''

import IOFunctions

# dic = {"vané".decode("utf-8"):1,"éé".decode("utf-8"):2}
#  
# IOFunctions.saveDict(dic, "a.txt")

s = "lskdgj8sdf6"

se = set(range(10))

for c in s:
    try:
        int(c)
        print "vaneau"
    except:
        continue