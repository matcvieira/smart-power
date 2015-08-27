# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'avisoReligador.ui'
#
# Created: Mon Apr 27 17:57:38 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys

class AvisoReligador(QtGui.QWidget):

    def __init__(self, estado, nome):
        super(AvisoReligador, self).__init__()
        self.estado = estado
        self.nome = nome
        self.dialog = QtGui.QDialog(self)
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(420, 120)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(120, 70, 176, 27))
        self.buttonBox.addButton(QtGui.QPushButton("Sim"), QtGui.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(QtGui.QPushButton(QtGui.QApplication.translate("Dialog", "Não", None, QtGui.QApplication.UnicodeUTF8)), QtGui.QDialogButtonBox.RejectRole)
        #self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        self.buttonBox.setObjectName("buttonBox")
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 420, 41))
        self.label.setObjectName("label")
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "AVISO!", None, QtGui.QApplication.UnicodeUTF8))
        if self.estado == 0:
            self.label.setText(QtGui.QApplication.translate("Dialog", "Você tem certeza de que quer ABRIR o Religador " + str(self.nome) + "?", None, QtGui.QApplication.UnicodeUTF8))
        else:
            self.label.setText(QtGui.QApplication.translate("Dialog", "Você tem certeza de que quer FECHAR o Religador "  + str(self.nome) + "?", None, QtGui.QApplication.UnicodeUTF8))
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ReligadorAviso = AvisoReligador()
    sys.exit(app.exec_())
