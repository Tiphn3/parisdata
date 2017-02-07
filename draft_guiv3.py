# -*- coding: utf-8 -*-
from __future__ import division
"""
Created on Sat Feb 04 02:08:58 2017

@author: Tiphaine
"""

from PyQt4 import QtGui,QtCore,QtWebKit
import pyqtgraph as pg
import numpy as np

import requests
from key import key # Pb: sans ma cle on ne peut pas faire tourner le code
from builtins import str
# for python 3 compatibility (see http://python-future.org/compatible_idioms.html#unicode)
import json
import webbrowser

APP = QtGui.QApplication.instance()


if APP == None:
    APP = QtGui.QApplication(["parisdata"])
    

############################### Version 3 #####################################
# 1) Ajout d'un nouveau widget : maintenant google maps s'ouvre dans l'interface
# graphique
# 2) les donnees velib telechargees contiennent 100 lignes (contre 10 par defaut)
###############################################################################


class Pw(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, parent=None)
        self.resize(1100,900)
        self.setWindowTitle("Graphe dans un widget")
        
        self.layout = QtGui.QGridLayout()   
        self.setLayout(self.layout)
        
        self.html = QtWebKit.QWebView()
        self.layout.addWidget(self.html)
        
        # Donnees Velib ParisData (100 lignes)
            # url : "https://opendata.paris.fr/api/records/1.0/search?dataset=
            # stations-velib-disponibilites-en-temps-reel"
        self.r = requests.get("https://opendata.paris.fr/api/records/1.0/search?dataset=stations-velib-disponibilites-en-temps-reel&rows=100")
        self.dvelib = self.r.json()
        
        # Line Edit for method Velib_arrondissement
        self.l1 = QtGui.QLineEdit()
        self.l1.setObjectName("arrondissement")
        self.l1.setText(u"Numéro d'arrondissement")
        self.layout.addWidget(self.l1)
        
        # Menu deroulant _  Velib par arrondissement
        self.cb1 = QtGui.QComboBox()
        self.cb1.addItems([str(i+1) for i in range(20)])
        self.cb1.currentIndexChanged.connect(self.velib_arrondissement)
        self.layout.addWidget(self.cb1)
        
        # Line Edit Resultats de recherche
        self.l2 = QtGui.QLineEdit()
        self.l2.setObjectName(u'Résultats')
        self.l2.setText(u'Résultats')
        self.layout.addWidget(self.l2)
        
        # Menu deroulant des resultats
        self.cb2 = QtGui.QComboBox()
        self.layout.addWidget(self.cb2)
        # Menu deroulant du nombre de velibs disponibles
        self.cb3 = QtGui.QComboBox()
        self.layout.addWidget(self.cb3)
        
        # url issus du site Google developers
        self.search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        self.details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    
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
            self.cb3.addItems([str(velibdispo)])
            self.cb2.addItems([str(loc)])
            self.cb2.currentIndexChanged.connect(self.googlemap)
#            self.cb2.addItems([unicode(items) for items in info.items()])
#            self.cb2.currentIndexChanged.connect(self.googlemap)
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
        self.search_req = search_req
        search_json = search_req.json()
        self.search_json = search_json
        
        place_id = search_json["results"][0]["place_id"]
        
        details_payload = {"key": key, "placeid": place_id}
        details_resp = requests.get(self.details_url, params=details_payload)
        details_json = details_resp.json()
    
        url = details_json["result"]["url"]
        self.html.load(QtCore.QUrl(url))
        self.html.show()


test = Pw()
test.show()

if __name__=="main":
    APP.exec_()
# Si le code est executé en mode standalone, la boucle d'application doit être lancée 
#pour que le code ne retourne pas immédiatement sans rien faire...

