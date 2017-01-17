# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 16:21:24 2017

@author: A.K.
"""

from __future__ import division
import requests
import json
import numpy as np
import time
import matplotlib.pyplot as plt

#Vecteur temps - (chaqu minute)
temps = np.arange(time.time(),time.time()+3600,60)
#creation d'un vecteur qui prendera le nombre de vélo dispo
Nb_Bike = np.ones(60)

for n in xrange(60):
        #Recupération des données sur site
        r = requests.get("http://opendata.paris.fr//api/records/1.0/search?dataset=stations-velib-disponibilites-en-temps-reel")
        #Transformation en dico
        dico = r.json()
        
        
        #Données utilisées(le nom de la station n'est pas forcément nécessaire )
        name_station = str(dico['records'][6]['fields']['name'].encode('utf-8'))
        Nb_Bike[n] = int(dico['records'][6]['fields']['available_bikes'])
        

        time.sleep(60)
        
plt.plot(temps,Nb_Bike)
#Commentaire : Je transformmerais prochainement le code en fonction
