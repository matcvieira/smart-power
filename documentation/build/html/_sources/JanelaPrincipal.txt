.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* JanelaPrincipal(*[parent]*)
===============================================

**Herança:**

* **parent -** object

Classe que implementa a interface gráfica do simulador.

Métodos
++++++++++

* `inicializar_componentes(main_window)`_
* `itemInserted(item_type)`_
* `save()`_
* `open()`_
* `setSelect()`_
* `buttonGroupClicked(id)`_
* `buttonGroupPressed(id)`_
* `buttonGroupReleased()`_
* `buttonGroupUncheck()`_
* `retranslateUi(main_window)`_

__init__()
++++++++++++++++++++++++++
Metodo construtor da classe JanelaPrincipal.

inicializar_componentes(main_window)
+++++++++++++++++++++++++++++++++++++++++++++++++++

**Parâmetros:**

* **main_window -** Pyside.QtGui.QMainWindow.ControlMainWindow

Método que implementa os componentes da interface gráfica.

itemInserted(item_type)
++++++++++++++++++++++++++
**Parâmetros:**

* **item_type -** PySide.QtCore.int 

Callback chamada no momento em que um item é inserido no diagrama gráfico.

save()
+++++++

Método que salva os elementos gráficos chamando a função que os codifica em um arquivo XML.

open()
+++++++

Método que abre o arquivo XML salvo anteriormente e chama função que redesenha os elementos graficos.

setSelect()
++++++++++++

Callback chamada no momento em que se faz necessário alterar o modo de seleção para movimentação de itens no diagrama gráfico ou vice-versa.

buttonGroupClicked(id)
+++++++++++++++++++++++++
 
**Parâmetros:**

* **id -** PySide.QtCore.int

Callback chamada no momento em que um botão de inserção de itens é pressionado.

buttonGroupPressed(id)
++++++++++++++++++++++++++++++

**Parâmetros:**

* **id -** PySide.QtCore.int

Callback chamada no momento em que um botão de inserção de itens é pressionado.

buttonGroupReleased()
++++++++++++++++++++++

Callback chamada no momento em que um botão de inserção de itens é liberado.

buttonGroupUncheck()
+++++++++++++++++++++++++
            
Callback chamada para remover a seleção de todos os buttons.

retranslateUi(main_window)
+++++++++++++++++++++++++++
**Parâmetros:**

* **main_window -** Pyside.QtGui.QMainWindow.ControlMainWindow

Callback chamada no momento em que um botão de inserção de itens é pressionado.