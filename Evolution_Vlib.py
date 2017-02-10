# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 18:59:53 2017

@author: ak
"""

import pyqtgraph as pg
import numpy as np
from PyQt4 import QtGui,QtCore
import requests
import json
import os
import time

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
        self.r = requests.get("http://opendata.paris.fr//api/records/1.0/search?dataset=stations-velib-disponibilites-en-temps-reel&rows=500")
        self.dvelib = self.r.json()
        
         # First button
        self.button = QtGui.QPushButton(u"Nouvelle prise de données",self)
        self.button.clicked.connect(self.plotGraph)
        self.layout.addWidget(self.button,0,0)
        
        self.l1 = QtGui.QLineEdit()
        self.l1.setObjectName("arrondissement")
        self.l1.setText("Numero arrondissement")
        self.layout.addWidget(self.l1)
        
    def plotGraph(self):
        self.plot.clear()
        x0,y0 = self.superhisto()
        self.data = pg.BarGraphItem(x=y0,height =x0,width=0.3)
        self.plot.addItem(self.data)
        
    def superhisto(self):
        
        #But : Trie les données d'acquisition par arrondissement
        #entré : numero arrondissement
        #sortie : 2 vecteur tps,velo 
            #tps: temps d'acquisition
            #velo: nombre de vélo dans l'arrendissement pris au temps t
        
        #NECESSAIRE : AVOIR LES DONNES D'ACQUISITION ET ADAPTER LE NOM DU
        #CHEMIN DES FICHIER 
        numero = self.l1.text()
        arr = int(numero)


        #NOM DU FICHIER
        chemin_f = '/home/ak/fac/Projet python/acqui/data'

        k=1
        Velo = []
        Tps = []

        while True :
            try:
                 #NOM DU FICHIER
               
                data =  open(chemin_f+str(k), 'r')
                Lecture_fichier = data.read()
                dico = dict(eval(Lecture_fichier))
                
                # nombre de vélo
                nb_velo = dico['records'][arr]['fields']["available_bikes"]
                
                #prendre l'heure et minute d'acquisition du fichier
                #(renvoie a sa dete de creation)
                a = os.stat(chemin_f+str(k))[8]
                heure = time.localtime(a)[3]
                minute = time.localtime(a)[4]
                temps = float(str(heure)+"."+str(minute))
                
                Tps.append(temps)
                Velo.append(nb_velo)
                k+=1
            except:
                break
        return Velo,Tps
         
         
APP = QtGui.QApplication.instance()
if APP is None:
	APP = QtGui.QApplication(["parisdata"])		

test = Pw()
test.show()


if __name__=="__main__":
	APP.exec_() 