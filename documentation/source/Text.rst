.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* Text(*[parent]*)
===============================================
**Herança:**

* **parent -** QtGui.QGraphicsTextItem

Classe que implementa o objeto Text Genérico.

Métodos
+++++++

* `itemChange(change, value)`_
* `focusOutEvent(event)`_

__init__(text,parent[=None],scene[=None])
++++++++++++++++++++++++++++++++++++++++++++++
**Parâmetros:**

* **text -** unicode

* **parent -** PySide.QtGui.QGraphicsItem.Node

* **scene -** PySide.QtGui.QGraphicsScene.SceneWidget


itemChange(change, value)
++++++++++++++++++++++++++++

**Parâmetros:** 

* **change -** PySide.QtGui.QGraphicsItem.Node.GraphicsItemChange

* **value -** object	

Função virtual reimplementada para emitir sinal de mudança (ver Pyside, QGraphicsTextItem)

focusOutEvent(event)
+++++++++++++++++++++
**Parâmetros:**

* **event -** QtGui.QFocusEvent

Função virtual reimplementada para emitir sinal de perda de foco (ver Pyside, QGraphicsTextItem)
