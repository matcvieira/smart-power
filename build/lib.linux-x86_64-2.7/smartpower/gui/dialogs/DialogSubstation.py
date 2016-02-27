# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogSubstation.ui'
#
# Created: Mon Mar  2 22:55:39 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys

class SubstationDialog(QtGui.QWidget):

    def __init__(self, item):
        super(SubstationDialog, self).__init__()
        self.dialog = QtGui.QDialog(self)
        self.item = item
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(380, 210)
        #Define o tamanho da caixa dialogo 
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 170, 341, 32))
        #Define o tamanho do layout dos botões do dialogo
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtGui.QWidget(Dialog)
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
        self.nomeLineEdit.setPlaceholderText(str(self.item.substation.nome))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nomeLineEdit)
        self.nomeLineEdit.textChanged.connect(self.en_dis_button)

        #definição da propriedade TENSÃO PRIMÁRIO
        self.tpLabel = QtGui.QLabel(self.formLayoutWidget)
        self.tpLabel.setObjectName("tpLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.tpLabel)
        self.tpLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.tpLineEdit.setObjectName("tpLineEdit")
        self.tpLineEdit.setPlaceholderText(str(self.item.substation.tensao_primario))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.tpLineEdit)

        #definição da propriedade TENSÃO SECUNDÁRIO
        self.tsLabel = QtGui.QLabel(self.formLayoutWidget)
        self.tsLabel.setObjectName("tsLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.tsLabel)
        self.tsLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.tsLineEdit.setObjectName("tsLineEdit")
        self.tsLineEdit.setPlaceholderText(str(self.item.substation.tensao_secundario))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.tsLineEdit)

        #definição da propriedade POTENCIA
        self.potLabel = QtGui.QLabel(self.formLayoutWidget)
        self.potLabel.setObjectName("potLabel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.potLabel)
        self.potLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.potLineEdit.setObjectName("potLineEdit")
        self.potLineEdit.setPlaceholderText(str(self.item.substation.potencia))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.potLineEdit)

        #definição da propriedade IMPEDANCIA
        self.zLabel = QtGui.QLabel(self.formLayoutWidget)
        self.zLabel.setObjectName("zLabel")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.zLabel)
        self.zLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.zLineEdit.setObjectName("zLineEdit")
        self.zLineEdit.setPlaceholderText(str(self.item.substation.impedancia))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.zLineEdit)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        if self.nomeLineEdit.text() == "":
            print self.buttonBox.buttons()
            self.buttonBox.buttons()[0].setEnabled(False)
        else:
            self.buttonBox.buttons()[0].setEnabled(True)
        if self.nomeLineEdit.placeholderText() != "":
            self.buttonBox.buttons()[0].setEnabled(True)

    def en_dis_button(self):

        if self.nomeLineEdit.text() == "":
            print self.buttonBox.buttons()
            self.buttonBox.buttons()[0].setEnabled(False)
        else:
            self.buttonBox.buttons()[0].setEnabled(True)

    def retranslateUi(self, Dialog):
        #Tradução dos nomes dados aos objetos para os nomes gráficos do programa
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Subestacao - Propriedades", None, QtGui.QApplication.UnicodeUTF8))
        self.nomeLabel.setText(QtGui.QApplication.translate("Dialog", "Nome", None, QtGui.QApplication.UnicodeUTF8))
        self.tpLabel.setText(QtGui.QApplication.translate("Dialog", "Tensao Primario:", None, QtGui.QApplication.UnicodeUTF8))
        self.tsLabel.setText(QtGui.QApplication.translate("Dialog", "Tensao Secundario:", None, QtGui.QApplication.UnicodeUTF8))
        self.potLabel.setText(QtGui.QApplication.translate("Dialog", "Potencia:", None, QtGui.QApplication.UnicodeUTF8))
        self.zLabel.setText(QtGui.QApplication.translate("Dialog", "Impedancia:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    SubstationDialog = SubstationDialog()
    sys.exit(app.exec_())
