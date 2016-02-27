.. SmartPower documentation master file, created by
   sphinx-quickstart on Thu Jul 16 09:57:33 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*class* Cursor(*[parent]*)
===============================================
**Herança:**

* **parent -** PySide.QtGui.QCursor

Classe que implementa o cursor do mouse dentro da aplicação.

Métodos
+++++++

* `setShapeSubs(widget)`_
* `setShapeRecl(widget)`_
* `setShapeNodeC(widget)`_
* `setShapeBus(widget)`_
* `setShapeImage(widget,image)`_
* `setShapePad(widget)`_
* `setShape(widget,id)`_

__init__(image)
++++++++++++++++++++++++++++
**Parâmetros:**

* **image -** unicode

Metodo inicial (construtor) da classe Cursor. Cria um cursor com a imagem que se econtra no endereço dado pelo parâmetro image.

setShapeSubs(widget)
+++++++++++++++++++++

**Parâmetros:**

* **widget -** PySide.QtCore.QWidget

Método que seta o formato do cursor para o ícone de Subestação.

setShapeRecl(widget)
+++++++++++++++++++++

**Parâmetros:**

* **widget -** PySide.QtCore.QWidget

Método que seta o formato do cursor para o ícone de Religador.

setShapeBus(widget)
+++++++++++++++++++++

**Parâmetros:**

* **widget -** PySide.QtCore.QWidget

Método que seta o formato do cursor para o ícone de Barra

setShapeNodeC(widget)
+++++++++++++++++++++

**Parâmetros:**

* **widget -** PySide.QtCore.QWidget

Método que seta o formato do cursor para o ícone de Nó de Carga.

setShapeImage(widget,image)
+++++++++++++++++++++++++++++++

**Parâmetros:**

* **widget -** PySide.QtCore.QWidget

* **image -** unicode

Método que seta o formato do cursor para a imagem no endereço dado pelo parâmetro image.

setShapePad(widget)
+++++++++++++++++++++

**Parâmetros:**

* **widget -** PySide.QtCore.QWidget

Método que seta o formato do cursor para o formato padrão do sistema.

setShape(widget,id)
+++++++++++++++++++++++++++++++

**Parâmetros:**

* **widget -** PySide.QtCore.QWidget

* **id -** PySide.QtCore.int

Método que seta o formato do cursor para o icone do button pressionado de acordo com o id do button.
