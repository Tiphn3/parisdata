# -*- coding: utf-8 -*-
from __future__ import division
"""
Created on Sun Jan 22 17:20:39 2017

@author: Tiphaine
"""

import pyqtgraph as pg
import numpy as np
from PyQt4 import QtGui,QtCore

#app = pg.mkQApp()

class Pw(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, parent=None)
        self.resize(640,640)
        self.setWindowTitle("Graphe dans un widget")
        
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        
        self.plot = pg.PlotWidget(title="Donnees aleatoires")
        self.layout.addWidget(self.plot)
        
        self.button = QtGui.QPushButton("Texte sur le bouton",self)
        self.button.clicked.connect(self.plotGraph)
        self.layout.addWidget(self.button,2,0)
        
    def plotGraph(self):
        self.plot.clear()
        self.data = np.random.normal(loc=0.0,scale=2,size=100)
        self.plot.plot(self.data)


test = Pw()
test.show()
