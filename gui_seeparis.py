# -*- coding: utf-8 -*-
from __future__ import division
"""
Created on Tue Feb 07 10:29:50 2017

@author: Tiphaine
"""
import os

from PyQt4 import QtGui,QtCore,QtWebKit
import pyqtgraph as pg
import numpy as np

import requests
from key import key # Pb: sans la cle on ne peut pas faire tourner le code


APP = QtGui.QApplication.instance()

if APP == None:
    APP = QtGui.QApplication(["parisdata"])
    

############################### Version 4 #####################################
# 1) Google Maps s'ouvre dans un widget de l'interface graphique
# 2) les donnees velib telechargees contiennent un nombre ajustable de lignes 
# (contre 10 par defaut)
# 4) Plusieurs boutons : arbres remarquables, cinemas, musee
# 5) histogramme du nombre moyen de velib disponibles par arrondissement.
# 6) histogramme du nombre moyen de velib par arrdt sur une journée
###############################################################################

class SeeParisGui(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, parent=None)
        self.resize(1500,900)
        self.setWindowTitle(u"Visitez Paris à vélo")
        
        self.layout = QtGui.QGridLayout()   
        self.setLayout(self.layout)
        
        self.v_layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.v_layout,0,0)
        
        # Widget internet : affiche les differentes cartes
        self.html1 = QtWebKit.QWebView()
        self.html1.setFixedHeight(400)
        self.layout.addWidget(self.html1,0,1)
        
        # Widget internet : reserve au Google Maps
        self.html2 = QtWebKit.QWebView()
        self.html2.setFixedHeight(400)
        self.layout.addWidget(self.html2,2,1)
        
        # Plot Widget 1
        self.plotwidget = pg.PlotWidget(title=u"Données courantes")
        self.layout.addWidget(self.plotwidget,0,2)
        
        # Plot Widget 2
        self.plotwidget2 = pg.PlotWidget(title=u"Données journalières (11/02/2017)")
        self.layout.addWidget(self.plotwidget2,2,2)
        
        ############################
        
        # Donnees Velib ParisData (500 lignes, environ 3 min)
            # url : "https://opendata.paris.fr/api/records/1.0/search?dataset=
            # stations-velib-disponibilites-en-temps-reel&rows=500&sort=last_update"
        self.r = requests.get("https://opendata.paris.fr/api/records/1.0/search?dataset=stations-velib-disponibilites-en-temps-reel&rows=500&sort=last_update")
        self.dvelib = self.r.json()
        
        # Bouton Carte des velibs dans Paris
        self.button1 = QtGui.QPushButton(u"Carte des vélibs")
        self.button1.setFixedWidth(300)
        self.v_layout.addWidget(self.button1)
        self.button1.clicked.connect(self.velib_carte)
        
        # Line Edit for method Velib_arrondissement
        self.l1 = QtGui.QLabel()
        self.l1.setFixedWidth(300)
        self.l1.setText(u"Numéro d'arrondissement")
        self.v_layout.addWidget(self.l1)
        
        # Menu deroulant _  Velib par arrondissement
        self.cb1 = QtGui.QComboBox()
        self.cb1.addItems([str(i+1) for i in range(20)])
        self.cb1.setFixedWidth(300)
        self.cb1.currentIndexChanged.connect(self.velib_arrondissement)
        self.v_layout.addWidget(self.cb1)
        
         # Line Edit Resultats de recherche
        self.l2 = QtGui.QLabel()
        self.l2.setFixedWidth(300)
        self.l2.setText(u'Résultats')
        self.v_layout.addWidget(self.l2)
        
        # Menu deroulant des resultats
        self.cb2 = QtGui.QComboBox()
        self.cb2.setFixedWidth(300)
        self.v_layout.addWidget(self.cb2)
        self.cb2.currentIndexChanged.connect(self.googlemap)
        
