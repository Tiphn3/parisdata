# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 19:59:43 2017

@author: ak
"""

#Le but du code est de se familiariser avec les données du site et d'éssayer
# de commencer a les mettre en forment

from __future__ import division
import requests
import json
import numpy as np

#Recupération des données sur site
r = requests.get("http://opendata.paris.fr//api/records/1.0/search?dataset=stations-velib-disponibilites-en-temps-reel")
#Transformation en dico
dico = r.json()

#Creation d'un ficher, pour réorganiser les données qui nous intéréssent
f = open('NbVLib_fct_station','w')

#Boucle qui selectionne Nombre de Vélos disponibles par station
for n in xrange(len(dico['records'])):
 data = [str(dico['records'][n]['fields']['name']),str(dico['records'][n]['fields']['available_bikes'])]
 f.write(data[0])
 f.write(data[1])
 f.write('\n')
f.close() 

#Commentaire: J'ai taper ce code dans le but d'éssayer d'organiser le ficher
# recu par le site Paris Data, dans l'exemple j'ai sélectionné le nombres de
# vélos par station et l'ai inscrit dans un fichier.

#Suite possible? : Peut être allez plus loin et isoler le nombre de  vélo
#par stations et s'amuser à tracer un graphe qui indique en fonction du temps
# le nombre de vélo disponible pour une station choisie par l'utilisateur (en
# réactulisant réguliérement les données du site)
 

 