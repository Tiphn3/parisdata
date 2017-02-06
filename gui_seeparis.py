# -*- coding: utf-8 -*-
from __future__ import division

"""
Created on Mon Feb 06 09:49:04 2017

@author: Tiphaine
"""

from PyQt4 import QtGui,QtCore,QtWebKit
import pyqtgraph as pg
import numpy as np
import json
#import webbrowser

import requests
from key import key # Pb: sans ma cle on ne peut pas faire tourner le code


APP = QtGui.QApplication.instance()

if APP == None:
    APP = QtGui.QApplication(["parisdata"])
    

############################### Version 4 #####################################
# 1) Ajout d'un nouveau widget : maintenant google maps s'ouvre dans l'interface
# graphique
# 2) les donnees velib telechargees contiennent un nombre ajustable de lignes 
# (contre 10 par defaut)
# 4) Voir les arbres remarquables de Paris. A terme, l'objectif est de rajouter 
# egalement la carte des cinemas et musees a Paris
# 5) Prochaine etape : rajouter un histogramme du nombre moyen de velib 
# disponibles dans un arrondissement.
###############################################################################


class SeeParisGui(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, parent=None)
        self.resize(1300,900)
        self.setWindowTitle(u"Visitez Paris à vélo")
        
        self.layout = QtGui.QGridLayout()   
        self.setLayout(self.layout)
        
        # Widget internet : ajoute sur le gui avec sa position dans le gui
        self.html = QtWebKit.QWebView()
        self.layout.addWidget(self.html,0,1)
        
        # Donnees Velib ParisData (100 lignes)
            # url : "https://opendata.paris.fr/api/records/1.0/search?dataset=
            # stations-velib-disponibilites-en-temps-reel"
        self.r = requests.get("https://opendata.paris.fr/api/records/1.0/search?dataset=stations-velib-disponibilites-en-temps-reel&rows=500&sort=last_update")
        self.dvelib = self.r.json()
        
        # Line Edit for method Velib_arrondissement
        self.l1 = QtGui.QLineEdit()
        self.l1.setObjectName("arrondissement")
        self.l1.setText(u"Numéro d'arrondissement")
        self.layout.addWidget(self.l1,0,0)
        
        # Menu deroulant _  Velib par arrondissement
        self.cb1 = QtGui.QComboBox()
        self.cb1.addItems([unicode(str(i+1)) for i in range(20)])
        self.cb1.currentIndexChanged.connect(self.velib_arrondissement)
        self.layout.addWidget(self.cb1,1,0)
        
        # Line Edit Resultats de recherche
        self.l2 = QtGui.QLineEdit()
        self.l2.setObjectName(u'Résultats')
        self.l2.setText(u'Résultats')
        self.layout.addWidget(self.l2,2,0)
        
        # Menu deroulant des resultats
        self.cb2 = QtGui.QComboBox()
        self.layout.addWidget(self.cb2)
        # Menu deroulant du nombre de velibs disponibles
        self.cb3 = QtGui.QComboBox()
        self.layout.addWidget(self.cb3,3,0)
        
        # url issus du site Google developers
        self.search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        self.details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        # Arbres remarquables de Paris : bouton a cliquer pour voir
        self.button1 = QtGui.QPushButton(u'Arbres remarquables à Paris')
        self.layout.addWidget(self.button1,4,0)
        self.button1.clicked.connect(self.arbres_remarquables)
    
    # Methods             
    def velib_arrondissement(self):
        """ revoie un dictionnaire dont les cles sont les adresses des stations
        de velib et les valeurs sont le nombre de velib disponibles
        
        entree: le jeu de donnees a considerer et le numero de l'arrondissement
                 (abbrévié 'arrdt') d'interet
        sortie: le dictionnaire
        """
        try:
            numero = self.cb1.currentText()
            arrdt = str(numero)
            N = len(self.dvelib['records'])
            info = dict()
            self.cb2.clear()
            self.cb3.clear()
            # Construction du dictionnaire
            for i in range(N):
                if int(str(self.dvelib['records'][i]['fields']['name'][:2])) == int(arrdt) :
                    loc        = str(self.dvelib['records'][i]['fields']['address'])
                    velibdispo = self.dvelib['records'][i]['fields']['available_bikes']
                    info[loc]  = velibdispo
#            print (info)
            self.cb3.addItems([unicode(velibdispo)])
            self.cb2.addItems([unicode(loc)])
            self.cb2.currentIndexChanged.connect(self.googlemap)

        except:
            print (u"Rentrez un numéro d'arrondissement")
    
    def googlemap(self):
        """ La fonction construit un url avec lequel webbrowser ouvre la page
        google map correspondante. Les donnees google map viennent du site Google
        developers, mais il faut une cle.
        
        entree: l'adresse d'une station velib
        sortie: l'url google map de cette adresse et ouverture d'une page internet
        """
        query = self.cb2.currentText()
        search_payload = {'key': key, 'query': query}
        search_req = requests.get(self.search_url, params=search_payload )
        search_json = search_req.json()
        
        place_id = search_json["results"][0]["place_id"]
        
        details_payload = {"key": key, "placeid": place_id}
        details_resp = requests.get(self.details_url, params= details_payload)
        details_json = details_resp.json()
    
        url = details_json["result"]["url"]
        self.html.load(QtCore.QUrl(url))
        self.html.show()
        
    def arbres_remarquables(self):
        """ Cette fonction affiche dans un widget la carte ParisData des arbres
        remarquables de paris
        entree : il suffit d'appeler la fonction
        sortie : la carte affichee dans un widget du module QWebKit
        """
        url = "https://opendata.paris.fr/explore/embed/dataset/arbresremarquablesparis2011/map/?location=12,48.85611,2.34953&static=false&datasetcard=false"
        
        self.html.load(QtCore.QUrl(url))
        self.html.show()



ouverture = SeeParisGui()
ouverture.show()

if __name__=="main":
    APP.exec_()
# Si le code est executé en mode standalone, la boucle d'application doit être lancée 
#pour que le code ne retourne pas immédiatement sans rien faire...