#        # Menu deroulant du nombre de velibs disponibles
#        self.cb3 = QtGui.QComboBox()
#        self.cb3.setFixedWidth(300)
#        self.layout.addWidget(self.cb3,5,0)
        ################
        
        # Arbres remarquables de Paris : bouton a cliquer pour voir
        self.button2 = QtGui.QPushButton(u'Arbres remarquables à Paris')
        self.button2.setFixedWidth(300)
        self.layout.addWidget(self.button2,5,0)
        self.button2.clicked.connect(self.arbres_remarquables)
        
        # Salles de cinema : bouton
        self.cinebutton = QtGui.QPushButton(u"Salles de cinéma")
        self.cinebutton.setFixedWidth(300)
        self.layout.addWidget(self.cinebutton,6,0)
        self.cinebutton.clicked.connect(self.salles_de_cinema)
        
        # Musees : bouton
        self.museebutton = QtGui.QPushButton(u"Musées")
        self.museebutton.setFixedWidth(300)
        self.layout.addWidget(self.museebutton)
        self.museebutton.clicked.connect(self.musees,7,0)
        
        
        # LineEdit recherche d'adresse sur Google Maps
        self.l1 = QtGui.QLineEdit()
        self.l1.setObjectName("adresse d'une station")
        self.l1.setFixedWidth(300)
        self.l1.setText(u"Rentrez une adresse")
        self.layout.addWidget(self.l1,8,0)
        
        # bouton -Lancer la recherche google map
        self.button3 = QtGui.QPushButton('Chercher', self)
        self.button3.setFixedWidth(150)
        self.button3.clicked.connect(self.googlemap2)
        self.layout.addWidget(self.button3,8,1)
        
        # Histogramme bouton
        self.button4 = QtGui.QPushButton(u"Afficher l'histogramme")
        self.button4.setFixedWidth(300)
        self.button4.clicked.connect(self.histograph)
        self.layout.addWidget(self.button4,1,2)        
        
        # url issus du site Google developers
        self.search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        self.details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        #########################
        # Donnees temps reel - lineEdit, Bouton et plot widget
        # Bouton d'affichage 
        self.button5 = QtGui.QPushButton(u"Affichage",self)
        self.button5.clicked.connect(self.plot_graph)
        self.layout.addWidget(self.button5,4,2)
        
        # Ligne de texte
        self.l2 = QtGui.QLineEdit()
        self.l2.setObjectName("arrondissement")
        self.l2.setText(u"Numéro d'arrondissement")
        self.layout.addWidget(self.l2,3,2)
        
                
        ############################ Methods ################################
    def plot_graph(self):
        self.plotwidget2.clear()
        x0,y0 = self.superhisto()
        x0 = [(x0[i]-x0[0])/3600 for i in range(len(x0))]
        self.data = pg.BarGraphItem(x=x0,height =y0,width=0.01)
        self.plotwidget2.addItem(self.data)
        self.plotwidget2.getAxis('bottom').setLabel('Temps (H)')
        self.plotwidget2.getAxis('left').setLabel('Moyenne des velibs disponibles')
    
    def superhisto(self):
        """ But : Trie les données d'acquisition par arrondissement
        entrée : numero arrondissement
        sortie : 2 vecteur tps,velo 
            tps: temps d'acquisition
            velo: nombre de vélo dans l'arrendissement pris au temps t
        
        NECESSAIRE : AVOIR LES DONNES D'ACQUISITION ET ADAPTER LE NOM DU
        CHEMIN DES FICHIER 
        """
        numero = self.l2.text()
        arr = int(numero)

        if (arr <= 20):           

            # Chemin d'acces et nom du fichier
#            chemin_f = '/home/ak/fac/Projet python/acqui2/datta'
            chemin_f = "C:/Users/Tiphaine/Documents/COURS/PHYSIQUE/M2_LuMI/S2/Projet_informatique/Day_data/datta"

            k=1
            Velo = []
            Tps = []

            while True :
                try:
                    #NOM DU FICHIER                        
                        data =  open(chemin_f+str(k), 'r')
                        Lecture_fichier = data.read()
                        dico = dict(eval(Lecture_fichier))
                        N = len(dico["records"])
                            
                        for i in range(N):
                                if int(str(dico['records'][i]['fields']['name'][:2])) == int(arr):
                                    
                                    # nombre de vélo
                                    nb_velo = dico['records'][i]['fields']["available_bikes"]
                                    
                                    #prendre l'heure et minute d'acquisition du fichier
                                    #(renvoie a sa dete de creation)
                                    a = os.stat(chemin_f+str(k))[8]
                                    
                                    Tps.append(a)
                                    Velo.append(nb_velo)
                                    k+=1
                except:
                         break
            return Tps,Velo
        else:
            raise ValueError("""rentrez un numéro d'arrondissement valable""")
        
    def histograph(self):
        """ Trace le nombre de velibs disponibles en 'temps reel' a partir des
        donnees parisdata
        """
        # Recuperation des donnees
        try :
            arrdt_liste = []
            velibmoyen_liste = []
            velibstd_liste = []
        
            for i in range(1,21):
                velibdispo = []
                arrdt = str(i)
                N = len(self.dvelib['records'])
            
                for j in range(N):
                     if int(str(self.dvelib['records'][j]['fields']['name'][:2])) == int(arrdt):
                         velibdispo.append(self.dvelib['records'][j]['fields']['available_bikes'])
                
                velibmoyen_liste.append(np.mean(velibdispo))
                velibstd_liste.append(np.std(velibdispo))
                arrdt_liste.append(i)
        except :
            print u'pas de données'
        
        # Plot
        self.plotwidget.clear()
        histoplot = pg.BarGraphItem(x=arrdt_liste, height=velibmoyen_liste,width=0.3, brush='b')
        self.plotwidget.addItem(histoplot)

    def velib_carte(self):
          """ Renvoie dans un widget la carte des velibs dans Paris
          """
          url = "https://opendata.paris.fr/explore/embed/dataset/stations-velib-disponibilites-en-temps-reel/map/?dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6InN0YXRpb25zLXZlbGliLWRpc3BvbmliaWxpdGVzLWVuLXRlbXBzLXJlZWwiLCJvcHRpb25zIjp7fX0sImNoYXJ0cyI6W3sidHlwZSI6ImxpbmUiLCJmdW5jIjoiQVZHIiwieUF4aXMiOiJudW1iZXIiLCJzY2llbnRpZmljRGlzcGxheSI6dHJ1ZSwiY29sb3IiOiIjNjZjMmE1In1dLCJ4QXhpcyI6ImF2YWlsYWJsZV9iaWtlcyIsIm1heHBvaW50cyI6IiIsInRpbWVzY2FsZSI6IiIsInNvcnQiOiIiLCJzZXJpZXNCcmVha2Rvd24iOiIiLCJzZXJpZXNCcmVha2Rvd25UaW1lc2NhbGUiOiIifV0sInRpbWVzY2FsZSI6IiJ9&location=11,48.85426,2.39114&static=false&datasetcard=false"
          
          self.html1.load(QtCore.QUrl(url))
          self.html1.show()
          
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
#             self.cb3.clear()
             # Construction du dictionnaire
             for i in range(N):
