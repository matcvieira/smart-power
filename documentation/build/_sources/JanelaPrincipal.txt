.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* JanelaPrincipal( *[parent = object]* )
===============================================
**Parâmetro: parent** - object

Classe que implementa a interface gráfica do simulador.

Métodos
++++++++++

* `inicializar_componentes( main_window )`_
* `itemInserted( item_type )`_
* `save()`_
* `open()`_
* `setSelect()`_
* `buttonGroupClicked( id )`_
* `retranslateUi( main_window )`_

__init__()
++++++++++++++++++++++++++
Metodo construtor da classe JanelaPrincipal.

inicializar_componentes( main_window )
++++++++++++++++++++++++++++++++++++++
**Parâmetro: main_window** - object.JanelaPrincipal

Método que implementa os componentes da interface gráfica.

itemInserted( item_type )
++++++++++++++++++++++++++
**Parâmetro: item_type** - 

Callback chamada no momento em que um item é inserido no diagrama gráfico.

save()
+++++++

Método que salva os elementos gráficos chamando a função que os codifica em um arquivo XML.

open()
+++++++

Método que abre o arquivo XML salvo anteriormente e chama função que redesenha os elementos graficos.

setSelect()
++++++++++++

Callback chamada no momento em que se faz necessário alterar o modo de seleção para movimentação de itens no diagrama gráfico ou vice-versa.

buttonGroupClicked( id )
+++++++++++++++++++++++++
**Parâmetro: id** - 

Callback chamada no momento em que um botão de inserção de itens é pressionado.

retranslateUi( main_window )
+++++++++++++++++++++++++++
**Parâmetro: main_window** - object.JanelaPrincipal

Callback chamada no momento em que um botão de inserção de itens é pressionado.