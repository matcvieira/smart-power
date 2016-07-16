.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* Edge(*[parent]*)
===============================================
**Herança:**

* **parent -** PySide.QtGui.QGraphicsLineItem

Classe que implementa o objeto Edge que liga dois objetos Node um ao outro.

Métodos
+++++++

* `get_fraction(pos)`_
* `update_position()`_
* `set_color(color)`_
* `boundingRect()`_
* `paint(painter, option, widget)`_
* `mousePressEvent(mouse_event)`_
* `contextMenuEvent(event)`_

__init__(w1, w2, edge_menu)
++++++++++++++++++++++++++++
**Parâmetros:**

* **w1, w2 -** PySide.QtGui.QGraphicsRectItem.Node

* **edge_menu -** Pyside.QtGui.QMenu

Metodo inicial (construtor) da classe Edge. Recebe como parâmetros os objetos Node Inicial e Final. Define o objeto QtCore.QLineF que define a linha que representa o objeto QtGui.QGraphicsLineItem

get_fraction(pos)
++++++++++++++++++

**Parâmetros:**

* **pos -** PySide.QtCore.QPointF

Esta função obtém uma fração da linha e é utilizada durante o modelo denominado "Sticky to Line" de um nó de carga. Pode ser usado para outros fins em futuras expansões.

update_position()
++++++++++++++++++

Método de atualização da posição do objeto edge implementado pela classe Edge. Sempre que um dos objetos Nodes w1 ou w2 modifica sua posição este método é chamado para que o objeto edge possa acompanhar o movimento dos Objetos Node.

set_color(color)
+++++++++++++++++

**Parâmetro:**

* **color -** PySide.QtGui.QColor

Metodo que seta a cor do objeto Edge como a definida pelo parametro color.

paint(painter, option, widget)
++++++++++++++++++++++++++++++

**Parâmetros:**

* **painter -** PySide.QtGui.QPainter

* **option -** PySide.QtGui.QStyleOptionGraphicsItem

* **widget -** PySide.QtGui.QGraphicsView.ViewWidget 

Metodo de desenho do objeto edge implementado pela classe Edge. A classe executa esta função constantemente.

mousePressEvent(mouse_event)
+++++++++++++++++++++++++++++++++++

**Parâmetros:**

* **mouse_event -** PySide.QtGui.QGraphicsSceneMouseEvent

Metodo chamado quando um objeto da classe edge é pressionado (mousePressEvent).

contextMenuEvent(event)
++++++++++++++++++++++++

**Parâmetros:**

* **event -** PySide.QtGui.QGraphicsSceneContextMenuEvent

Callback chamada quando o botão direito do mouse é pressionado sobre a linha, executando o myLineMenu (QtGui.QMenu), o menu de configuração de condutor. 
 