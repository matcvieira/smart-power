.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* ControlMainWindow(*[parent = PySide.QtGui.QMainWindow]*)
====================================================================

Classe que cria a janela principal do programa.

Métodos
+++++++

* `mouseReleaseEvent(mouse_event)`_
* `setCursorIcon(id)`_
* `setCursorPad(id)`_

__init__()
++++++++++++++++++++++++++++++++++++++++++++++++++

Metodo inicial (construtor) da classe ControlMainWindow. Chama o metodo construtor da classe QtGui.QMainWindow passando como parametro parent.

mouseReleaseEvent(mouse_event)
+++++++++++++++++++++++++++++++

**Parâmetros:**

* **mouse_event -** PySide.QtGui.QMouseEvent

Função da chamada no momento que o evento mouse release é enviado. Quando um item arrastado para a área de desenho é liberado, este item é desenhado e o programa volta para o modo de seleção de itens.
        
setCursorIcon(id)
+++++++++++++++++

**Parâmetros:**

* **id -** PySide.QtCore.int

Callback que altera o formato do cursor dando a impressão visual de 'arrastar' o elemento para dentro do diagrama gráfico.

setCursorPad(id)
++++++++++++++++++

**Parâmetros:**

* **id -** PySide.QtCore.int

Função que altera o formato do cursor para a seta padrão. 