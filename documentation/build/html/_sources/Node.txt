.. SmartPower documentation m
.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* Node(*[parent*)
====================================================

**Herança:**

* **parent -** QtGui.QGraphicsTextItem

Classe que implementa o objeto DashedLine, utilizado para indicar que um elemento do diagrama foi selecionado. Sua representaçao é uma linha tracejada laranja ao redor do item selecionado.

Métodos
++++++++

* `fix_item()`_
* `update_count()`_
* `remove_edges()`_
* `remove_edge(edge)`_
* `add_edge(edge)`_
* `edge_position(edge)`_
* `center()`_
* `set_center(pos)`_
* `boundingRect()`_
* `paint(painter,option,widget)`_
* `itemChange(change,value)`_
* `MousePressEvent(mouse_event)`_
* `MouseMoveEvent(mouse_event)`_
* `MouseReleaseEvent(mouse_event)`_
* `MouseDoubleClickEvent(event)`_
* `MouseReleaseEvent(event)`_
* `adjust_in_grid(pos)`_
* `contextMenuEvent(event)`_


__init__(self,item_type,node_menu,parent[=None],scene[=None])
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

**Parametros:** 

* **item_type -** PySide.QtCore.int

* **parent -** PySide.QtGui.QGraphicsView.ViewWidget [or None]

* **scene -** PySide.QtGui.QGraphicsScene.SceneWidget [or None]

* **node_menu -** Pyside.QtGui.QMenu

Método inicial da classe Node.
Recebe como parâmetros os objetos myItemType (que define o tipo de Node desejado) e o menu desejado (menu que abre com clique direito). Analogamente ao que acontece com a Edge, este item é apenas a representação de um retângulo do tipo QtCore.QRectF.

fix_item()
+++++++++++++++
Seta a flag de fixação do item.

update_count()
+++++++++++++++++
Atualiza o contador que acompanha o número de Edges do item.

remove_edges()
+++++++++++++++++

Método de remoção de todos objetos Edge associados ao objeto node.

remove_edge(edge)
++++++++++++++++++++++++++++++++

**Parâmetros:**

* **edge** - PySide.QtGui.QGraphicsLineItem.Edge

Método de remoção da edge passada como parâmetro do item presente.

add_edge(edge)
++++++++++++++++++++++++++++++++++

**Parâmetros:**

* **edge** - PySide.QtGui.QGraphicsLineItem.Edge

Método de associação de objetos edge ao objeto node.
 
edge_position(edge)
+++++++++++++++++++++++++++++++++++++++++++

**Parâmetros:**

* **edge** - PySide.QtGui.QGraphicsLineItem.Edge

Este método é utilizado da distribuição das Edges ligadas numa barra, seguindo uma lógica de alinhamento.

center()
+++++++++

**Retorno:** PySide.QtCore.QPointF

Método que retorna o centro do objeto passado

set_center(pos)
++++++++++++++++++

**Parâmetros:**

**pos -** PySide.QtCore.QPointF

Método que define o posicionamento do objeto na tela de desenho setando o seu ponto central.

boundingRect()
+++++++++++++++
Reimplementação da função virtual que especifica a borda do objeto node

paint(painter,option,widget)
++++++++++++++++++++++++++++++

**Parâmetros:**

* **painter -** PySide.QtGui.QPainter

* **option -** PySide.QtGui.QStyleOptionGraphicsItem

* **widget -** PySide.QtGui.QGraphicsView.ViewWidget 

Método de desenho do objeto node implementado pela classe Node.Aqui se diferencia os objetos pela sua forma. Todos eram definidos por um retângulo QtCore.QRectF. Neste método, serão desenhadas suas formas baseadas em seus retângulos.

itemChange(change,value)
++++++++++++++++++++++++++++++++
**Parâmetros:**

* **change -** PySide.QtGui.QGraphicsItem.Node.GraphicsItemChange

* **value -** object	

Método que detecta mudanças na posição do objeto Node.

mousePressEvent(mouse_event)
++++++++++++++++++++++++++++++

**Parâmetros:**

* **mouse_event -** PySide.QtGui.QGraphicsSceneMouseEvent

Reimplementação da função virtual que define o evento referente ao aperto de botão do mouse.

mouseMoveEvent(mouse_event):
+++++++++++++++++++++++++++++++++++++++++++

**Parâmetros:**

* **mouse_event -** PySide.QtGui.QGraphicsSceneMouseEvent

Reimplementação da função virtual que define o evento referente ao movimento do mouse durante enquanto este pressiona um item.

mouseReleaseEvent(mouse_event):
+++++++++++++++++++++++++++++++++++++++

**Parâmetros:**

* **mouse_event -** PySide.QtGui.QGraphicsSceneMouseEvent

Reimplementação da função virtual que define o evento referente ao soltar do botão mouse após aperto.

mouseDoubleClickEvent(event)
++++++++++++++++++++++++++++++

**Parâmetros:**

* **event -** PySide.QtGui.QGraphicsSceneMouseEvent

Reimplementação da função de duplo clique do mouse.

mouseReleaseEvent(event)
++++++++++++++++++++++++++

**Parâmetros:**

* **event -** PySide.QtGui.QGraphicsSceneMouseEvent

Reimplementação da função virtual que define o evento lançado quando o botão do mouse é liberado.

adjust_in_grid(pos)
+++++++++++++++++++++

**Parâmetros:**

* **pos -** PySide.QtCore.QPointF

Este método implementa uma grade invisível na cena, que limita o movimento dos Nodes para posições bem definidas.

contextMenuEvent(event)
++++++++++++++++++++++++++++++

**Parâmetros:**

* **event -** PySide.QtGui.QGraphicsSceneContextMenuEvent

Método que reimplementa a função virtual do menu aberto pelo clique com botão direito.

