.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Arquivo elementos.py
====================

Arquivo que contém as classes abstratas associadas aos objetos do tipo Node e Edge. No caso dos objetos Node, a associação é feita de acordo com a sua função (religador, subestação, barra, nó de passagem ou nó de carga). As configurações e os padrões aqui definidos caracterizam o diagrama como uma RNP e guardam informações necessárias para conversões (ver Arquivo models).

Classes
-------

.. toctree::
   :maxdepth: 1

   Religador<Religador>
   EnergyConsumer<EnergyConsumer>
   Substation<Substation>
   BusBarSection<BusBarSection>
   Condutor<Condutor>
   NoConect<NoConect>
   Terminal<Terminal>

