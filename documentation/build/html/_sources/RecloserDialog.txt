.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* RecloserDialog(*[parent]*)
===============================================
**Herança:**

* **parent -** PySide.QtGui.QWidget

Classe que implementa a Dialog de configuração do Religador.

Métodos
+++++++

* `setupUi(Dialog)`_
* `en_dis_button()`_
* `update_values(index)`_
* `custom()`_
* `cadastrar(button)`_
* `retranslateUi(Dialog)`_

__init__(item)
++++++++++++++++++++++++++++

**Parâmetros:**

* **item -** PySide.QtCore.QGraphicsItem.Node

Metodo inicial (construtor) da classe RecloserDialog. É chamada quando um objeto da classe Node e do tipo Religador (item) é inserido no diagrama, ou quando um evento DoubleClick é realizado nesse objeto.

setupUi(Dialog)
+++++++++++++++++++++

**Parâmetros:**

* **Dialog -** PySide.QtCore.QDialog

Método que formata a Dialog, definindo:
tamanho, posição de buttons e labels, e suas ações.

en_dis_button()
+++++++++++++++++++++
Método que inativa o botão de confirmar enquanto os campos obrigatórios estiverem vazios, evitando objetos com erros de configuração.

update_values(index)
++++++++++++++++++++++++

**Parâmetros:**

* **index -** PySide.QtCore.int

Método que atualiza os valores exibidos pelas lineEdit da Dialog de configuração para os valores atuais do Religador. O parâmetro index indica quantas vezes o menu foi chamado e, caso seja igual a 0 (nenhuma vez), a função não é executada.

custom()
++++++++++++++++++++++++

Método que seta o cursor sempre para o início da lineEdit mesmo que o o usuário clique no meio da mesma.

cadastrar(button)
++++++++++++++++++++++++

Método que configura a ação do button "cadastrar", executando uma nova Dialog com os parâmetros do religador a preencher (ver Cadastro).

retranslateUi(Dialog)
++++++++++++++++++++++++

**Parâmetros:**

* **Dialog -** PySide.QtCore.QDialog

Método que redefine o conteúdo das labels e buttons da Dialog.
