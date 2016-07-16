#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
import math
import sys

class Cursor(QtGui.QCursor):

    def __init__(self, image):
        super(Cursor, self).__init__(image, -1, -1)

    def setShapeSubs(self, widget):
        cursor = Cursor(QtGui.QBitmap(u"icones/iconSubstation.png"))
        widget.setCursor(cursor)

    def setShapeRecl(self, widget):
        cursor = Cursor(QtGui.QBitmap(u"icones/iconRecloser.png"))
        widget.setCursor(cursor)

    def setShapePad(self, widget):
        cursor = Cursor(QtGui.QBitmap(u""))
        widget.setCursor(cursor)
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    cursor = Cursor("")
    app.setOverrideCursor(cursor)
    sys.exit(app.exec_())
