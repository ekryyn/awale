# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'player_view.ui'
#
# Created: Tue Nov 18 17:18:19 2014
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(282, 251)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.player_cmd = QtWidgets.QLineEdit(self.groupBox)
        self.player_cmd.setObjectName("player_cmd")
        self.horizontalLayout.addWidget(self.player_cmd)
        self.browse_btn = QtWidgets.QPushButton(self.groupBox)
        self.browse_btn.setObjectName("browse_btn")
        self.horizontalLayout.addWidget(self.browse_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.victories = QtWidgets.QLabel(self.groupBox)
        self.victories.setObjectName("victories")
        self.gridLayout_2.addWidget(self.victories, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.defeats = QtWidgets.QLabel(self.groupBox)
        self.defeats.setObjectName("defeats")
        self.gridLayout_2.addWidget(self.defeats, 2, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 3, 0, 1, 1)
        self.draws = QtWidgets.QLabel(self.groupBox)
        self.draws.setObjectName("draws")
        self.gridLayout_2.addWidget(self.draws, 3, 1, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 4, 0, 1, 1)
        self.win_percent = QtWidgets.QLabel(self.groupBox)
        self.win_percent.setObjectName("win_percent")
        self.gridLayout_2.addWidget(self.win_percent, 4, 1, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 5, 0, 1, 1)
        self.moves_played = QtWidgets.QLabel(self.groupBox)
        self.moves_played.setObjectName("moves_played")
        self.gridLayout_2.addWidget(self.moves_played, 5, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setObjectName("label_12")
        self.gridLayout_2.addWidget(self.label_12, 6, 0, 1, 1)
        self.valid_moves_mean = QtWidgets.QLabel(self.groupBox)
        self.valid_moves_mean.setObjectName("valid_moves_mean")
        self.gridLayout_2.addWidget(self.valid_moves_mean, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "PlayerName"))
        self.browse_btn.setText(_translate("Form", "Browse"))
        self.label_4.setText(_translate("Form", "Victories :"))
        self.victories.setText(_translate("Form", "0"))
        self.label_6.setText(_translate("Form", "Defeats :"))
        self.defeats.setText(_translate("Form", "0"))
        self.label_11.setText(_translate("Form", "Draws :"))
        self.draws.setText(_translate("Form", "0"))
        self.label_9.setText(_translate("Form", "Vicotry % :"))
        self.win_percent.setText(_translate("Form", "0%"))
        self.label_10.setText(_translate("Form", "Moves per game :"))
        self.moves_played.setText(_translate("Form", "0"))
        self.label_12.setText(_translate("Form", "Valid moves per turn :"))
        self.valid_moves_mean.setText(_translate("Form", "0"))

