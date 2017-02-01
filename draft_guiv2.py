# -*- coding: utf-8 -*-
from __future__ import division
"""
Created on Wed Feb 01 22:17:14 2017

@author: Tiphaine
"""
from PyQt4 import QtGui,QtCore
import pyqtgraph as pg
import numpy as np

import requests
from key import key # Pb: sans ma cle on ne peut pas faire tourner le code
import json
import webbrowser

APP = QtGui.QApplication.instance()


if APP == None:
    APP = QtGui.QApplication(["parisdata"])


class Pw(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, parent=None)
        self.resize(800,600)
        self.setWindowTitle("Graphe dans un widget")
        
        self.layout = QtGui.QGridLayout()   
        self.setLayout(self.layout)
        
        self.plot = pg.PlotWidget(title=u"Données aléatoires")
        self.layout.addWidget(self.plot,0,1)
        
        # Donnees Velib ParisData
            # url : "https://opendata.paris.fr/api/records/1.0/search?dataset=
            # stations-velib-disponibilites-en-temps-reel"
        self.r = requests.get("https://opendata.paris.fr/api/records/1.0/search?dataset=stations-velib-disponibilites-en-temps-reel")
        self.dvelib = self.r.json()

        # First button
        self.button = QtGui.QPushButton(u"Nouvelle prise de données",self)
        self.button.clicked.connect(self.plot_graph)
        self.layout.addWidget(self.button,0,0)
        
        # Line Edit for method Velib_arrondissement
        self.l1 = QtGui.QLineEdit()
        self.l1.setObjectName("arrondissement")
        self.l1.setText(u"Numéro d'arrondissement")
        self.layout.addWidget(self.l1)
        
        # Menu deroulant _  Velib par arrondissement
        self.cb1 = QtGui.QComboBox()
        self.cb1.addItems([unicode(str(i+1)) for i in range(20)])
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
    def plot_graph(self):
        self.plot.clear()
        self.data = np.random.normal(loc=0.0,scale=2,size=100)
        self.plot.plot(self.data)
        
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
            # Construction du dictionnaire
            for i in range(N):
                if str(self.dvelib['records'][i]['fields']['number'])[:2] == arrdt :
                    loc        = str(self.dvelib['records'][i]['fields']['address'])
                    velibdispo = self.dvelib['records'][i]['fields']['available_bikes']
                    info[loc]  = velibdispo
#            print (info)
            self.cb3.addItems([unicode(velibdispo)])
            self.cb2.addItems([unicode(loc)])
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
        search_json = search_req.json()
        
        place_id = search_json["results"][0]["place_id"]
        
        details_payload = {"key": key, "placeid": place_id}
        details_resp = requests.get(self.details_url, params= details_payload)
        details_json = details_resp.json()
    
        url = details_json["result"]["url"]
        webbrowser.open_new(url)
        print url


test = Pw()
test.show()

if __name__=="main":
    APP.exec_()
# Si le code est executé en mode standalone, la boucle d'application doit être lancée 
#pour que le code ne retourne pas immédiatement sans rien faire...

