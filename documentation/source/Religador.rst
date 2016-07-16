.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* Religador(*[parent]*)
===============================================
**Herança:**

* **parent -** object

Classe que define objetos abstratos do tipo Religador.

__init__(nome, rated_current, in_transit_time, breaking_capacity, reclose_sequences, estado)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**Parâmetros:**

* **nome -** unicode [=None]

* **rated_current -** unicode [=None]

* **in_transit_time -** unicode [=None]

* **breaking_capacity -** unicode [=None]

* **reclose_sequences -** unicode [=None]

* **estado -** PySide.QtCore.int [=1]

Metodo inicial (construtor) da classe Religador. Recebe como parâmetros os valores digitados pelo usuário no diálogo de configuração do elemento (ver DialogRecloser).