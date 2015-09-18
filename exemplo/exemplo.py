#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
from cursor import Cursor
import math
import sys

class MainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.cursor = Cursor("")
        self.setCursor(self.cursor)
        self.scene = SceneSpecial(self)
        self.view = ViewSpecial(self.scene, self)
        self.resize(1000, 700)
        self.view.resize(1000,500)
        self.show()

    def mouseReleaseEvent(self, mouse_event):
    	self.cursor.setShapePad(self)
        super(MainWindow, self).mouseReleaseEvent(mouse_event)
        print "release"
        self.view.drawItem(self.mapFromGlobal(self.cursor.pos()))
    
    def mousePressEvent(self, mouse_event):
    	self.cursor.setShapeSubs(self)
        super(MainWindow, self).mousePressEvent(mouse_event)
        print "press"

class ViewSpecial(QtGui.QGraphicsView):
	def __init__(self, parent, widget):
		super(ViewSpecial, self).__init__(parent, widget)
		self.scene = parent

	def drawItem(self, point):
		self.scene.drawItem(point)

class SceneSpecial(QtGui.QGraphicsScene):
    def __init__(self, parent):
        super(SceneSpecial, self).__init__(parent)
        self.cursor = parent.cursor
        self.setStickyFocus(True)

    def mouseReleaseEvent(self, mouse_event):
        super(SceneSpecial, self).mouseReleaseEvent(mouse_event)
        ell = QtGui.QGraphicsEllipseItem()
        ell.setRect(
            QtCore.QRectF(
                mouse_event.scenePos()-QtCore.QPoint(15, 15),
                QtCore.QSizeF(30, 30)))
        self.addItem(ell)

    def drawItem(self, point):
        ell = QtGui.QGraphicsEllipseItem()
        ell.setRect(
            QtCore.QRectF(
                point-QtCore.QPoint(15, 15),
                QtCore.QSizeF(30, 30)))
        self.addItem(ell)


    def paint(self, painter, option, widget):
        self.rectangle = QtCore.QRectF(10.0, 20.0, 80.0, 60.0)
        painter.drawRect(self.rectangle)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
