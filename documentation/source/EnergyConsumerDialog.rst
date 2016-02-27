.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* EnergyConsumerDialog(*[parent]*)
===============================================
**Herança:**

* **parent -** PySide.QtGui.QWidget

Classe que implementa a Dialog de configuração do Nó de carga.

Métodos
+++++++

* `setupUi(Dialog)`_
* `en_dis_button()`_
* `retranslateUi(Dialog)`_

__init__(item)
++++++++++++++++++++++++++++

**Parâmetros:**

* **item -** PySide.QtCore.QGraphicsItem.Node

Metodo inicial (construtor) da classe EnergyConsumerDialog. É chamada quando um objeto da classe Node e do tipo Nó de carga (item) é inserido no diagrama, ou quando um evento DoubleClick é realizado nesse objeto.

setupUi(Dialog)
+++++++++++++++++++++

**Parâmetros:**

* **Dialog -** PySide.QtCore.QDialog

Método que formata a Dialog, definindo:
tamanho, posição de buttons e labels, e suas ações.

en_dis_button()
+++++++++++++++++++++
Método que inativa o botão de confirmar enquanto os campos obrigatórios estiverem vazios, evitando objetos com erros de configuração.

retranslateUi(Dialog)
++++++++++++++++++++++++

**Parâmetros:**

* **Dialog -** PySide.QtCore.QDialog

Método que redefine o conteúdo das labels e buttons da Dialog.
