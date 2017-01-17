# -*- coding: utf-8 -*-
from __future__ import division
"""
Created on Tue Jan 17 11:21:15 2017

@author: Tiphaine
"""
import requests
import json

#########################  Traitement des donnees du site ParisData #######################

### Telechargement des donnees _ data velib => dvelib
r = requests.get("https://opendata.paris.fr/api/records/1.0/search?dataset=stations-velib-disponibilites-en-temps-reel")
dvelib = r.json()

# Les donnees velib obtenues sont les memes qu'avec le urlretrieve, a la difference qu'aucun fichier n'est
# enregistre et a ouvrir

###### Titre du jeu de donnees
titre = str(dvelib['parameters']['dataset'][0])
titre = titre.capitalize()
titre = titre.split('-')
titre = ' '.join(titre)
print titre


###### Extraction du nombre de velos disponibles par arrondissement
def velib_arrondissement(donnees,arrondissement):
    """ revoie un dictionnaire dont les cles sont les adresses des stations de velib
    et les valeurs sont le nombre de velib disponibles
    
    entree : le jeu de donnees a considerer et le numero de l'arrondissement d'interet
    sortie : le dictionnaire
    """
    arrondissement = str(arrondissement)
    N = len(donnees['records'])
    info = dict()
    # Construction du dictionnaire
    for i in range(N):
        if str(donnees['records'][i]['fields']['number'])[:2] == arrondissement :
            loc        = str(donnees['records'][i]['fields']['address'])
            velibdispo = donnees['records'][i]['fields']['available_bikes']
            info[loc]  = velibdispo
    return info

## Test 
print velib_arrondissement(dvelib,13)





####### Extraction du nombre de velib disponibles a une adresse demandée
# Dans l'idee il suffirait de rentrer une partie de l'adresse d'une station velib pour
# obtenir le nombre de velib disponibles

def velib_par_station(donnees,station):
    """ Connaitre le nombre de velos disponibles dans une station. Il suffit de connaitre
    en partie l'adresse de cette station. Par exemple pour la station se trouvant 52 rue Raffet
    75016 Paris, il suffit de se rappeler 'Raffet'
    
    entree : le jeu de donnees a considerer et le nombre de la station
    sortie : l'adresse de la station et le nombre de velos disponibles
    """
    N = len(donnees['records'])
    for i in range(N):
        if station.upper() in donnees['records'][i]['fields']['address']:
            return donnees['records'][i]['fields']['address'],\
            'Velib disponibles :', donnees['records'][i]['fields']['available_bikes']
        else : 
            return u'Aucune station trouvée à ce nom'

## Test
print velib_par_station(dvelib,'raffet')

#### Idees

## Placer le nombre de velib disponibles sur une carte

## Tracer un histogramme

## Courbe d'evolution du nombre de velos dispos en fonction du temps dans une station

## Trouver peut etre un lien avec Google Map pour se rendre a une station
