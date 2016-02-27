.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* SceneWidget(*[parent]*)
====================================================
**Herança:**

* **parent -** PySide.QtGui.QGraphicsScene

Classe que implementa o container gráfico onde os elementos (religadores, barras, subestações, nós de carga e condutores) residirão, denominado cena.

Métodos
+++++++
* `create_dict_recloser(corrente,capacidade,num_rel,padrao)`_
* `mousePressEvent(mouse_event)`_
* `mouseMoveEvent(mouse_event)`_
* `mouseReleaseEvent(mouse_event)`_
* `mouseDoubleClickEvent(mouse_event)`_
* `keyPressEvent(event)`_
* `keyReleaseEvent(event)`_
* `setTextSubstation()`_
* `setTextRecloser()`_
* `setTextNodeC()`_
* `setTextBus()`_
* `break_edge(edge,mode,original_edge,insert)`_
* `recover_edge(item)`_
* `set_item_type(type)`_
* `set_mode(mode)`_
* `change_state()`_
* `create_actions()`_
* `create_menus()`_
* `delete_item()`_
* `launch_dialog()`_
* `increase_bus()`_
* `decrease_bus()`_
* `align_line_h()`_
* `align_line_v()`_
* `h_align()`_
* `v_align()`_
* `set_grid()`_
* `simulate()`_

__init__(window)
++++++++++++++++++

**Parâmetros:**

* **window -** object.JanelaPrincipal

Método construtor da classe SceneWidget, realiza a definição de flags, atributos auxiliares e da geometria inicial da cena. Cria também as ações, os menus executados na cena e o dicionário padrão dos relés.


create_dict_recloser(corrente,capacidade,num_rel,padrao)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Parâmetros:**

* **corrente -** unicode

* **capacidade -** unicode

* **num_rel -** unicode

* **padrao -** PySide.QtCore.int

Este método cria um dicionário de um padrão de religador comercial, de acordo com os parâmetros passados.

mousePressEvent(mouse_event)
+++++++++++++++++++++++++++++++

**Parâmetros:**

* **mouse_event -** PySide.QtGui.QGraphicsSceneMouseEvent

Este método define as ações realizadas quando um evento do tipo mousePress é detectado no diagrama gráfico.

mouseMoveEvent(mouse_event)
++++++++++++++++++++++++++++++++++

**Parâmetros:**

* **mouse_event -** PySide.QtGui.QGraphicsSceneMouseEvent

Este método define as ações realizadas quando um evento do tipo mouseMove é detectado no diagrama grafico.

mouseReleaseEvent(mouse_event)
+++++++++++++++++++++++++++++++++++

**Parâmetros:**

* **mouse_event -** PySide.QtGui.QGraphicsSceneMouseEvent

Este método define as ações realizadas quando um evento do tipo mouseRelease e detectado no diagrama grafico. Neste caso conecta os dois elementos que estão ligados pela linha criada no evento mousePress.

mouseDoubleClickEvent(mouse_event)
++++++++++++++++++++++++++++++++++++++++++

**Parametros:**

* **mouse_event -** PySide.QtGui.QGraphicsSceneMouseEvent

Este método define as ações realizadas quando um evento do tipo mouseDoubleClick e detectado no diagrama grafico. Neste caso abre o diálogo de configuração de parâmetros.

keyPressEvent(event)
+++++++++++++++++++++++++

**Parâmetros:**

* **event -** PySide.QtGui.QKeyEvent 

Método que implementa a ação de pressionar qualquer tecla.

keyReleaseEvent(event)
++++++++++++++++++++++++++++++

**Parâmetros:**

* **event -** PySide.QtGui.QKeyEvent 

Método que implementa a ação de liberar qualquer tecla.

setTextSubstation()
+++++++++++++++++++++

Altera o parâmetro visibility da classe Node que seta a visibilidade dos textos dos objetos Node do tipo Subestação.

setTextRecloser()
++++++++++++++++++
Altera o parâmetro visibility da classe Node que seta a visibilidade dos textos dos objetos Node do tipo Religador.

setTextNodeC()
+++++++++++++++
Altera o parâmetro visibility da classe Node que seta a visibilidade dos textos dos objetos Node do tipo Nó de carga.

setTextBus()
+++++++++++++
Altera o parâmetro visibility da classe Node que seta a visibilidade dos textos dos objetos Node do tipo Barra.

break_edge(edge,mode,original_edge,insert)
++++++++++++++++++++++++++++++++++++++++++++++++++

**Parametros:**

* **edge -** PySide.QtGui.QGraphicsLineItem.Edge
* **mode -** PySide.QtCore.int
* **original_edge -** PySide.QtGui.QGraphicsLineItem.Edge
* **insert -** PySide.QtGui.QGraphicsLineItem.Node

Função break_edge usada para quebrar a linha quando a inserção é a partir ou em cima de uma linha. (Não implementada no modo de arrastar itens).

recover_edge(item)
+++++++++++++++++++++++++++++++++
**Parametros:**

* **item**- PySide.QtGui.QGraphicsLineItem.Node

Definição da função de recuperar uma linha quando está foi quebrada.

set_item_type(type)
+++++++++++++++++++++
**Parametros:**

**type**- PySide.QtCore.int

Define em qual tipo de item será inserido no diagrama grafico assim que um evento do tipo mousePress for detectado, podendo ser:
            Node.Subestacao
            Node.Religador
            Node.Barra
            Node.Agent

set_mode(mode)
++++++++++++++++++
**Parâmetros:**

* **mode -** PySide.QtCore.int

Define o modo em que o sistema está atuando (seleção de item, inserção de item ou inserção de linha).

change_state()
+++++++++++++++++++++++++
Define a função que muda o estado do religador. Esta função será chamada no momento que o usuário tiver selecionado um religador e pressionado a barra de espaço.

create_actions()
+++++++++++++++++++++
Este método cria as ações que serão utilizadas nos menus dos itens gráficos.

create_menus()
+++++++++++++++
Este metodo cria os menus de cada um dos itens gráficos: religador, subestação, barra e linha.
Auto-explicativo: ver QtGui.QMenu na biblioteca do Pyside.

delete_item()
++++++++++++++++++++
Este método implementa a ação de exclusão de um item gráfico do diagrama.

launch_dialog()
+++++++++++++++++++
Este método inicia os diálogos de configuração de cada um dos itens gráficos do diagrama.

increase_bus()
+++++++++++++++++++++
Este método implementa a ação de aumentar o tamanho do item gráfico barra.

decrease_bus()
++++++++++++++++++++
Este método implementa a ação de diminuir o tamanho do item gráfico barra.

align_line_h()
+++++++++++++++
Este método implementa a ação de alinhar horizontalmente os objetos da classe Line no diagrama gráfico.
        
align_line_v()
+++++++++++++++
Este método implementa a ação de alinhar verticalmente os objetos da classe Line no diagrama gráfico.

h_align()
++++++++++++++
Este método implementa a ação de alinhar horizontalmente os objetos da classe Node no diagrama gráfico.

v_align()
++++++++++
Este método implementa a ação de alinhar verticalmente os objetos da classe Node no diagrama gráfico.

set_grid()
+++++++++++
Cria uma grade no desenho, impondo posições pré-determinadas aos elementos 

simulate()
++++++++++++++++++
Inicia a simulação: cálculos de fluxo de carga e curto circuito

