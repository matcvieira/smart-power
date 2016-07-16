.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* Terminal(*[parent]*)
===============================================
**Herança:**

* **parent -** object

Classe que define objetos abstratos do tipo Terminal.

Métodos
+++++++

* `connect()`_
* `disconnect()`_
* `delete_from_list()`_


__init__(parent,connected)
++++++++++++++++++++++++++++++
**Parâmetros:**

* **parent -** PySide.QtGui.QGraphicsItem.Node

* **connected -** PySide.QtCore.bool

Metodo inicial (construtor) da classe NoConect. Recebe como parâmetros um objeto da classe Node (parent) e um booleano (connected) que indica se o objeto está ou não conectado.

connect()
+++++++++++++++

Seta o objeto da classe terminal como conectado.

disconnect()
+++++++++++++++

Seta o objeto da classe terminal como desconectado.

delete_from_list()
++++++++++++++++++++

Apaga o terminal do nó conectivo ao qual ele estava associado, removendo-o das listas de terminais desse nó.


