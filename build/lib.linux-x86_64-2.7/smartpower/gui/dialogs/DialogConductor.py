# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogConductor.ui'
#
# Created: Tue Mar 17 13:53:51 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys

class ConductorDialog(QtGui.QWidget):

    def __init__(self, item):
        super(ConductorDialog, self).__init__()
        self.dialog = QtGui.QDialog(self)
        self.item = item
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(380, 210)

        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(0, 170, 341, 32))

        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 350, 150))

        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")

        self.comprimentoLabel = QtGui.QLabel(self.formLayoutWidget)
        self.comprimentoLabel.setObjectName("comprimentoLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.comprimentoLabel)
        self.comprimentoLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.comprimentoLineEdit.setObjectName("comprimentoLineEdit")
        self.comprimentoLineEdit.setPlaceholderText(str(self.item.linha.comprimento))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comprimentoLineEdit)

        self.resistenciaLabel = QtGui.QLabel(self.formLayoutWidget)
        self.resistenciaLabel.setObjectName("resistenciaLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.resistenciaLabel)
        self.resistenciaLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.resistenciaLineEdit.setObjectName("resistenciaLineEdit")
        self.resistenciaLineEdit.setPlaceholderText(str(self.item.linha.resistencia))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.resistenciaLineEdit)
        
        self.resistenciaZeroLabel = QtGui.QLabel(self.formLayoutWidget)
        self.resistenciaZeroLabel.setObjectName("resistenciaZeroLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.resistenciaZeroLabel)
        self.resistenciaZeroLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.resistenciaZeroLineEdit.setObjectName("resistenciaZeroLineEdit")
        self.resistenciaZeroLineEdit.setPlaceholderText(str(self.item.linha.resistencia_zero))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.resistenciaZeroLineEdit)
        
        self.reatanciaLabel = QtGui.QLabel(self.formLayoutWidget)
        self.reatanciaLabel.setObjectName("reatanciaLabel")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.reatanciaLabel)
        self.reatanciaLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.reatanciaLineEdit.setObjectName("reatanciaLineEdit")
        self.reatanciaLineEdit.setPlaceholderText(str(self.item.linha.reatancia))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.reatanciaLineEdit)
        
        self.reatanciaZeroLabel = QtGui.QLabel(self.formLayoutWidget)
        self.reatanciaZeroLabel.setObjectName("reatanciaZeroLabel")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.reatanciaZeroLabel)
        self.reatanciaZeroLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.reatanciaZeroLineEdit.setObjectName("reatanciaZeroLineEdit")
        self.reatanciaZeroLineEdit.setPlaceholderText(str(self.item.linha.reatancia_zero))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.reatanciaZeroLineEdit)
        
        self.ampacidadeLabel = QtGui.QLabel(self.formLayoutWidget)
        self.ampacidadeLabel.setObjectName("ampacidadeLabel")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.ampacidadeLabel)
        self.ampacidadeLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.ampacidadeLineEdit.setObjectName("ampacidadeLineEdit")
        self.ampacidadeLineEdit.setPlaceholderText(str(self.item.linha.ampacidade))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.ampacidadeLineEdit)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Condutor - Propriedades", None, QtGui.QApplication.UnicodeUTF8))
        self.comprimentoLabel.setText(QtGui.QApplication.translate("Dialog", "Comprimento", None, QtGui.QApplication.UnicodeUTF8))
        self.resistenciaLabel.setText(QtGui.QApplication.translate("Dialog", "Resistencia", None, QtGui.QApplication.UnicodeUTF8))
        self.resistenciaZeroLabel.setText(QtGui.QApplication.translate("Dialog", "Resistencia Zero", None, QtGui.QApplication.UnicodeUTF8))
        self.reatanciaLabel.setText(QtGui.QApplication.translate("Dialog", "Reatancia", None, QtGui.QApplication.UnicodeUTF8))
        self.reatanciaZeroLabel.setText(QtGui.QApplication.translate("Dialog", "Reatancia Zero", None, QtGui.QApplication.UnicodeUTF8))
        self.ampacidadeLabel.setText(QtGui.QApplication.translate("Dialog", "Ampacidade", None, QtGui.QApplication.UnicodeUTF8))

    if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)
        dialogConductor = ConductorDialog()
        sys.exit(app.exec_())