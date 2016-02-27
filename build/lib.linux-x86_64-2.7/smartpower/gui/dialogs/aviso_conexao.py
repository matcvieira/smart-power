# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aviso_conexao.ui'
#
# Created: Sun Mar 15 15:28:01 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys

class AvisoConexaoDialog(QtGui.QWidget):

    def __init__(self):
        super(AvisoConexaoDialog, self).__init__()
        self.dialog = QtGui.QDialog(self)
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(332, 86)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(110, 50, 81, 27))
        self.pushButton.setObjectName("pushButton")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 311, 21))
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        self.pushButton.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Erro", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Você deve excluir as outras conexões primeiro!", None, QtGui.QApplication.UnicodeUTF8))

