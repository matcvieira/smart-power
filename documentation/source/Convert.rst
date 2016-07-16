.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* Convert(*[parent]*)
===============================================
**Herança:**

* **parent -** object

Classe que realiza a conversão da rede padrão CIM salva em um arquivo .xml em uma rede padrão RNP.

Métodos
+++++++

* `get_fraction(pos)`_
* `update_position()`_
* `set_color(color)`_
* `boundingRect()`_
* `paint(painter, option, widget)`_
* `mousePressEvent(mouse_event)`_
* `contextMenuEvent(event)`_

__init__(cim_path)
++++++++++++++++++++++++++++
**Parâmetro:**

* **cim_path -** unicode [=None]

Metodo inicial (construtor) da classe Convert. Recebe como parâmetro o endereço do arquivo XML em padrão CIM, e a partir dele monta a RNP.