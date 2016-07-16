.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* DiagramToXML(*[parent]*)
===============================================
**Herança:**

* **parent -** xml.etree.ElementTree.Element

Esta classe possui as funções que armazenam as informações necessárias à conversão do diagrama grafico em um arquivo XML

Métodos
+++++++

* `write_xml(path)`_


__init__(scene)
++++++++++++++++++++++++++++
**Parâmetros:**

* **scene -** PySide.QtGui.QGraphicsScene.SceneWidget

Metodo inicial (construtor) da classe DiagramToXML. Recebe como parâmetro o objeto SceneWidget que contém o diagrama a ser convertido.

write_xml(path)
++++++++++++++++++

**Parâmetros:**

* **path -** unicode

Função que cria o arquivo XML na localização indicada pelo argumento path.
