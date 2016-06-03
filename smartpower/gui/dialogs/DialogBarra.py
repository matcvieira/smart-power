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
        Propriedades.resize(380, 271)
        #Define o tamanho da caixa dialogo
        self.buttonBox = QtGui.QDialogButtonBox(Propriedades)
        self.buttonBox.setGeometry(QtCore.QRect(0, 231, 341, 32))
        #Define o tamanho do layout dos botões do dialogo
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtGui.QWidget(Propriedades)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 350, 231))
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

        #definição da propriedade IMPEDANCIA SEQUENCIA POSITIVA
        self.r_posLabel = QtGui.QLabel(self.formLayoutWidget)
        self.r_posLabel.setObjectName("r_posLabel")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.r_posLabel)
        self.r_posLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.r_posLineEdit.setObjectName("r_posLineEdit")
        self.r_posLineEdit.setPlaceholderText(str(self.item.barra.r_pos))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.r_posLineEdit)

        self.i_posLabel = QtGui.QLabel(self.formLayoutWidget)
        self.i_posLabel.setObjectName("i_posLabel")
        self.i_posLabel.setAlignment(QtCore.Qt.AlignRight)
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.i_posLabel)
        self.i_posLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.i_posLineEdit.setObjectName("i_posLineEdit")
        self.i_posLineEdit.setPlaceholderText(str(self.item.barra.i_pos))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.i_posLineEdit)

        #definição da propriedade IMPEDANCIA SEQUENCIA ZERO
        self.r_zeroLabel = QtGui.QLabel(self.formLayoutWidget)
        self.r_zeroLabel.setObjectName("r_zeroLabel")
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.r_zeroLabel)
        self.r_zeroLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.r_zeroLineEdit.setObjectName("r_zeroLineEdit")
        self.r_zeroLineEdit.setPlaceholderText(str(self.item.barra.r_zero))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.r_zeroLineEdit)

        self.i_zeroLabel = QtGui.QLabel(self.formLayoutWidget)
        self.i_zeroLabel.setObjectName("i_zeroLabel")
        self.i_zeroLabel.setAlignment(QtCore.Qt.AlignRight)
        self.formLayout.setWidget(8, QtGui.QFormLayout.LabelRole, self.i_zeroLabel)
        self.i_zeroLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.i_zeroLineEdit.setObjectName("i_zeroLineEdit")
        self.i_zeroLineEdit.setPlaceholderText(str(self.item.barra.i_zero))
        self.formLayout.setWidget(8, QtGui.QFormLayout.FieldRole, self.i_zeroLineEdit)

        self.retranslateUi(Propriedades)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Propriedades.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Propriedades.reject)
        QtCore.QMetaObject.connectSlotsByName(Propriedades)

    def retranslateUi(self, Propriedades):
        #Tradução dos nomes dados aos objetos para os nomes gráficos do programa
        Propriedades.setWindowTitle(QtGui.QApplication.translate("Propriedades", "Barra - Propriedades", None, QtGui.QApplication.UnicodeUTF8))
        self.nomeLabel.setText(QtGui.QApplication.translate("Propriedades", "Nome:", None, QtGui.QApplication.UnicodeUTF8))
        self.fasesLabel.setText(QtGui.QApplication.translate("Propriedades", "Fases:", None, QtGui.QApplication.UnicodeUTF8))
        self.r_posLabel.setText(QtGui.QApplication.translate("Dialog", "Impedância (Sequência Positiva):", None, QtGui.QApplication.UnicodeUTF8))
        self.i_posLabel.setText(QtGui.QApplication.translate("Dialog", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.r_zeroLabel.setText(QtGui.QApplication.translate("Dialog", "Impedância (Sequência Zero):", None, QtGui.QApplication.UnicodeUTF8))
        self.i_zeroLabel.setText(QtGui.QApplication.translate("Dialog", "+", None, QtGui.QApplication.UnicodeUTF8))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    BarraDialog = BarraDialog()
    sys.exit(app.exec_())
