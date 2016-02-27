# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogBarra.ui'
#
# Created: Sun Mar  1 19:05:57 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys
class BarraDialog(QtGui.QWidget):

    def __init__(self, item):
        super(BarraDialog, self).__init__()
        self.dialog = QtGui.QDialog(None)
        self.item = item
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Propriedades):
        Propriedades.setObjectName("Propriedades")
        Propriedades.resize(380, 210)
        #Define o tamanho da caixa dialogo 
        self.buttonBox = QtGui.QDialogButtonBox(Propriedades)
        self.buttonBox.setGeometry(QtCore.QRect(0, 170, 341, 32))
        #Define o tamanho do layout dos botões do dialogo
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtGui.QWidget(Propriedades)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 350, 150))
        #Define a localização do layout das propriedades (coordenada x do ponto, coordenada y do ponto, dimensão em x, dimensão em y)
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        
        #definição da propriedade NOME
        self.nomeLabel = QtGui.QLabel(self.formLayoutWidget)
        self.nomeLabel.setObjectName("nomeLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nomeLabel)
        self.nomeLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.nomeLineEdit.setObjectName("nomeLineEdit")
        self.nomeLineEdit.setPlaceholderText(str(self.item.barra.nome))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nomeLineEdit)
        self.fasesLabel = QtGui.QLabel(self.formLayoutWidget)
        
        #definição da propriedade FASES
        self.fasesLabel.setObjectName("fasesLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.fasesLabel)
        self.fasesLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.fasesLineEdit.setObjectName("fasesLineEdit")
        self.fasesLineEdit.setPlaceholderText(str(self.item.barra.phases))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.fasesLineEdit)

        self.retranslateUi(Propriedades)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Propriedades.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Propriedades.reject)
        QtCore.QMetaObject.connectSlotsByName(Propriedades)

    def retranslateUi(self, Propriedades):
        #Tradução dos nomes dados aos objetos para os nomes gráficos do programa
        Propriedades.setWindowTitle(QtGui.QApplication.translate("Propriedades", "Barra - Propriedades", None, QtGui.QApplication.UnicodeUTF8))
        self.nomeLabel.setText(QtGui.QApplication.translate("Propriedades", "Nome:", None, QtGui.QApplication.UnicodeUTF8))
        self.fasesLabel.setText(QtGui.QApplication.translate("Propriedades", "Fases:", None, QtGui.QApplication.UnicodeUTF8))
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    BarraDialog = BarraDialog()
    sys.exit(app.exec_())
