.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* BarraDialog(*[parent]*)
===============================================
**Herança:**

* **parent -** PySide.QtGui.QWidget

Classe que implementa a Dialog de configuração da barra.

Métodos
+++++++

* `setupUi(Propriedades)`_
* `retranslateUi(Propriedades)`_

__init__(item)
++++++++++++++++++++++++++++

**Parâmetros:**

* **item -** PySide.QtCore.QGraphicsItem.Node

Metodo inicial (construtor) da classe SubstationDialog. É chamada quando um objeto da classe Node e do tipo BusBar (item) é inserido no diagrama, ou quando um evento DoubleClick é realizado nesse objeto.


setupUi(Propriedades)
+++++++++++++++++++++

**Parâmetros:**

* **Propriedades -** PySide.QtCore.QDialog

Método que formata a Propriedades, definindo:
tamanho, posição de buttons e labels, e suas ações.

retranslateUi(Propriedades)
++++++++++++++++++++++++

**Parâmetros:**

* **Propriedades -** PySide.QtCore.QDialog

Método que redefine o conteúdo das labels e buttons da Propriedades.
