.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* CimXML(*[parent]*)
===============================================
**Herança:**

* **parent -** object

Classe que representa os dados dos componentes em padrão CIM

Métodos
+++++++

* `write_xml(path)`_
* `montar_rede(scene)`_

__init__(scene,file_path)
++++++++++++++++++++++++++++
**Parâmetros:**

* **scene -** PySide.QtGui.QGraphicsScene.SceneWidget

Metodo inicial (construtor) da classe CimXML. Recebe como parâmetro o objeto SceneWidget que contém o diagrama gráfico.

write_xml(path)
++++++++++++++++++

**Parâmetros:**

* **path -** unicode

Função que cria o arquivo XML na localização indicada pelo argumento path.

montar_rede(scene)
++++++++++++++++++

**Parâmetros:**

* **scene -** PySide.QtGui.QGraphicsScene.SceneWidget

Função que lê os elementos contidos na scene, os classifica e os divide em listas de acordo com a função deles na rede, para então montar a rede seguindo o padrão CIM.