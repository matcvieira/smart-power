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
        self.view.drawItem(self.view.mapToScene(self.view.mapFromGlobal(self.cursor.pos())))
    
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

    def drawItem(self, pointf):
        cont=1
        point = pointf.toPoint()
        """
        ell = QtGui.QGraphicsEllipseItem()        
        ell.setRect(
            QtCore.QRectF(
                point-QtCore.QPoint(15, 15),
                QtCore.QSizeF(30, 30)))
        #self.addItem(ell)

        traf = QtGui.QPolygon()
        traf.append(point+QtCore.QPoint(4,8))
        traf.append(point+QtCore.QPoint(0,14))
        traf.append(point+QtCore.QPoint(8,14))
        

        #self.addItem(QtGui.QGraphicsPolygonItem(traf))

        #TESTE FUNCIONAL DO PATH
        path = QtGui.QPainterPath()
        #path.addEllipse(ell)]

        traf = QtGui.QPolygon()
        traf.append(point+QtCore.QPoint(4,7)+QtCore.QPoint(46,47))
        traf.append(point+QtCore.QPoint(0,0)+QtCore.QPoint(46,47))
        traf.append(point+QtCore.QPoint(8,0)+QtCore.QPoint(46,47))
        traf.append(point+QtCore.QPoint(4,7)+QtCore.QPoint(46,47))

        path.moveTo(point+QtCore.QPoint(0, 0))
        path.cubicTo(point.x()+99, point.y()+0, point.x()+50, point.y()+50, point.x()+99, point.y()+99)
        path.cubicTo(point.x()+0, point.y()+99, point.x()+50, point.y()+50, point.x()+0, point.y()+0)
        
        path.addPolygon(traf)
        """

        self.addItem(Node(cont,point))
        self.update()


    def paint(self, painter, option, widget):
        self.rectangle = QtCore.QRectF(10.0, 20.0, 80.0, 60.0)
        painter.drawRect(self.rectangle)



class Node(QtGui.QGraphicsRectItem):

    def __init__(self,mytype,point):
        super(Node, self).__init__()
        cont = mytype
        #Path para nó de passagem:
        if cont == 1:
            self.shapes = [self,]
            self.rect = QtCore.QRectF(point.x()+0, point.y()+7, 8, 8)
            self.trif = QtGui.QPolygon()

            self.trif.append(point+QtCore.QPoint(4,7))
            self.trif.append(point+QtCore.QPoint(0,0))
            self.trif.append(point+QtCore.QPoint(8,0))
            self.trif.append(point+QtCore.QPoint(4,7))
            
            # Define e ajusta a posição do label do item gráfico. Começa com
            # um texto vazio.
            self.text = QtGui.QGraphicsTextItem('A', self, self.scene())
            self.text.setPos(self.mapFromItem(self.text, 0, self.rect.height()))

            self.shapes[0].setRect(self.rect)
            self.shapes[1].setPolygon(self.trif)


    def paint(self, painter, option, widget):
        #Desenho do nó de passagem
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            painter.setBrush(QtCore.Qt.black)
            painter.drawRoundedRect(self.rect,5,5)
            painter.drawPolygon(self.shapes[1].trif)
        





if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())
