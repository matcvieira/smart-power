.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* Substation(*[parent]*)
===============================================
**Herança:**

* **parent -** object

Classe que define objetos abstratos do tipo Substation (Subestação).

__init__(nome, tensao_primario, tensao_secundario, potencia, impedancia)
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
**Parâmetros:**

* **nome -** unicode

* **tensao_primario -** unicode

* **tensao_secundario -** unicode

* **potencia -** unicode

* **impedancia -** unicode

Metodo inicial (construtor) da classe Substation. Recebe como parâmetros os valores digitados pelo usuário no diálogo de configuração do elemento (ver DialogSubstation).