#                loc = [str(record['fields']['address']) for record in self.dvelib['records']]
#                velibdispo = [record['fields']['available_bikes'] for record in self.dvelib['records']]
                 if int(str(self.dvelib['records'][i]['fields']['name'][:2])) == int(arrdt):
                     loc        = str(self.dvelib['records'][i]['fields']['address'])                    
                     velibdispo = self.dvelib['records'][i]['fields']['available_bikes']
                     info[loc]  = velibdispo
                     self.cb2.blockSignals(True)
                     self.cb2.addItem(loc)
                     self.cb2.blockSignals(False)
#            print (info)
          except:
             print (u"Pas de station répertoriées dans cet arrondissement")
    
    def googlemap(self):
        """ La fonction construit un url avec lequel webbrowser ouvre la page
        google map correspondante. Les donnees google map viennent du site Google
        developers, mais il faut une cle.
        
        entree: l'adresse d'une station velib
        sortie: l'url google map de cette adresse et ouverture d'une page internet
        """
        query = self.cb2.currentText()
#            query = str(self.l1.text())
    
        search_payload = {'key': key, 'query': query}
        search_req = requests.get(self.search_url, params=search_payload )
        search_json = search_req.json()
        
        place_id = search_json["results"][0]["place_id"]
        
        details_payload = {"key": key, "placeid": place_id}
        details_resp = requests.get(self.details_url, params= details_payload)
        details_json = details_resp.json()
    
        url = details_json["result"]["url"]
        self.html2.load(QtCore.QUrl(url))
        self.html2.show()
    
    def googlemap2(self):
        """ La fonction construit un url avec lequel webbrowser ouvre la page
        google map correspondante. Les donnees google map viennent du site Google
        developers, mais il faut une cle.
        
        entree: l'adresse d'une station velib
        sortie: l'url google map de cette adresse et ouverture d'une page internet
        """
        query = str(self.l1.text())
    
        search_payload = {'key': key, 'query': query}
        search_req = requests.get(self.search_url, params=search_payload )
        search_json = search_req.json()
        
        place_id = search_json["results"][0]["place_id"]
        
        details_payload = {"key": key, "placeid": place_id}
        details_resp = requests.get(self.details_url, params= details_payload)
        details_json = details_resp.json()
    
        url = details_json["result"]["url"]
        self.html2.load(QtCore.QUrl(url))
        self.html2.show()
        
    def arbres_remarquables(self):
        """ Cette fonction affiche dans un widget la carte ParisData des arbres
        remarquables de paris
        entree : il suffit d'appeler la fonction
        sortie : la carte affichee dans un widget du module QWebKit
        """
        url = "https://opendata.paris.fr/explore/embed/dataset/arbresremarquablesparis2011/map/?location=12,48.85611,2.34953&static=false&datasetcard=false"
        
        self.html1.load(QtCore.QUrl(url))
        self.html1.show()
     
    def salles_de_cinema(self):
         """ Afficher la localisation des salles de cinema dans Paris sur une 
         carte
         """
         url = "https://opendata.paris.fr/explore/embed/dataset/cinemas-a-paris/map/?location=12,48.85632,2.3559&static=false&datasetcard=false"
         
         self.html1.load(QtCore.QUrl(url))
         self.html1.show()
         
    def musees(self):
        """ Afficher l'emplacement des musees parisiens sur une carte
        """
        url = "https://opendata.paris.fr/explore/embed/dataset/liste-musees-de-france-a-paris/map/?location=12,48.86142,2.36266&static=false&datasetcard=false"
        
        self.html1.load(QtCore.QUrl(url))
        self.html1.show()


ouverture = SeeParisGui()
ouverture.show()

if __name__=="main":
    APP.exec_()
# Si le code est executé en mode standalone, la boucle d'application doit être lancée 
#pour que le code ne retourne pas immédiatement sans rien faire...

