.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* XMLToDiagram(*[parent]*)
===============================================
**Herança:**

* **parent -** object

Classe que constrói um diagrama gráfico a partir de um arquivo XML.

__init__(scene,file_path)
++++++++++++++++++++++++++++
**Parâmetros:**

* **scene -** PySide.QtGui.QGraphicsScene.SceneWidget

* **file_path -** unicode

Metodo inicial (construtor) da classe XMLToDiagram. Recebe como parâmetros o endereço do arquivo XML (file_path) e o objeto SceneWidget (scene) onde o diagrama será desenhado após a conversão.
