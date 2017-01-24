# -*- coding: utf-8 -*-
from __future__ import division
"""
Created on Sun Jan 22 17:20:39 2017

@author: Tiphaine
"""

import pyqtgraph as pg
import numpy as np
from PyQt4 import QtGui,QtCore
import requests
#import json

#app = pg.mkQApp()

class Pw(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, parent=None)
        self.resize(900,800)
        self.setWindowTitle("Graphe dans un widget")
        
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        
        self.plot = pg.PlotWidget(title=u"Données aléatoires")
        self.layout.addWidget(self.plot,0,1)
        
        # Donnees Velib ParisData
        self.r = requests.get("https://opendata.paris.fr/api/records/1.0/search?dataset=stations-velib-disponibilites-en-temps-reel")
        self.dvelib = self.r.json()

        
        # First button
        self.button = QtGui.QPushButton(u"Nouvelle prise de données",self)
        self.button.clicked.connect(self.plotGraph)
        self.layout.addWidget(self.button,0,0)
        
        # Line Edit for method Velib_arrondissement
        self.l1 = QtGui.QLineEdit()
        self.l1.setObjectName("arrondissement")
        self.l1.setText(u"Numéro d'arrondissement")
        self.layout.addWidget(self.l1)
        
        # Second button - Find a velib with an arrondissement number
        self.button2 = QtGui.QPushButton('Chercher', self)
        self.connect(self.button2, QtCore.SIGNAL("clicked()"), self.velib_arrondissement)
        self.layout.addWidget(self.button2)
        
        # Line Edit for method Velib_par_station
        self.l2 = QtGui.QLineEdit()
        self.l2.setObjectName("station")
        self.l2.setText("Nom de la station")
        self.layout.addWidget(self.l2)
        
        # Third button - Find a velib with a station name
        self.button3 = QtGui.QPushButton('Chercher la station',self)
        self.connect(self.button3, QtCore.SIGNAL("clicked()"), self.velib_par_station)
        self.layout.addWidget(self.button3)
    
    # Methods     
    def plotGraph(self):
        self.plot.clear()
        self.data = np.random.normal(loc=0.0,scale=2,size=100)
        self.plot.plot(self.data)
        
    def velib_arrondissement(self):
        """ revoie un dictionnaire dont les cles sont les adresses des stations de velib
        et les valeurs sont le nombre de velib disponibles
        
        entree : le jeu de donnees a considerer et le numero de l'arrondissement d'interet
        sortie : le dictionnaire
        """
        try :
            numero = self.l1.text()
            arrondissement = str(numero)
            N = len(self.dvelib['records'])
            info = dict()
            # Construction du dictionnaire
            for i in range(N):
                if str(self.dvelib['records'][i]['fields']['number'])[:2] == arrondissement :
                    loc        = str(self.dvelib['records'][i]['fields']['address'])
                    velibdispo = self.dvelib['records'][i]['fields']['available_bikes']
                    info[loc]  = velibdispo
            print(info)
        except :
            print(u"Rentrez un numéro d'arrondissement")
    
    def velib_par_station(self):
        """ Connaitre le nombre de velos disponibles dans une station. Il suffit de connaitre
        en partie l'adresse de cette station. Par exemple pour la station se trouvant 52 rue Raffet
        75016 Paris, il suffit de se rappeler 'Raffet'
        
        entree : le jeu de donnees a considerer et le nombre de la station
        sortie : l'adresse de la station et le nombre de velos disponibles
        """
        station = self.l2.text()
        station = str(station)
        counter = 0
        N = len(self.dvelib['records'])
        for i in range(N):
            if station.upper() in self.dvelib['records'][i]['fields']['address']:
                print(self.dvelib['records'][i]['fields']['address'],\
                'Velib disponibles :', self.dvelib['records'][i]['fields']['available_bikes'])
                counter += 1
            elif i == N-1 and counter == 0 : 
                print(u'Aucune station trouvée à ce nom')
            else :
                counter = counter

# creer une application Qt si elle n'existe pas encore (pour que le code puisse etre executé avec "python draft_GUI.py")
APP = QtGui.QApplication.instance()
if APP is None:
	APP = QtGui.QApplication(["parisdata"])		

test = Pw()
test.show()

if __name__=="__main__":
	APP.exec_() # Si le code est executé en mode standalone, la boucle d'application doit être lancée pour que le code ne
				# retourne pas immédiatement sans rien faire...


# Le code marche, mais il y a un petit beug au niveau de la fonction velib par station, il faut cliquer
# deux fois sur le bouton pour afficher le resultat de la recherche
