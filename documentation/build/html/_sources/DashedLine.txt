.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* DashedLine(*[parent]*)
====================================================

**Herança:**

* **parent -** PySide.QtGui.QGraphicsLineItem

Classe que implementa o objeto DashedLine, utilizado para indicar que um elemento do diagrama foi selecionado. Sua representaçao e uma borda tracejada laranja.

Métodos
+++++++

* `paint(painter, option, widget)`_

__init__()
++++++++++
Método construtor (inicial) da classe DashedLine. Chama o construtor da classe parent sem passagem de parâmetros (QtGui.QGraphicsLineItem).

paint(painter, option, widget)
++++++++++++++++++++++++++++++++
**Parâmetros:**

* **painter -** PySide.QtGui.QPainter

* **option -** PySide.QtGui.QStyleOptionGraphicsItem

* **widget -** PySide.QtGui.QGraphicsView.ViewWidget 

Método que desenha o objeto dashedLine, chamado sempre que um objeto novo é selecionado.
