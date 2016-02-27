# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogEnergyConsumer.ui'
#
# Created: Sat Apr 25 01:53:31 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys


class EnergyConsumerDialog(QtGui.QWidget):
    
    def __init__(self, item):
        super(EnergyConsumerDialog, self).__init__()
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
        self.identificaOLabel = QtGui.QLabel(self.formLayoutWidget)
        self.identificaOLabel.setObjectName("identificaOLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.identificaOLabel)
        self.identificaOLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.identificaOLineEdit.setObjectName("identificaOLineEdit")
        self.identificaOLineEdit.setPlaceholderText(str(self.item.no_de_carga.nome))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.identificaOLineEdit)
        self.identificaOLineEdit.textChanged.connect(self.en_dis_button)

        #definição da propriedade Potencia Ativa
        self.potNciaAtivaLabel = QtGui.QLabel(self.formLayoutWidget)
        self.potNciaAtivaLabel.setObjectName("potNciaAtivaLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.potNciaAtivaLabel)
        self.potNciaAtivaLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.potNciaAtivaLineEdit.setObjectName("potNciaAtivaLineEdit")
        self.potNciaAtivaLineEdit.setPlaceholderText(str(self.item.no_de_carga.potencia_ativa))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.potNciaAtivaLineEdit)
        
        #definição da propriedade Potencia Reativa
        self.potNciaReativaLabel = QtGui.QLabel(self.formLayoutWidget)
        self.potNciaReativaLabel.setObjectName("potNciaReativaLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.potNciaReativaLabel)
        self.potNciaReativaLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.potNciaReativaLineEdit.setObjectName("potNciaReativaLineEdit")
        self.potNciaReativaLineEdit.setPlaceholderText(str(self.item.no_de_carga.potencia_reativa))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.potNciaReativaLineEdit)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # if self.identificaOLineEdit.text() == "":
        #     print self.buttonBox.buttons()
        #     self.buttonBox.buttons()[0].setEnabled(False)
        # else:
        #     self.buttonBox.buttons()[0].setEnabled(True)
        self.en_dis_button()
        if self.identificaOLineEdit.placeholderText() != "":
            if self.potNciaAtivaLineEdit.placeholderText() != "0":
                if self.potNciaReativaLineEdit.placeholderText() != "0":
                    self.buttonBox.buttons()[0].setFocus()
                else:
                    self.potNciaReativaLineEdit.setFocus()
            else:
                self.potNciaAtivaLineEdit.setFocus()
        else:
            self.identificaOLineEdit.setFocus()


    def en_dis_button(self):

        if self.identificaOLineEdit.text() == "":
            print self.buttonBox.buttons()
            self.buttonBox.buttons()[0].setEnabled(False)
        else:
            self.buttonBox.buttons()[0].setEnabled(True)
        if self.identificaOLineEdit.placeholderText() != "":
            self.buttonBox.buttons()[0].setEnabled(True)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "No de Carga - Propriedades", None, QtGui.QApplication.UnicodeUTF8))
        self.identificaOLabel.setText(QtGui.QApplication.translate("Dialog", "Identificação", None, QtGui.QApplication.UnicodeUTF8))
        self.potNciaAtivaLabel.setText(QtGui.QApplication.translate("Dialog", "Potência Ativa", None, QtGui.QApplication.UnicodeUTF8))
        self.potNciaReativaLabel.setText(QtGui.QApplication.translate("Dialog", "Potência Reativa", None, QtGui.QApplication.UnicodeUTF8))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    EnergyConsumerDialog = EnergyConsumerDialog()
    sys.exit(app.exec_())
