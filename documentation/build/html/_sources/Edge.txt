.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* Edge( *[parent = QGraphicsLineItem]* )
===============================================
**Parâmetro: parent** - QtGui.QGraphicsLineItem

Classe que implementa o objeto Edge que liga dois objetos Node um ao outro.

Métodos
+++++++

* `get_fraction(pos)`_
* `update_position()`_
* `set_color(color)`_
* `boundingRect()`_
* `paint(painter, option, widget)`_
* `mousePressEvent(mouse_event)`_
* `contestMenuEvent(event)`_

__init__(w1, w2, edge_menu)
++++++++++++++++++++++++++++++++++++++++++++++
**Parâmetros:**

**w1, w2** - QtGui.QGraphicsRectItem.Node

**edge_menu** - QtGui.QGraphicsLineItem

Metodo inicial (construtor) da classe Edge. Recebe como parâmetros os objetos Node Inicial e Final. Define o objeto QtCore.QLineF que define a linha que representa o objeto QtGui.QGraphicsLineItem

get_fraction(pos)
++++++++++++++++++
**Parâmetro: pos** -

Descriçao...

update_position()
++++++++++++++++++
``Retorna a nova posição do objeto`` ...............

set_color(color)
+++++++++++++++++
**Parâmetro: color** - QtGui.QColor

Descriçao....

boundingRect()
++++++++++++++++
Descriçao...

paint(painter, option, widget)
++++++++++++++++++++++++++++++

**Parâmetros:**

**painter** -

**option** -

**widget** -

Descriçao....

mousePressEvent(mouse_event)
+++++++++++++++++++++++++++++++++++

**Parâmetro: mouse_event** -

contestMenuEvent(event)
++++++++++++++++++++++++

**Parâmetro: - event**


 