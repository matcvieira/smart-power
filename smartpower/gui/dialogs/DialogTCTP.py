# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogRecloser.ui'
#
# Created: Sun Feb  8 22:33:29 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys
from Cadastro import CadastroDialog

class TCTPDialog(QtGui.QWidget):

    def __init__(self, item):
        super(RecloserDialog, self).__init__()
        self.dialog = QtGui.QDialog(self)
        self.item = item
        self.scene = self.item.scene()
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        #Dialog.resize(380, 210)
        sc = 10.0
        Dialog.resize(380, 40+33*sc)
        #Define o tamanho da caixa dialogo
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 33*sc, 341, 32))
        #Define o tamanho do layout dos botões do dialogo
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cadastro = QtGui.QPushButton('Cadastrar Novo')
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        #print self.buttonBox.buttons
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 350, 33*sc))
        #Define a localização do layout das propriedades (coordenada x do ponto, coordenada y do ponto, dimensão em x, dimensão em y)
        self.layout = QtGui.QVBoxLayout()
        self.subLayout1 = QtGui.QHBoxLayout()
        self.sublayout2 = QtGui.QHBoxLayout()
        self.sublayout3 = QtGui.QHBoxLayout()
        self.sublayout4 = QtGui.QHBoxLayout()

        # Definição da COMBOBOX
        self.testeLabel = QtGui.QLabel(self.formLayoutWidget)
        self.testeLabel.setObjectName("testeLabel")
        self.formLayout.setWidget(10, QtGui.QFormLayout.LabelRole, self.testeLabel)
        self.testeLineEdit = QtGui.QComboBox(self.formLayoutWidget)
        self.testeLineEdit.setObjectName("testeEdit")
        self.testeLineEdit.addItems(self.scene.dict_prop.keys())
        self.testeLineEdit.insertItem(0,"Custom")
        index = self.testeLineEdit.findText(self.item.text_config)
        # if index < 0:
        #     index = 0
        self.testeLineEdit.setCurrentIndex(index)
        self.formLayout.setWidget(10, QtGui.QFormLayout.FieldRole, self.testeLineEdit)
        self.testeLineEdit.currentIndexChanged.connect(self.update_values)


        #definição da propriedade RTC
        self.RTCLabel = QtGui.QLabel(self.formLayoutWidget)
        self.RTCLabel.setObjectName("identificaOLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.identificaOLabel)
        self.RTCLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.RTCLineEdit.setObjectName("RTCLineEdit")
        self.RTCLineEdit.setPlaceholderText(self.item.text.toPlainText())
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.RTCLineEdit)
        self.RTCLineEdit.textChanged.connect(self.en_dis_button)

        #definição da propriedade RTP
        self.RTPLabel = QtGui.QLabel(self.formLayoutWidget)
        self.RTPLabel.setObjectName("RTPLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.RTPLabel)
        self.RTPLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.RTPLineEdit.setObjectName("RTPLineEdit")
        self.RTPLineEdit.setText(str(self.item.chave.ratedCurrent))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.RTPLineEdit)
        self.RTPLineEdit.textEdited.connect(self.custom)

        '''
        if self.identificaOLineEdit.text() == "":
            print self.buttonBox.buttons()
            self.buttonBox.buttons()[0].setEnabled(False)
        else:
            self.buttonBox.buttons()[0].setEnabled(True)
        if self.identificaOLineEdit.placeholderText() != "":
            self.buttonBox.buttons()[0].setEnabled(True)
        '''

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def en_dis_button(self):

        if self.identificaOLineEdit.text() == "":
            print self.buttonBox.buttons()
            self.buttonBox.buttons()[0].setEnabled(False)
        else:
            self.buttonBox.buttons()[0].setEnabled(True)

    def update_values(self, index):

        if index == 0:
            return

        self.correnteNominalLineEdit.setText(str(self.scene.dict_prop[self.testeLineEdit.currentText()]['Corrente Nominal']))
        self.capacidadeDeInterrupOLineEdit.setText(str(self.scene.dict_prop[self.testeLineEdit.currentText()]['Capacidade de Interrupcao']))
        self.nDeSequNciasDeReligamentoLineEdit.setText(str(self.scene.dict_prop[self.testeLineEdit.currentText()]['Sequencia']))




    def retranslateUi(self, Dialog):

        #Tradução dos nomes dados aos objetos para os nomes gráficos do programa
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "TC e TP - Propriedades", None, QtGui.QApplication.UnicodeUTF8))
        self.RTCLabel.setText(QtGui.QApplication.translate("Dialog", "RTC:", None, QtGui.QApplication.UnicodeUTF8))
        self.RTP.setText(QtGui.QApplication.translate("Dialog", "RTP: ", None, QtGui.QApplication.UnicodeUTF8))
        
    if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)
        dialogTCTP = TCTPDialog()
        sys.exit(app.exec_())