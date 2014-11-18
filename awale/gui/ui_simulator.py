# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulator.ui'
#
# Created: Tue Nov 18 19:03:33 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(596, 327)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.player2 = PlayerView(self.centralwidget)
        self.player2.setObjectName("player2")
        self.gridLayout_3.addWidget(self.player2, 0, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.nbGame = QtWidgets.QSpinBox(self.centralwidget)
        self.nbGame.setObjectName("nbGame")
        self.gridLayout_2.addWidget(self.nbGame, 1, 1, 1, 1)
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.gridLayout_2.addWidget(self.startButton, 1, 2, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_2.addWidget(self.progressBar, 2, 0, 1, 3)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.reason = QtWidgets.QLabel(self.centralwidget)
        self.reason.setObjectName("reason")
        self.gridLayout_2.addWidget(self.reason, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 1, 0, 1, 2)
        self.player1 = PlayerView(self.centralwidget)
        self.player1.setObjectName("player1")
        self.gridLayout_3.addWidget(self.player1, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "Number of games :"))
        self.startButton.setText(_translate("MainWindow", "Start !"))
        self.label.setText(_translate("MainWindow", "Chance or Talent ?"))
        self.reason.setText(_translate("MainWindow", "Unknown"))

from awale.gui.player_view import PlayerView
