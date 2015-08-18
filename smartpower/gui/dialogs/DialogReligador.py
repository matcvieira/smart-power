# -*- coding: utf-8 -*-

# Implementacao da caixa de dialogo do item Religador
#
# Created: Mon Feb 10 17:04:44 2014
#      by: Lucas Silveira Melo
#

from PySide import QtCore, QtGui
import sys

class RecloserDialog(QtGui.QWidget):
    
    def __init__(self):
        super(RecloserDialog, self).__init__()
        self.dialog = QtGui.QDialog(self)
        self.setupUi(self.dialog)
        self.dialog.exec_()
        
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(400, 300)
        
        self.buttonBox = QtGui.QDialogButtonBox(dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        
        self.formLayoutWidget = QtGui.QWidget(dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(19, 19, 361, 211))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        
        self.senderLabel = QtGui.QLabel(self.formLayoutWidget)
        self.senderLabel.setObjectName("senderLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.senderLabel)
        
        self.senderText = QtGui.QLineEdit(self.formLayoutWidget)
        self.senderText.setObjectName("senderText")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.senderText)
        
        self.receiverLabel = QtGui.QLabel(self.formLayoutWidget)
        self.receiverLabel.setObjectName("receiverLabel")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.receiverLabel)
        
        self.communicativeActComboBox = QtGui.QComboBox(self.formLayoutWidget)
        self.communicativeActComboBox.setObjectName("communicativeActComboBox")
        self.communicativeActComboBox.addItem("")
        self.communicativeActComboBox.addItem("")
        self.communicativeActComboBox.addItem("")
        self.communicativeActComboBox.addItem("")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.communicativeActComboBox)

        self.retranslateUi(dialog)
        
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), dialog.reject)
        
        QtCore.QMetaObject.connectSlotsByName(dialog)
                
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.senderLabel.setText(QtGui.QApplication.translate("Dialog", "Codigo de Operacao", None, QtGui.QApplication.UnicodeUTF8))
        self.receiverLabel.setText(QtGui.QApplication.translate("Dialog", "Tipo de Condutor", None, QtGui.QApplication.UnicodeUTF8))
        self.communicativeActComboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "4.0 mm2", None, QtGui.QApplication.UnicodeUTF8))
        self.communicativeActComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "6.0 mm2", None, QtGui.QApplication.UnicodeUTF8))
        self.communicativeActComboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "8.0 mm2", None, QtGui.QApplication.UnicodeUTF8))
        self.communicativeActComboBox.setItemText(3, QtGui.QApplication.translate("Dialog", "10.0 mm2", None, QtGui.QApplication.UnicodeUTF8))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    dialogReligador = RecloserDialog()
    sys.exit(app.exec_())