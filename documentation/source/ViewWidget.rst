.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* ViewWidget(*[parent]*)
====================================================
**Herança:**

* **parent -** PySide.QtGui.QGraphicsView

Esta classe implementa o container QGraphicsView onde residirá o objeto QGraphicsScene.

Métodos
+++++++
* `wheelEvent(event)`_
* `scale_view(scale_factor)`_

__init__(scene)
++++++++++++++++++
**Parâmetros:**

* **scene -** PySide.QtGui.QGraphicsScene.SceneWidget

Método construtor da classe ViewWidget.


wheelEvent(event)
+++++++++++++++++++

**Parâmetros:**

* **event -** PySide.QtGui.GraphicsSceneWheelEvent

Função que implementa a ação de girar o scroll do mouse, ampliando ou reduzindo o zoom do diagrama.


scale_view(scale_factor)
+++++++++++++++++++++++++++++++

**Parâmetros:**

* **scale_factor -** PySide.QtCore.qreal

Função que calcula o fator de escala aplicado ao diagrama, alterando o tamanho do mesmo e simulando a função zoom.