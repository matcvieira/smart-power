#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
import math
import sys

class Cursor(QtGui.QCursor):
    '''
        Classe que implementa o cursor do mouse dentro da aplicação.
    '''

    def __init__(self, image):
        '''
            Método contrutor da classe Cursor.
        '''
        if image == "":
            super(Cursor, self).__init__()
        else:
            super(Cursor, self).__init__(image, -1, -1)

    def setShapeSubs(self, widget):
        '''
            Método que seta o formato do cursor para o ícone de Subestação.
        '''
        cursor = Cursor(QtGui.QBitmap(u"icones/iconSubstation.png"))
        widget.setCursor(cursor)
        print "subs"

    def setShapeRecl(self, widget):
        '''
            Método que seta o formato do cursor para o ícone de Religador.
        '''
        cursor = Cursor(QtGui.QBitmap(u"icones/iconRecloser.png"))
        widget.setCursor(cursor)
        print "recl"

    def setShapeBus(self, widget):
        '''
            Método que seta o formato do cursor para o ícone de Barra #corrigir!!!
        '''
        cursor = Cursor(QtGui.QBitmap(u"icones/iconBus2.png"))
        widget.setCursor(cursor)
        print "bus"

    def setShapeNodeC(self, widget):
        '''
            Método que seta o formato do cursor para o ícone de Nó de Carga.
        '''
        cursor = Cursor(QtGui.QBitmap(u"icones/iconNode.png"))
        widget.setCursor(cursor)
        print "nod"

    def setShapeImage(self, widget, image):
        '''
            Método que seta o formato do cursor para a imagem contida no
            parametro image.
        '''
        cursor = Cursor(image)
        widget.setCursor(cursor)

    def setShapePad(self, widget):
        '''
            Método que seta o formato do cursor para o formato padrão: seta do sistema.
        '''
        cursor = Cursor("")
        widget.setCursor(cursor)
        print "nada"

    def setShape(self, widget, id):
        '''
            Método que seta o formato do cursor para o icone do botao 
            pressionado de acordo com o id passado.
        '''
        if id == 0:
            self.setShapeSubs(widget)
        elif id == 1:
            self.setShapeRecl(widget)
        elif id == 2:
            self.setShapeBus(widget)
        elif id == 4:
            self.setShapeNodeC(widget)
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    cursor = Cursor("")
    app.setOverrideCursor(cursor)
    sys.exit(app.exec_())
