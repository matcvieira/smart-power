# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Cadastro.ui'
#
# Created: Sat Mar 14 16:55:19 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import sys

class CadastroDialog(QtGui.QWidget):

    def __init__(self):
        super(CadastroDialog, self).__init__()
        self.dialog = QtGui.QDialog(self)
        self.setupUi(self.dialog)
        self.dialog.exec_()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(348, 109)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(160, 70, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 331, 41))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.nomeDoCadastroLabel = QtGui.QLabel(self.formLayoutWidget)
        self.nomeDoCadastroLabel.setObjectName("nomeDoCadastroLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.nomeDoCadastroLabel)
        self.nomeDoCadastroLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.nomeDoCadastroLineEdit.setObjectName("nomeDoCadastroLineEdit")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nomeDoCadastroLineEdit)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Novo Cadastro", None, QtGui.QApplication.UnicodeUTF8))
        self.nomeDoCadastroLabel.setText(QtGui.QApplication.translate("Dialog", "Nome do Cadastro:", None, QtGui.QApplication.UnicodeUTF8))
        

if __name__ == '__main__':
        app = QtGui.QApplication(sys.argv)
        dialogCadastro = CadastroDialog()
        sys.exit(app.exec_())