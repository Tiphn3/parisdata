# -*- coding: utf-8 -*-
from __future__ import division
"""
Created on Wed Jan 11 11:45:00 2017

@author: Tiphaine
"""

import urllib
import json
import csv

# Utilisation de json
dico = {4:['coucou',False,45]}
string = json.dumps(dico)
json.loads(string)

#################################################################################

# Lire le code source d'un site web dans Python                                 
sock = urllib.urlopen("http://diveintopython.net/") 
htmlSource = sock.read()                            
sock.close()                                        
print htmlSource 

#################################################################################

# Telecharger un fichier pdf a partir d'une page web
urllib.urlretrieve('http://math.univ-toulouse.fr/~besse/Wikistat/pdf/st-intro.pdf', \
 "Statistique_introduction.pdf")

# un fichier csv
urllib.urlretrieve('https://opendata.paris.fr/explore/dataset/stations-velib-disponibilites-en-temps-reel/export/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6InN0YXRpb25zLXZlbGliLWRpc3BvbmliaWxpdGVzLWVuLXRlbXBzLXJlZWwiLCJvcHRpb25zIjp7fX0sImNoYXJ0cyI6W3sidHlwZSI6ImJhciIsImZ1bmMiOiJBVkciLCJ5QXhpcyI6Im51bWJlciIsInNjaWVudGlmaWNEaXNwbGF5Ijp0cnVlLCJjb2xvciI6IiM2NmMyYTUifV0sInhBeGlzIjoibGFzdF91cGRhdGUiLCJtYXhwb2ludHMiOiIiLCJ0aW1lc2NhbGUiOiJ5ZWFyIiwic29ydCI6IiJ9XX0%3D/stations-velib-disponibilites-en-temps-reel.csv',\
'velib.csv')

# PROBLEME
# un fichier csv (ou xls ou json) est telecharge, mais il ne correspond pas au fichier telecharge lorsque l'on 
# clique sur le lien du site parisdata.fr
