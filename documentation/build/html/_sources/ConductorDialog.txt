.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* ConductorDialog(*[parent]*)
===============================================
**Herança:**

* **parent -** PySide.QtGui.QWidget

Classe que implementa a Dialog de configuração do condutor.

Métodos
+++++++

* `setupUi(Dialog)`_
* `retranslateUi(Dialog)`_

__init__(item)
++++++++++++++++++++++++++++

**Parâmetros:**

* **item -** PySide.QtCore.QGraphicsItem.Node

Metodo inicial (construtor) da classe ConductorDialog. É chamada um evento DoubleClick é realizado em um objeto da classe Edge.

setupUi(Dialog)
+++++++++++++++++++++

**Parâmetros:**

* **Dialog -** PySide.QtCore.QDialog

Método que formata a Dialog, definindo:
tamanho, posição de buttons e labels, e suas ações.

retranslateUi(Dialog)
++++++++++++++++++++++++

**Parâmetros:**

* **Dialog -** PySide.QtCore.QDialog

Método que redefine o conteúdo das labels e buttons da Dialog.
