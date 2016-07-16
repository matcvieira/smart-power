.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* EnergyConsumer(*[parent]*)
===============================================
**Herança:**

* **parent -** object

Classe que define objetos abstratos do tipo EnergyConsumer (Nó de Carga).

__init__(nome, pfixed, qfixed)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**Parâmetros:**

* **nome -** unicode

* **pfixed -** PySide.QtCore.int [=0]

* **qfixed -** PySide.QtCore.int [=0]

Metodo inicial (construtor) da classe EnergyConsumer. Recebe como parâmetros os valores digitados pelo usuário no diálogo de configuração do elemento (ver DialogEnergyConsumer).