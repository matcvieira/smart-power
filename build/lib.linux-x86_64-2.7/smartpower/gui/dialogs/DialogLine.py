# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DialogLine.ui'
#
# Created: Mon Feb  9 00:19:18 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys

class LineDialog(QtGui.QWidget):

    def __init__(self):
        super(LineDialog, self).__init__()
        self.dialog = QtGui.QDialog(self)
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(428, 180)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(210, 130, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 401, 101))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.comprimentoMLabel = QtGui.QLabel(self.formLayoutWidget)
        self.comprimentoMLabel.setObjectName("comprimentoMLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.comprimentoMLabel)
        self.comprimentoMLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.comprimentoMLineEdit.setObjectName("comprimentoMLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comprimentoMLineEdit)
        self.impedNciaPorComprimentoLabel = QtGui.QLabel(self.formLayoutWidget)
        self.impedNciaPorComprimentoLabel.setObjectName("impedNciaPorComprimentoLabel")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.impedNciaPorComprimentoLabel)
        self.impedNciaPorComprimentoLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.impedNciaPorComprimentoLineEdit.setObjectName("impedNciaPorComprimentoLineEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.impedNciaPorComprimentoLineEdit)
        self.limiteDeOperaOALabel = QtGui.QLabel(self.formLayoutWidget)
        self.limiteDeOperaOALabel.setObjectName("limiteDeOperaOALabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.limiteDeOperaOALabel)
        self.limiteDeOperaOALineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.limiteDeOperaOALineEdit.setObjectName("limiteDeOperaOALineEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.limiteDeOperaOALineEdit)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Alimentador - Propriedades", None, QtGui.QApplication.UnicodeUTF8))
        self.comprimentoMLabel.setText(QtGui.QApplication.translate("Dialog", "Comprimento (m):", None, QtGui.QApplication.UnicodeUTF8))
        self.impedNciaPorComprimentoLabel.setText(QtGui.QApplication.translate("Dialog", "Impedância por Comprimento (ohms/m)", None, QtGui.QApplication.UnicodeUTF8))
        self.limiteDeOperaOALabel.setText(QtGui.QApplication.translate("Dialog", "Limite de Operação (A)", None, QtGui.QApplication.UnicodeUTF8))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    dialogLinha = LineDialog()
    sys.exit(app.exec_())