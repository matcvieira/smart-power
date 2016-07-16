.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* AddRemoveCommand(*[parent]*)
====================================================
**Herança:**

* **parent -** PySide.QtGui.QUndoCommand

Classe que implementa os comandos "desfazer"(undo) e "refazer"(redo) em itens do diagrama gráfico.

Métodos
+++++++
* `undo()`_
* `redo()`_

__init__(mode,scene,item)
++++++++++++++++++++++++++++++++++
**Parâmetros:**

* **mode -** PySide.QtGui.QGraphicsScene.SceneWidget
* **scene -** PySide.QtGui.QGraphicsScene.SceneWidget
* **item -** PySide.QtGui.QGraphicsItem.item

Método construtor da classe AddRemoveCommand, é chamado sempre que um objeto da classe node (item) é adicionado ao ou removido do diagrama gráfico (scene). O parâmetro mode define qual ação (remoção ou inserção) foi realizada e permite que a mesma possa ser desfeita (ou refeita), pois uma cópia do objeto Node é armazenada no objeto AddRemoveCommand criado.

redo()
+++++++++++++++++++

Refaz uma ação que foi desfeita.

undo()
+++++++++++++++++++

Desfaz a última ação de remoção ou inserção de item realizada.