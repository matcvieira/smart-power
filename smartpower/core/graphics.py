#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PySide import QtCore, QtGui
import math
import sys
# Importa os módulos necessários para implementação do diagrama gráfico
from elementos import Religador, BusBarSection, Substation, Condutor
from elementos import EnergyConsumer
from smartpower.gui.dialogs.DialogRecloser import RecloserDialog
from smartpower.gui.dialogs.DialogBarra import BarraDialog
from smartpower.gui.dialogs.DialogConductor import ConductorDialog
from smartpower.gui.dialogs.DialogSubstation import SubstationDialog
from smartpower.gui.dialogs.DialogEnergyConsumer import EnergyConsumerDialog
from smartpower.gui.dialogs.aviso_conexao import AvisoConexaoDialog
from smartpower.gui.dialogs.avisoReligador import AvisoReligador

from smartpower.core import Bridge

from smartpower.calc import xml2objects


lista_no_conectivo = []

class DashedLine(QtGui.QGraphicsLineItem):
    '''
        Classe que implementa o objeto DashedLine, utilizado para indicar que um
        elemento do diagrama foi selecionado. Sua representaçao e uma borda
        tracejada laranja.
    '''

    def __init__(self):
        '''
            Metodo construtor (inicial) da classe DashedLine. Chama o construtor
            da classe parent sem passar parametros(QtGui.QGraphicsLineItem).
        '''
        super(DashedLine, self).__init__()

    def paint(self, painter, option, widget):
        '''
            Metodo que desenha o objeto dashedLine, chamado sempre que um objeto
            novo e selecionado.
        '''
        painter.setPen(QtGui.QPen(QtCore.Qt.red,  # QPen Brush
                                                    2,  # QPen width
                                                    QtCore.Qt.DashLine,
                                                    # QPen style
                                                    QtCore.Qt.SquareCap,
                                                    # QPen cap style
                                                    QtCore.Qt.RoundJoin)
                       # QPen join style
                       )
        painter.drawLine(self.line())  


class Edge(QtGui.QGraphicsLineItem):
    '''
        Classe que implementa o objeto Edge que liga dois objetos Node um ao
        outro
    '''
    def __init__(self, w1, w2, edge_menu):
        '''
            Metodo inicial da classe Edge
            Recebe como parâmetros os objetos Node Inicial e Final
            Define o objeto QtCore.QLineF que define a linha que
            representa o objeto QtGui.QGraphicsLineItem.
        '''
        # A class edge representará graficamente os condutores no diagrama.
        # Nesta classe está presente a sua definição, assim como suas funções
        # necessárias para alinhamento e ligação.
        # NOTA IMPORTANTE: A Edge representa gráficamente uma linha. Sendo
        # assim, ela possui uma linha virtual em que a classe se baseia para
        # desenhar a linha de fato. Edge é um objeto do tipo
        # QtGui.QGraphicsLineItem. Sua linha é definida por um objeto do tipo
        # QtCore.QLineF. (Ver esta duas funções na biblioteca PySide)
        super(Edge, self).__init__()
        self.id = id(self)
        self.w1 = w1
        self.w2 = w2
        # Adiciona o objeto edge as lista de w1 e w2, respectivamente.
        self.w1.add_edge(self)
        self.w2.add_edge(self)
        # Associa o menu edge a ser passado para abertura de dialog.
        self.myEdgeMenu = edge_menu
        # Cria e configura a linha que liga os itens w1 e w2.
        line = QtCore.QLineF(self.w1.pos(), self.w2.pos())
        self.setLine(line)
        self.setZValue(-1)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        # Cria uma flag que determina se a edge está ou não fixa a uma barra
        self.isFixed = False
        # Cria uma flag que fixa a edge numa barra.
        self.fixFlag = False
        # Cria uma flag que determina se a edge é ou não permanente.
        self.isPermanent = False
        # Cria um atributo "linha", que é um objeto do tipo condutor. Este
        # objeto será utilizado para representar os dados elétricos do
        # condutor. Os dados são iniciados nulos e depois serão setados por
        # meio dos menus. Ver classe "Condutor" em elementos.py.
        self.linha = Condutor(0, 0, 0, 0, 0, 0)

        # Análise: se um item (w1 ou w2) que a linha conecta for uma barra,
        # seta-se um atributo desta barra, denominado "bar_busy", como True,
        # indicando que a barra está "ocupada".
        if w1.myItemType == Node.Barra or w2.myItemType == Node.Barra:
            self.isPermanent = True
            if w1.myItemType == Node.Barra:
                w1.bar_busy = True
            if w2.myItemType == Node.Barra:
                w2.bar_busy = True

    def get_fraction(self, pos):
        '''
            Esta função obtém uma fração da linha e é utilizada durante o
            modelo que denomino "Sticky to Line" de um nó de carga. Pode ser
            usado para outros fins em futuras expansões.
        '''
        # Define os limites (horizontal e vertical) da linha, ou seja, a
        # diferença entre os pontos x2 e x1 e os pontos y2 e y1 da linha
        # (supondo uma linha que liga (x1,y1) a (x2,y2)).
        delta_x = math.fabs(self.line().p2().x() - self.line().p1().x())
        delta_y = math.fabs(self.line().p2().y() - self.line().p1().y())

        # "dist" representa a distância entre o ponto presente na posição
        # "pos", passada na chamada da função, e o ponto inicial da linha.
        # Esta distância é dada pela relação matemática que descreve a
        # distância entre dois pontos:
        # L = ((x1 - x2)² + (y1 - y2)²)^(1/2)
        dist = math.sqrt(pow(pos.x() - self.line().p1().x(), 2)
                         + pow(pos.y() - self.line().p1().y(), 2))
        # Este é um método de aproximação para uma fração definida. Compara-se
        # "dist" com o comprimento total da linha. Dependendo da fração obtida
        # arredonda-se esta fração para os valores definidos de 0.25, 0.5 e
        # 0.75
        fraction = dist / self.line().length()
        if 0.75 < fraction < 1:
            fraction = 0.75
        if 0.5 < fraction < 0.75:
            fraction = 0.5
        if 0.25 < fraction < 0.5:
            fraction = 0.25
        if 0 < fraction < 0.25:
            fraction = 0.25
        # Resta analisar uma possível inconsistência: Se o ponto p1 analisado
        # acima está abaixo ou acima, à esquerda ou à direita, do ponto p2.
        # Se estiver à direita:
        if self.line().p1().x() > self.line().p2().x():
            # A posição final x é x1 - fração_obtida * delta_x. Ou seja, x1
            # será o ponto referência e a posição final x estará a esquerda
            # deste ponto
            posf_x = self.line().p1().x() - fraction * delta_x
        # Se estiver à esquerda:
        else:
            # A posição final x é x1 + fração_obtida * delta_x. Ou seja, x1
            # será o ponto referência e a posição final x estará à direita
            # deste ponto.
            posf_x = self.line().p1().x() + fraction * delta_x
        # O mesmo é feito para y, sabendo que nos módulos do PySide, o eixo y
        # incrementa seu valor quando é percorrido para BAIXO. Assim:
        # Se estiver ABAIXO:
        if self.line().p1().y() > self.line().p2().y():
            # A posição final y é y1 - fração_obtida * delta_y. Ou seja, y1
            # será o ponto referência e a posição final y estará ACIMA deste
            # ponto.
            posf_y = self.line().p1().y() - fraction * delta_y
        # Se estiver ACIMA:
        else:
            # A posição final y é y1 + fração_obtida * delta_y. Ou seja, y1
            # será o ponto de referência e a posição final y estará ABAIXO
            # deste ponto.
            posf_y = self.line().p1().y() + fraction * delta_y
        # Finalmente, define e retorna a posição final. Explicando: Se
        # passarmos uma posição que esteja entre o começo e a metade da linha,
        # a função retornará a posição que está exatamente em 0.25 da linha.
        # Caso passemos uma posição que esteja no terceiro quarto da linha,
        # a função retornará a posição que esteja exatamente na metade da
        # linha. Passando uma posição que esteja no último quarto da linha, a
        # função retornará a posição que esteja exatamente em 0.75 da linha.
        posf = QtCore.QPointF(posf_x, posf_y)

        return posf

    def update_position(self):
        '''
            Método de atualização da posição do objeto edge implementado pela
            classe Edge. Sempre que um dos objetos Nodes w1 ou w2 modifica sua
            posição este método é chamado para que o objeto edge possa
            acompanhar o movimento dos Objetos Node.
        '''
        # Simplesmente cria uma nova linha ligando os itens w1 e w2.
        line = QtCore.QLineF(self.w1.pos(), self.w2.pos())
        length = line.length()
        # Se o comprimento obtido for nulo, retorna a função e a linha não
        # será atualizada
        if length == 0.0:
            return
        # Esta função virtual é necessária para realizar mudanças de geometria
        # em tempo real nos objetos da biblioteca PySide.
        self.prepareGeometryChange()
        # Seta a linha obtida como linha da Edge.
        self.setLine(line)

    def set_color(self, color):
        '''
            Metodo que seta a cor do objeto Edge como a definida pelo parametro
            color.
        '''
        self.setPen(QtGui.QPen(color))


    def paint(self, painter, option, widget):
        '''
            Metodo de desenho do objeto edge implementado pela classe Edge.
            A classe executa esta função constantemente.
        '''
        # Se os itens colidirem graficamente, a linha não é desenhada.
        if (self.w1.collidesWithItem(self.w2)):
            return

        # Temos abaixo a lógica de distribuição de linhas quando elas são
        # conectadas a uma barra.

        # Se o item self.w1 for do tipo barra deve-se alinhar o item self.w2.
        # Note que este alinhamento não se aplica ao elemento Subestação:
        if (self.w1.myItemType == Node.Barra
                and self.w2.myItemType != Node.Subestacao):
            # Seta a flag indicando fixação da linha na Barra.
            self.fixFlag = True
            # Seta flag de w2, indicando que este item está fixo na barra.
            self.w2.Fixed = True
            # Se o número de linhas conectas a barra for maior que 1 deve-se
            # proceder a lógica de distribuição e alinhamento.
            if len(self.w1.edges) > 1:
                # Insere a linha em seu local de distribuição calculado pelo
                # item gráfico barra. Este local é determinado pela função
                # edge_position (Ver classe Node).
                line = QtCore.QLineF(self.mapFromItem(
                    self.w1, self.w1.rect().center().x(),
                    self.w1.edge_position(
                        self)), self.mapFromItem(
                    self.w2, self.w2.rect().center()))
                # Ajusta o item w2 na grade invisível presente no diagrama.
                # (Ver classe Node, função "adjust_in_grid")
                pos = self.w2.adjust_in_grid(
                    QtCore.QPointF(self.w2.scenePos().x(), line.y1()))
                self.w2.setPos(pos)

                # Ajusta a linha final de acordo com o local de distribuição
                # com a correção do ajuste na grade.
                line.setLine(line.x1(), self.w2.y() + 10, line.x2(), line.y2())
                # Fixa o item w2.

                self.w2.fix_item()
            # Se esta é a primeira ligação da linha, realiza-se uma ligação
            # normal.
            else:
                line = QtCore.QLineF(self.mapFromItem(
                    self.w1, self.w1.rect().center()), self.mapFromItem(
                    self.w2, self.w2.rect().center()))

        # Se o item self.w2 for do tipo barra deve-se alinhar o item self.w1.
        # O procedimento é análogo ao exposto acima.
        elif (self.w2.myItemType == Node.Barra
                and self.w1.myItemType != Node.Subestacao):
            self.fixFlag = True
            self.w1.Fixed = True
            if len(self.w2.edges) > 1:
                line = QtCore.QLineF(self.mapFromItem(
                    self.w1, self.w1.rect().center()), self.mapFromItem(
                    self.w2, self.w2.rect().center().x(),
                    self.w2.edge_position(
                        self)))
                self.w1.setY(self.mapFromItem(
                    self.w2, self.w2.rect().center().x(),
                    self.w2.edge_position(
                        self)).y() - 12.5)
                self.w1.fix_item()
            else:
                line = QtCore.QLineF(self.mapFromItem(
                    self.w1, self.w1.rect().center()), self.mapFromItem(
                    self.w2, self.w2.rect().center()))
        else:
            line = QtCore.QLineF(self.mapFromItem(
                self.w1, self.w1.rect().center()), self.mapFromItem(
                self.w2, self.w2.rect().center()))
        self.setLine(line)
        if self.fixFlag:
            self.isFixed = True

        # Define a caneta e o preenchimento da linha.

        painter.setPen(QtGui.QPen(QtCore.Qt.black,  # QPen Brush
                                                    2,  # QPen width
                                                    QtCore.Qt.SolidLine,
                                                    # QPen style
                                                    QtCore.Qt.SquareCap,
                                                    # QPen cap style
                                                    QtCore.Qt.RoundJoin)
                       # QPen join style
                       )
        painter.setBrush(QtCore.Qt.black)
        painter.drawLine(self.line())

        # Se a linha for selecionado, desenha uma linha tracejada ao redor
        # da linha selecionada.
        if self.isSelected():
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
            my_line = QtCore.QLineF(line)
            my_line.translate(0, 4.0)
            painter.drawLine(my_line)
            my_line.translate(0, -8.0)
            painter.drawLine(my_line)

    def mousePressEvent(self, mouse_event):
        '''
            Metodo do evento de pressionar o mouse (mousePressEvent)
            implementado pela classe Edge
        '''

        self.setSelected(True)
        super(Edge, self).mousePressEvent(mouse_event)
        return

    def contextMenuEvent(self, event):
        '''
            Callback chamada... ***continuar***
        '''
        self.scene().clearSelection()
        self.setSelected(True)
        self.myEdgeMenu.exec_(event.screenPos() + QtCore.QPointF(20, 20))


class Text(QtGui.QGraphicsTextItem):
    '''
        Classe que implementa o objeto Text Genérico
    '''

    # Cria dois sinais, um relacionado à mudança de posição/geometria do item
    # e outro a quando o item perde o foco, ou deixa de estar selecionado.
    # (ver PySide, QtCore.Signal)
    selectedChange = QtCore.Signal(QtGui.QGraphicsItem)
    lostFocus = QtCore.Signal(QtGui.QGraphicsTextItem)

    def __init__(self, text, parent=None, scene=None):
        '''
            Configurações do texto (ver PySide, QtGui.QGraphicsTextItem)
        '''
        super(Text, self).__init__(parent, scene)
        self.setPlainText(text)
        self.setZValue(100)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)

    def itemChange(self, change, value):
        '''
            Função virtual reimplementada para emitir sinal de mudança (ver
            Pyside, QGraphicsTextItem)
        '''
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            self.selectedChange.emit(self)
        return value

    def focusOutEvent(self, event):
        '''
            Função virtual reimplementada para emitir sinal de perda de foco
            (ver Pyside, QGraphicsTextItem)
        '''
        self.lostFocus.emit(self)
        super(Text, self).focusOutEvent(event)


class Node(QtGui.QGraphicsRectItem):
    '''
       Classe que implementa o objeto Node Genérico. Este elemento gráfico irá
       representar religadores, barras, subestações e nós de carga
    '''
    # tipos de itens possiveis
    Subestacao, Religador, Barra, Agent, NoDeCarga, NoConectivo = range(6)

    def __init__(self, item_type, node_menu, parent=None, scene=None):
        '''
            Método inicial da classe Node
            Recebe como parâmetros os objetos myItemType (que define o tipo de
            Node desejado) e o menu desejado (menu que abre com clique direito)
            Analogamente ao que acontece com a Edge, este item é apenas a
            representação de um retângulo do tipo QtCore.QRectF.
        '''
        super(Node, self).__init__()
        # Definição de atributos do tipo flag:
        self.bar_busy = False           # flag - barra ocupada.
        self.Fixed = False              # flag - item fixado a uma barra.
        # Definição de diversos atributos que serão usados posteriormente.
        self.id = id(self)              # Atributo que guarda id única do item.
        self.edges = {}                 # Dicionário contendo edges do item.
        self.l0 = None                  # Variável auxiliar de posição.
        self.edges_no_sub = {}          # Falta perguntar ao lucas.
        self.myItemType = item_type     # Define o tipo de item.
        self.edge_counter = 0           # Contador que acompanha o nº de edges.
        self.mean_pos = None            # Atributo de posição média.
        self.text_config = 'Custom'     # Atributo da configuração de relé.
        self.pos_ref = 0                # Atributo de posição referência.
        # Se o item a ser inserido for do tipo subestação:
        if self.myItemType == self.Subestacao:
            # Define o retângulo.
            rect = QtCore.QRectF(0, 0, 50.0, 50.0)
            # Define e ajusta a posição do label do item gráfico. Começa com
            # um texto vazio.
            self.text = Text('', self, self.scene())
            self.substation = Substation(
                self.text.toPlainText(), 0.0, 0.0, 0.0, complex(0, 0))
            self.text.setPos(self.mapFromItem(self.text, 0, rect.height()))
        # Se o item a ser inserido for do tipo religador:
        elif self.myItemType == self.Religador:
            rect = QtCore.QRectF(0, 0, 20, 20)
            # Define e ajusta a posição do label do item gráfico. Começa com
            # um texto vazio.
            self.text = Text('', self, self.scene())
            self.text.setPos(self.mapFromItem(self.text, 10, rect.height()))
            # Cria o objeto chave que contém os dados elétricos do elemento
            # religador.
            self.chave = Religador(self.text.toPlainText(), 0, 0, 0, 0, 1)
        # Se o item a ser inserido for do tipo barra:
        elif self.myItemType == self.Barra:
            rect = QtCore.QRectF(0, 0, 10.0, 100.0)
            # Define e ajusta a posição do label do item gráfico. Começa com
            # um texto vazio.
            self.text = Text('Barra', self, self.scene())
            self.text.setPos(self.mapFromItem(self.text, 0, rect.height()))
            # Cria o objeto barra que contém os dados elétricos do elemento
            # barra.
            self.barra = BusBarSection("Identificador")
            # Define uma lista vazia com os terminais que possivelmente a barra
            # terá
            self.terminals = []
        # Se o item a ser inserido for do tipo agente:
        # OBS: PERGUNTAR PRO LUCAS SE O ABAIXO É NECESSÁRIO
        elif self.myItemType == self.Agent:
            rect = QtCore.QRectF(0, 0, 50.0, 50.0)
            # Define e ajusta a posição do label do item gráfico. Começa com
            # o texto Agente.
            self.text = Text('Agente', self, self.scene())
            self.text.setPos(self.mapFromItem(self.text, 0, rect.height()))

        # OBS: PERGUNTAR SE AINDA É NECESSÁRIO A PRESENÇA DE UM NÓ CONECTIVO
        # Se o item a ser inserido for do tipo nó conectivo:
        elif self.myItemType == self.NoConectivo:
            rect = QtCore.QRectF(0, 0, 7, 7)

        # Se o item a ser inserido for do tipo nó de carga:
        elif self.myItemType == self.NoDeCarga:
            rect = QtCore.QRectF(0, 0, 8, 8)
            # Define e ajusta a posição do label do item gráfico. Começa com
            # um texto vazio.
            self.text = Text('', self, self.scene())
            self.text.setPos(self.mapFromItem(self.text, 0, rect.height()))
            # Define uma lista vazia com os terminais que possivelmente o nó
            # de carga terá
            self.terminals = []
            # Cria o objeto barra que contém os dados elétricos do elemento
            # barra.
            self.no_de_carga = EnergyConsumer('', 0, 0)
        # Estabelece o retângulo do item gráfico como o rect obtido, dependendo
        # do item.
        self.setRect(rect)
        # Estabelece o menu (aberto via clique direito) dependendo do tipo de
        # item.
        self.myNodeMenu = node_menu

        # Seta as flags do QGraphicsItem (ver QtGui.QGraphicsItem.setFlag)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setZValue(0)

    def fix_item(self):
        '''
            Seta a flag de fixação do item.
        '''
        self.Fixed = True

    def update_count(self):
        '''
            Atualiza o contador que acompanha o número de Edges do item.
        '''
        self.edge_counter = len(self.edges)

    def remove_edges(self):
        '''
            Método de remoção de todos objetos Edge associados ao objeto node.
        '''
        # Cria uma lista vazia que irá receber as Edges removidas.
        deleted_list = []
        # Varre as edges do Node.
        for edge in self.edges:
            # Como todas as edges serão removidas, adiciona cada uma à
            # "deleted_list".
            deleted_list.append(edge)
            # Remove a Edge da cena em que o Node se encontra.
            self.scene().removeItem(edge)

        for edge in deleted_list:
            # Como cada edge removida possui um outro item conectado além do
            # Node presente, precisamos removê-la também da lista de edges.
            # deste outro item.
            if edge.w1 is not None:
                edge.w1.remove_edge(edge)
            if edge.w2 is not None:
                edge.w2.remove_edge(edge)

        # Limpa a lista de edges do presente Node, assim como a lista de edges
        # que não são conectadas à subestações.
        self.edges.clear()
        self.edges_no_sub.clear()
        # Atualiza o contador que acompanha o número de edges associadas ao
        # item.
        self.update_count()

    def remove_edge(self, edge):
        '''
            Esta função remove a edge passada na chamada do item presente.
        '''
        self.edges.pop(edge)
        self.update_count()

    def add_edge(self, edge):
        '''
            Método de adição de objetos edge associados ao objeto node
        '''
        # Se o Node for um religador, este só pode ter no máximo 2 ligações.
        # Ou seja, se o contador que acompanha o número de edges do Node for
        # maior que 2, a função retorna.
        if self.myItemType == self.Religador:
            if self.edge_counter > 2:
                return
        # Incrementa o contador.
            self.edge_counter += 1
        # Adiciona a Edge passada na chamada da função para o dicionário de
        # Edges do Node.
        self.edges[edge] = len(self.edges)
        # Se o presente Node não for uma subestação, adiciona a Edge no
        # dicionário de edges que não se conectam a subestações.
        if (edge.w1.myItemType != Node.Subestacao
                and edge.w2.myItemType != Node.Subestacao):
            self.edges_no_sub[edge] = len(self.edges_no_sub)
        self.update_count()

    def edge_position(self, edge):
        '''
            Este método é utilizado da distribuição das Edges ligadas numa
            barra, seguindo uma lógica de alinhamento.
        '''
        # PEDIR PARA O LUCAS EXPLICAR
        height = self.rect().height()
        height = height - 2.0 * height / 8.0

        num_edges = len(self.edges_no_sub)

        num_edges -= 1

        if num_edges <= 0:
            num_edges = 1

        dw = height / float(num_edges)

        pos = height / 8.0 + self.edges_no_sub[edge] * dw

        return pos

    def center(self):
        '''
            Método que retorna o centro do objeto passado.
        '''
        point = QtCore.QPointF(self.rect().width(), self.rect().height())
        return (self.pos() + point / 2)

    def set_center(self, pos):
        w = self.rect().width()
        h = self.rect().height()
        point = QtCore.QPointF(w / 2, h / 2)
        self.setPos(pos - point)

    def boundingRect(self):
        '''
            Reimplementação da função virtual que especifica a borda do objeto
            node (ver biblioteca Pyside, QtGui.QGraphicsRectItem.boundingRect)
        '''
        extra = 5.0
        return self.rect().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        '''
            Método de desenho do objeto node implementado pela classe Node.
            Aqui se diferencia os objetos pela sua forma. Todos eram definidos
            por um retângulo QtCore.QRectF. Neste método, serão desenhadas
            suas formas baseadas em seus retângulos.
            Ver método paint em PySide.
        '''
        # Caso o item a ser inserido seja do tipo subestacão:
        if self.myItemType == self.Subestacao:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            painter.setBrush(QtCore.Qt.white)
            painter.drawEllipse(self.rect())
        # Caso o item a ser inserido seja do tipo religador:
        elif self.myItemType == self.Religador:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            # Faz-se aqui importante observação: se a chave associada ao
            # elemento gráfico religador estiver fechada, desenha-se o
            # religador preenchido de preto. Caso contrário, ele é vazado
            # (branco)
            if self.chave.normalOpen == 1:
                painter.setBrush(QtCore.Qt.white)
            else:
                painter.setBrush(QtCore.Qt.black)
            painter.drawRoundedRect(self.rect(), 5, 5)
        # Caso o item a ser inserido seja do tipo barra:
        elif self.myItemType == self.Barra:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            painter.setBrush(QtCore.Qt.black)
            painter.drawRoundedRect(self.rect(), 2, 2)
        # Caso o item a ser inserido seja do tipo agente:
        elif self.myItemType == self.Agent:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            painter.setBrush(QtCore.Qt.white)
            painter.drawRect(self.rect())
        # Caso o item a ser inserido seja do tipo nó conectivo:
        elif self.myItemType == self.NoConectivo:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            painter.setBrush(QtCore.Qt.black)
            painter.drawEllipse(self.rect())

        # Caso o item a ser inserido seja do tipo nó de carga:
        elif self.myItemType == self.NoDeCarga:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
            painter.setBrush(QtCore.Qt.black)
            painter.drawRect(self.rect())

        # Se o item estiver selecionado, desenha uma caixa pontilhada de
        # seleção em seu redor.
        if self.isSelected():
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
            painter.setBrush(QtCore.Qt.NoBrush)
            adjust = 2
            rect = self.rect().adjusted(-adjust, -adjust, adjust, adjust)
            painter.drawRect(rect)

    def itemChange(self, change, value):
        '''
            Método que detecta mudancas na posição do objeto Node
        '''
        # Se a mudança for posição (ver QtGui.QGraphicsItem.ItemPositionChange)
        # é preciso atualizar as edges deste Node uma a uma:
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            for edge in self.edges:
                edge.update_position()
        # Condição interna de retorno necessária.
        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def mousePressEvent(self, mouse_event):
        '''
            Reimplementação da função virtual que define o evento referente
            ao aperto de botão do mouse.
        '''
        # Armazena a cena do item
        self.cena = self.scene()
        # "Deseleciona" os outros itens que por ventura estejam selecionados.
        self.scene().clearSelection()
        # Aciona a flag interna do item que indica que o item está selecionado.
        self.setSelected(True)
        super(Node, self).mousePressEvent(mouse_event)
        return

    def mouseMoveEvent(self, mouse_event):
        '''
            Reimplementação da função virtual que define o evento referente
            ao movimento do mouse durante o aperto.
        '''
        super(Node, self).mouseMoveEvent(mouse_event)
        # Chama a função "adjust_in_grid", que limita o movimento dos itens
        # numa grade invisível presente no diagrama (ver adjust_in_grid na
        # class node).
        self.setPos(self.adjust_in_grid(self.scenePos()))

    def mouseReleaseEvent(self, mouse_event):
        '''
            Reimplementação da função virtual que define o evento referente
            ao soltar do botão mouse após aperto.
        '''
        super(Node, self).mouseReleaseEvent(mouse_event)
        # Cria uma edge None para auxílio na execução.
        new_edge = None
        scene = self.scene()
        # Cria um elemento gráfico do tipo elipse, com tamanho definido pelo
        # retângulo QtCore.QRectF. Este elipse é adicionado na posição em que o
        # botão foi solto. Este elipse precisa ser removido ao final da função,
        # caso contrário ele ficará visível na cena.
        ell = QtGui.QGraphicsEllipseItem()
        ell.setRect(
            QtCore.QRectF(
                mouse_event.scenePos() - QtCore.QPointF(10, 10),
                QtCore.QSizeF(30, 30)))
        scene.addItem(ell)

        # O trecho a seguir implementa o caráter "Sticky" do nó conectivo.
        # Explicando: Se o nó só tiver uma extremidade ocupada e colidir com
        # um node que não seja outro nó conectivo, a linha "gruda" no item
        # colidido, estabelecendo uma ligação.
        if self.myItemType == Node.NoConectivo and len(self.edges) == 1:
            # Varre todos os itens que foram colididos com o elipse criado.
            # Isto permite que haja uma margem de colisão ao redor do nó.
            for item in scene.items():
                if ell.collidesWithItem(item):
                    if isinstance(item, Node):
                        if item.myItemType != Node.NoConectivo:
                            # Se o item for uma barra, ainda é preciso tratar
                            # o algoritmo! PENDÊNCIA.
                            if item.myItemType == Node.Barra:
                                scene.removeItem(ell)
                                return
                            # Não sendo o item uma barra, remove-se a linha
                            # do nó conectivo, e cria uma nova linha se liga
                            # diretamente ao item colidido.
                            for edge in self.edges:
                                edge.scene().removeItem(edge)
                                if edge.w1.myItemType != Node.NoConectivo:
                                    w1 = edge.w1
                                else:
                                    w1 = edge.w2
                                new_edge = Edge(w1, item, scene.myLineMenu)
                                scene.addItem(new_edge)
                                new_edge.update_position()
                                scene.removeItem(self)
        # Caso o item seja um Nó de Carga e não esteja conectado ainda, este
        # trecho do método implementa a característica "Sticky" do Nó de Carga
        # quando ele colide com uma linha.
        if self.myItemType == Node.NoDeCarga:
            # Se o Nó de Carga já estiver conectado, a função retorna.
            if len(self.edges) != 0:
                scene.removeItem(ell)
                return
            scene.removeItem(ell)
            if self.scene().myMode == 1:
                return
                # Se algum item da cena colidir com o elipse e este item não
                # for o próprio nó de carga, quebra a linha e adiciona o nó
                # de carga. Se o comprimento da linha for muito pequeno, isto
                # não é feito.
            for item in scene.items():
                if ell.collidesWithItem(item):
                    if isinstance(item, Edge) and not item.isUnderMouse():
                        if item.line().length() < 20:
                            return
                        break_mode = 3
                        pos = item.get_fraction(mouse_event.scenePos())
                        self.setPos(pos.x() - 5, pos.y() - 5)
                        scene.break_edge(item, break_mode, None, self)

        scene.removeItem(ell)
        return

    def mouseDoubleClickEvent(self, event):
        '''
            Reimplementação da função de duplo clique do mouse.
        '''
        # Limpa a seleção de qualquer objeto na cena.
        self.scene().clearSelection()
        # Seta o item como selecionado.
        self.setSelected(True)
        super(Node, self).mouseDoubleClickEvent(event)
        # Executa o Dialog de configuração dos elementos do Node.
        self.scene().launch_dialog()

    def adjust_in_grid(self, pos):
        '''
            Este método implementa uma grade invisível na cena, que limita o
            movimento dos Nodes para posições bem definidas.
        '''
        # Ajuste de posição empírico
        item_x = pos.x() - 5
        item_y = pos.y() - 5
        if item_x == 0 or item_y == 0:
            return
        # Isola a centena da posição x e y do item, e.g se a posição x for
        # 384, centena_x = int(384/100) * 100 = 3 * 100. Todo o exemplo é aná-
        # logo para a posição y.
        centena_x = int(item_x / 100) * 100
        centena_y = int(item_y / 100) * 100
        # Calcula os residuais, que é a dezena+unidade. No nosso exemplo,
        # residual_x = 384 - 300 = 84
        residual_x = item_x - centena_x
        residual_y = item_y - centena_y
        # A posição de referência para a grade é a 0,0. Assim, definiu-se que
        # cada quadrado da grade possui 20x20 pixels. Sendo assim, o residual
        # calculado irá nos mostrar em que quadrado o item precisa ser
        # ajustado. No nosso exemplo, temos x = 384. Então a posição x deve
        # ser ajustada para 380, que se encontra no quadrado que compreende
        # 380 -> 400. Segue-se a seguinte regra:
        #  0 < residual < 10  -> Posição final = centena
        # 10 < residual < 20  -> Posição final = centena + 20
        # 20 < residual < 30  -> Posição final = centena + 20
        # 30 < residual < 40  -> Posição final = centena + 40
        # 40 < residual < 50  -> Posição final = centena + 40
        # 50 < residual < 60  -> Posição final = centena + 60
        # 60 < residual < 70  -> Posição final = centena + 60
        # 70 < residual < 80  -> Posição final = centena + 80
        # 80 < residual < 90  -> Posição final = centena + 80
        #      residual > 90  -> Posição final = centena + 100

        if residual_x > 10:
            if residual_x > 20:
                if residual_x > 30:
                    new_pos_x = centena_x + 40
                else:
                    new_pos_x = centena_x + 20
            else:
                new_pos_x = centena_x + 20
        else:
            new_pos_x = centena_x

        if residual_x > 40:
            if residual_x > 50:
                new_pos_x = centena_x + 60
            else:
                new_pos_x = centena_x + 40
        if residual_x > 60:
            if residual_x > 70:
                new_pos_x = centena_x + 80
            else:
                new_pos_x = centena_x + 60
        if residual_x > 80:
            if residual_x > 90:
                new_pos_x = centena_x + 100
            else:
                new_pos_x = centena_x + 80

        if residual_y > 10:
            if residual_y > 20:
                if residual_y > 30:
                    new_pos_y = centena_y + 40
                else:
                    new_pos_y = centena_y + 20
            else:
                new_pos_y = centena_y + 20
        else:
            new_pos_y = centena_y

        if residual_y > 40:
            if residual_y > 50:
                new_pos_y = centena_y + 60
            else:
                new_pos_y = centena_y + 40
        if residual_y > 60:
            if residual_y > 70:
                new_pos_y = centena_y + 80
            else:
                new_pos_y = centena_y + 60
        if residual_y > 80:
            if residual_y > 90:
                new_pos_y = centena_y + 100
            else:
                new_pos_y = centena_y + 80
        # Ajuste de posição devido à diferença de geometria.
        if self.myItemType == Node.NoDeCarga:
            new_pos_x += 6
            new_pos_y += 6
        return QtCore.QPointF(new_pos_x, new_pos_y)

    def contextMenuEvent(self, event):
        '''
            Método que reimplementa a função virtual do menu aberto pelo clique
            com botão direito.
        '''
        # Limpa a seleção dos itens da cena.
        self.scene().clearSelection()
        # Seta a flag do item como selecionado.
        self.setSelected(True)
        # Executa o menu, dependendo do tipo de item.
        self.myNodeMenu.exec_(event.screenPos())


class SceneWidget(QtGui.QGraphicsScene):
    '''
        Classe que implementa o container Gráfico onde os
        widgets residirão, denominado cena.
    '''

    # Tipos de modos de interacao com o diagrama grafico
    InsertItem, InsertLine, InsertText, MoveItem, SelectItems = range(5)

    # Tipos de estilos para o background do diagrama grafico
    GridStyle, NoStyle = range(2)
    # Signal definido para a classe SceneWidget enviado quando um item é
    # inserido no diagrama grafico
    itemInserted = QtCore.Signal(int)

    def __init__(self, window):

        super(SceneWidget, self).__init__()
        # Definição de flags
        self.main_window = window
        self.start_item_is_ghost = False
        self.end_item_is_ghost = False
        self.keyControlIsPressed = False
        # Definição de atributos auxiliares
        self.line = None
        self.no = None
        self.selectRect = None
        self.text_item = None
        self.dict_prop = {}
        self.lista_no_conectivo = []
        # Definição da geometria inicial da cena
        self.setSceneRect(0, 0, 800, 800)
        self.myMode = self.MoveItem
        self.myItemType = Node.Subestacao
        self.my_background_style = self.NoStyle
        # Execuções de métodos iniciais
        # Cria as ações que podem ser realizadas na cena (ver create_actions
        # em SceneWidget)
        self.create_actions()
        # Cria os menus que serão utilizados na cena (ver create_menus em
        # SceneWidget)
        self.create_menus()
        # Cria a pilha de comandos UNDO para implementação dos comandos
        # desfazer e refazer (CTRL+Z e CTRL+Y). PENDÊNCIA.
        self.undoStack = QtGui.QUndoStack()
        # Cria os dicionários de padrões dos relés (ver create_dict_recloser em
        # SceneWidget
        self.custom_dict = {'Corrente Nominal': 0,
                            'Capacidade de Interrupcao': 0, 'Sequencia': 0}
        self.create_dict_recloser(100, 4, 4, 'ABB')
        self.create_dict_recloser(150, 5, 3, 'SEL')
        self.create_dict_recloser(200, 6, 3, 'BOSCH')
        print "CENA CRIADA"

    def create_dict_recloser(self, corrente, capacidade, num_rel, padrao):
        '''
            Este método cria um dicionário de um padrão de religador comercial,
            de acordo com os parâmetros passados.
        '''
        prop = {'Corrente Nominal': corrente,
                'Capacidade de Interrupcao': capacidade, 'Sequencia': num_rel}
        self.dict_prop[padrao] = prop

    def mousePressEvent(self, mouse_event):
        '''
            Este método define as ações realizadas quando um evento do tipo
            mousePress é detectado no diagrama grafico
        '''
        super(SceneWidget, self).mousePressEvent(mouse_event)
        # Armazena em um atributo a posição em que o mouse foi apertado.
        self.pressPos = mouse_event.scenePos()
        # Define o break_mode, utilizado no método de quebrar linhas (ver
        # break_edge em SceneWidget.
        self.break_mode = 2
        # Cria uma variável para receber uma edge que foi quebrada.
        self.edge_broken = None
        # Define as ações para quando o botão apertado do mouse NÃO for o
        # esquerdo.
        if (mouse_event.button() != QtCore.Qt.LeftButton):
            # Variável auxiliar que indica se o nó tem prioridade.
            node_priority = False
            # Limpa seleção de itens na cena.
            self.clearSelection()
            # Cria um elipse que será adicionado e retirado da cena no término
            # da função, de forma que nunca será visível ao usuário. O elipse
            # é inserido na posição de press do mouse.
            # O elipse dá precisão ao clique do usuário. Toda ação será inter-
            # pretada com uma margem de seleção ao redor, representada pelo
            # elipse.
            ell = QtGui.QGraphicsEllipseItem()
            ell.setRect(
                QtCore.QRectF(
                    mouse_event.scenePos()
                    - QtCore.QPointF(10, 10), QtCore.QSizeF(30, 30)))
            self.addItem(ell)
            # Testa todos os itens da cena.
            for item in self.items():
                # Se o elipse de precisão colidir com a cena e este for um
                # Node, seta-se prioridade para o mesmo.
                if ell.collidesWithItem(item):
                    if isinstance(item, Node):
                        node_priority = True

            # Testa novamente todos os itens da cena.
            for item in self.items():
                # Se o elipse colidir com uma edge e não houver prioridade de
                # nó, abre-se o menu de opções (context) da Edge
                if (ell.collidesWithItem(item) and isinstance(item, Edge)
                        and not node_priority):
                    self.removeItem(ell)
                    item.setSelected(True)
                    item.myEdgeMenu.exec_(mouse_event.screenPos())
                    item.setSelected(False)
                    return
            # Caso não haja linhas colidindo, remove o elipse e retorna.
            self.removeItem(ell)
            return
        # Cria uma variável para receber item oculto e removê-lo, caso exista.
        item_oculto = None
        for item in self.items():
            if not item.isVisible():
                item_oculto = item
        if item_oculto is None:
            pass
        else:
            self.removeItem(item_oculto)

        # Caso o botão pressionado do mouse for o esquerdo:
        # Entra no modo passado à cena.
        # Se o modo for de inserção de itens:
        if self.myMode == self.InsertItem:
            # Insere o item com determinado tipo (ver Node).
            if self.myItemType == Node.Religador:
                item = Node(self.myItemType, self.myRecloserMenu)
            elif self.myItemType == Node.Barra:
                item = Node(self.myItemType, self.myBusMenu)
            elif self.myItemType == Node.Subestacao:
                item = Node(self.myItemType, self.mySubstationMenu)
            elif self.myItemType == Node.NoDeCarga:
                item = Node(self.myItemType, self.mySubstationMenu)
            # Ajusta a posição do item para a posição do press do mouse.
            item.setPos(item.adjust_in_grid(mouse_event.scenePos()))
            self.addItem(item)

            # Quando um item é adicionado, o dialog de configuração se abre
            # para que o usuário prontamente insira seus dados (ver
            # launch_dialog). Caso o usuário cancele a janela, o item é
            # removido da cena.
            if self.myItemType == Node.Religador:
                item.setSelected(True)
                result = self.launch_dialog()
                item.setSelected(False)
                if result == 0:
                    self.removeItem(item)

            elif self.myItemType == Node.Barra:
                item.setSelected(True)
                result = self.launch_dialog()
                item.setSelected(False)
                if result == 0:
                    self.removeItem(item)
            elif self.myItemType == Node.Subestacao:
                item.setSelected(True)
                result = self.launch_dialog()
                item.setSelected(False)
                if result == 0:
                    self.removeItem(item)

            elif self.myItemType == Node.NoDeCarga:
                item.setSelected(True)
                result = self.launch_dialog()
                item.setSelected(False)
                if result == 0:
                    self.removeItem(item)
            # Cria um comando para que seja possibilitada a ação de desfazer/
            # refazer. PENDÊNCIA
            comando = AddRemoveCommand("Add", self, item)
            self.undoStack.push(comando)
            # Emite um sinal contendo o tipo do item.
            self.itemInserted.emit(self.myItemType)

        # Caso o modo passado à cena seja de inserção de linha:
        elif self.myMode == self.InsertLine:
            # Cria o elipse para o mesmo fim explicado anteriormente: dar
            # margem de ação para os "presses" do mouse
            ell = QtGui.QGraphicsEllipseItem()
            ell.setRect(
                QtCore.QRectF(
                    mouse_event.scenePos()
                    - QtCore.QPointF(10, 10), QtCore.QSizeF(30, 30)))
            self.addItem(ell)
            # Seta a prioridade de Node como falsa
            node_priority = False
            # Aqui se cria uma legenda para os tipos de colisão possível.
            edge_collision, node_collision, ellipse_collision = range(3)
            # Cria-se uma variável para receber o tipo de colisão
            collision = None
            # Varre os itens que estejam na posição apertada pelo mouse.
            # Se o item for do tipo Node, seta prioridade para o mesmo.
            for item in self.items(mouse_event.scenePos()):
                if isinstance(item, Node):
                    node_priority = True
            # Varre todos os itens da cena que colidem com o elipse de
            # precisão:
            for item in self.items():
                if ell.collidesWithItem(item):
                    # 1) Se este item for do tipo Edge e a prioridade de Node
                    # estiver desligada, seta a colisão como colisão de Edge.
                    # Ou seja, o usuário está inserindo uma linha em cima de
                    # outra linha, o que provoca uma quebra na linha original
                    # (criar derivações)
                    # IMPORTANTE: O break_mode associado com esta operação é 0.
                    # A Edge que será quebrada também é armazenada.
                    if isinstance(item, Edge) and not node_priority:

                        self.c_pos = (
                            item.line().p1() + item.line().p2()) / 2
                        collision = edge_collision
                        self.break_mode = 0
                        self.edge_broken = item
                    # 2) Se este item for do tipo Node, atribui-se este como o
                    # Node de origem de uma nova linha. Seta a colisão como
                    # colisão de Node.
                    elif isinstance(item, Node):
                        collision = node_collision
                        self.start_item = item
                    # 3) Se este item for outro elipse, seta a colisão como
                    # colisão de elipse.
                    elif isinstance(item, QtGui.QGraphicsEllipseItem):
                        collision = ellipse_collision
            # Define uma posição inicial como sendo a posição de press do
            # mouse.
            self.l0 = mouse_event.scenePos()
            # Realiza o teste do tipo da colisão.
            # 1) Colisão de edge: Existe necessidade de quebra de linha e da
            # inserção dum nó conectivo para realizar a derivação. c_pos é a
            # posição obtida anteriormente para o ponto médio da linha a ser
            # quebrada. O start_item se torna o nó conectivo inserido.
            if collision == edge_collision:
                self.no = Node(Node.NoConectivo, self.myLineMenu)
                self.addItem(self.no)
                self.no.setPos(self.c_pos - QtCore.QPointF(3.5, 3.5))
                self.start_item = self.no
                self.l0 = self.c_pos
            # Se a colisão for com outro elipse, significa que o usuário inse-
            # riu a linha num espaço livre da cena. Por ora, o programa adicio-
            # nará um nó conectivo, que será removido futuramente se a ligação
            # não se concretizar (ver mouseReleaseEvent de SceneWidget).
            elif collision == ellipse_collision:
                self.no = Node(Node.NoConectivo, self.myLineMenu)
                self.addItem(self.no)
                self.no.setPos(mouse_event.scenePos())
                self.start_item = self.no
            # Terminados os testes, cria uma linha que está pronta para ser
            # criada e atualizada à medida que o usuário move o mouse após o
            # press.
            self.line = QtGui.QGraphicsLineItem(
                QtCore.QLineF(
                    self.l0,
                    self.l0))
            self.line.setPen(
                QtGui.QPen(QtCore.Qt.black, 2))
            self.addItem(self.line)
            self.removeItem(ell)

        # Se o modo de inserção for de texto, insere o texto com base na
        # posição do mouse.
        elif self.myMode == self.InsertText:
            text_item = Text()
            text_item.setFont(self.myFont)
            text_item.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            text_item.setZValue(1000.0)
            text_item.lostFocus.connect(self.editorLostFocus)
            text_item.selectedChange.connect(self.itemSelected)
            self.addItem(text_item)
            text_item.setDefaultTextColor(self.myTextColor)
            text_item.setPos(mouse_event.scenePos())
            self.textInserted.emit(text_item)
        # Se o modo for de seleção de itens múltiplos:
        elif self.myMode == self.SelectItems:
            selection = True
            if selection:
                init_point = mouse_event.scenePos()
                self.selectRect = QtGui.QGraphicsRectItem(
                    QtCore.QRectF(init_point, init_point))
                self.selectRect.setPen(
                    QtGui.QPen(QtCore.Qt.red, 2, QtCore.Qt.DashLine))
                self.addItem(self.selectRect)
        # Caso não seja nenhum destes modos, estamos no modo simples de
        # seleção.
        else:
            # Desliga as prioridades
            super(SceneWidget, self).mousePressEvent(mouse_event)
            priority_on = False
            priority_node = False
            # Cria o elipse de precisão.
            ell = QtGui.QGraphicsEllipseItem()
            ell.setRect(
                QtCore.QRectF(
                    mouse_event.scenePos()
                    - QtCore.QPointF(10, 10), QtCore.QSizeF(30, 30)))
            self.addItem(ell)
            # Varre itens que colidem com o elipse.
            for item in self.items():
                # Se o item for do tipo Node ou Edge, seta prioridade para
                # estes dois. Se o item for do tipo Node, seta também priori-
                # dade de Node.
                if ell.collidesWithItem(item):
                    if isinstance(item, Node) or isinstance(item, Edge):
                        if isinstance(item, Node):
                            priority_node = True
                        priority_on = True
            # Varre itens que colidem com o elipse.
            for item in self.items():
                if ell.collidesWithItem(item):
                    # Se o item for outro elipse, e não houver prioridade de
                    # Node ou Edge, simplesmente limpa a seleção de objetos da
                    # cena.
                    if (isinstance(item, QtGui.QGraphicsEllipseItem)
                            and not priority_on):
                        self.clearSelection()
                    # Se o item for um Node, o mesmo é selecionado.
                    elif isinstance(item, Node):
                        self.removeItem(ell)
                        self.clearSelection()
                        item.setSelected(True)
                    # Se o item for uma Edge e não houver prioridade de Node,
                    # o mesmo é selecionado.
                    elif isinstance(item, Edge) and not priority_node:
                        self.removeItem(ell)
                        self.clearSelection()
                        item.setSelected(True)
                        return
            if ell.scene() == self:
                self.removeItem(ell)

        return

    def mouseMoveEvent(self, mouse_event):
        '''
            Este método define as ações realizadas quando um evento do tipo
            mouseMove é detectado no diagrama grafico.
        '''
        # Caso estejamos no modo de inserção de linha, desenha a nova linha
        # de acordo com o movimento do mouse
        if self.myMode == self.InsertLine and self.line:
            self.clearSelection()
            new_line = QtCore.QLineF(
                self.line.line().p1(), mouse_event.scenePos())
            self.line.setLine(new_line)
        # Caso estejamos no modo simples de movimentação de item, herda a
        # função nativa do PySide.
        elif self.myMode == self.MoveItem:
            super(SceneWidget, self).mouseMoveEvent(mouse_event)
            return
        # Caso estejamos no modo de seleção de múltiplos itens, desenha o
        # retângulo de seleção
        elif self.myMode == self.SelectItems and self.selectRect:
            new_rect = QtCore.QRectF(
                self.selectRect.rect().topLeft(), mouse_event.scenePos())
            self.selectRect.setRect(new_rect)

    def mouseReleaseEvent(self, mouse_event):
        '''
            Este método define as ações realizadas quando um evento do tipo
            mouseRelease e detectado no diagrama grafico. Neste caso conecta
            os dois elementos que estão ligados pela linha criada no evento
            mousePress.
        '''

        # Se o modo atual for de inserção de linha, desligam-se as prioridades
        # de node e edge e cria uma flag block_on.
        if self.myMode == self.InsertLine and self.line:
            node_priority = False
            edge_priority = False
            block_on = False
            # Remove o item self.no, já que ele foi criado provisoriamente
            # para aparecer durante o aperto do mouse.
            if self.no is not None:
                self.removeItem(self.no)
            # Cria o elipse de precisão localizado onde o mouse foi apertado.
            ell = QtGui.QGraphicsEllipseItem()
            ell.setRect(QtCore.QRectF(mouse_event.scenePos() -
                        QtCore.QPointF(10, 10), QtCore.QSizeF(30, 30)))
            self.addItem(ell)

            # Testes preliminares do start_item
            # Se o start_item for uma barra, seta a flag block_on
            if self.start_item.myItemType == Node.Barra:
                block_on = True
            # Caso seja um religador, verifica se este já possui as duas
            # ligações máximas permitidas. Se sim, remove o elipse de precisão
            # e retorna a função.
            if self.start_item.myItemType == Node.Religador:
                if len(self.start_item.edges) >= 2:
                    self.removeItem(self.line)
                    self.line = None
                    self.removeItem(ell)
                    return

            # Estabelecimento do end_item
            # Se houver um item "debaixo" do mouse e este for um Node, seta a
            # flag de prioridade de Node.
            for item in self.items():
                if item.isUnderMouse():
                    if isinstance(item, Node):
                        node_priority = True

            # Se o elipse de precisão englobar uma linha, seta a flag de
            # prioridade de edge (ou prioridade de linha)
            for item in self.items():
                if ell.collidesWithItem(item):
                    if isinstance(item, Edge):
                        edge_priority = True

            # Testa se o elipse de precisão engloba um Node ou Edge.
            for item in self.items():
                if ell.collidesWithItem(item):
                    # Caso seja um Node, realiza o teste do número de ligações
                    # máximo permitido (2).
                    if isinstance(item, Node):
                        if item.myItemType == Node.Religador:
                            if len(item.edges) >= 2:
                                self.removeItem(self.line)
                                self.line = None
                                self.removeItem(ell)
                                return
                        # Esta condição impede que um item ligado a uma barra
                        # já existente tenha sua condição de alinhamento
                        # alterada pela conexão com outra barra. Em outras
                        # palavras, não será permitido a ligação de uma barra
                        # para um item que já esteja ligado a outra barra.
                        if block_on is True:
                            for edge in item.edges:
                                if (edge.w1.myItemType == Node.Barra
                                        or edge.w2.myItemType == Node.Barra):
                                    self.removeItem(self.line)
                                    self.line = None
                                    self.removeItem(ell)
                                    return
                        # Terminando-se os testes, o end_item é estabelecido
                        # como o Node englobado pelo elipse de precisão.
                        self.end_item = item

                    # Se o elipse engloba uma edge, e não há prioridade de
                    # node, ou seja, não há um node "debaixo" do mouse:
                    elif isinstance(item, Edge) and not node_priority:
                        # Se block_on está setada (ou seja, o start_item é uma
                        # barra), remove a linha, o elipse de precisão e
                        # retorna a função. Em outras palavras, não é possível
                        # realizar a ligação de uma barra para outra linha
                        # (quebra de linha).
                        if block_on is True:
                            self.removeItem(self.line)
                            self.line = None
                            self.removeItem(ell)
                            return
                        # Caso contrário, a situação é de que o item final é
                        # uma linha, ou seja, quebra-se a linha no meio para a
                        # inserção de um nó de passagem.
                        # Define o centro da linha.
                        c_pos = (item.line().p1() + item.line().p2()) / 2
                        # Define o item final como um nó conectivo, com sua
                        # posição no centro da linha a ser quebrada.
                        self.end_item = Node(Node.NoConectivo, self.myLineMenu)
                        self.end_item.setPos(c_pos +
                                             QtCore.QPointF(-3.5, -3.5))
                        # Define o break_mode como 1 (quebra regular de linha)
                        self.break_mode = 1
                        # Armazena a linha a ser quebrada para uso posterior.
                        self.edge_broken = item
                    # Se o item englobado pelo elipse de precisão for ele
                    # próprio, significa que não o botão do mouse não foi solto
                    # sobre nenhum elemento na cena. Assim, cria-se
                    # simplesmente um nó de passagem na posição clicada.
                    elif (isinstance(item, QtGui.QGraphicsEllipseItem)
                            and not node_priority and not edge_priority):
                        self.end_item = Node(Node.NoConectivo, self.myLineMenu)
                        self.end_item.setPos(mouse_event.scenePos())
            # A linha provisória e o elipse de precisão são removidos.
            self.removeItem(self.line)
            self.line = None
            self.removeItem(ell)

            # Testes posteriores do start_item e end_item
            # Se o start item for uma barra e o end_item um simples nó
            # conectivo, substitui-se o último por um religador.
            if self.start_item.myItemType == Node.Barra:
                if self.end_item.myItemType == Node.NoConectivo:
                    self.removeItem(self.end_item)
                    self.end_item = Node(Node.Religador, self.myRecloserMenu)
                    self.addItem(self.end_item)
                    self.end_item.setPos(mouse_event.scenePos())
            # Se o end item for uma barra e o start item um simples nó
            # conectivo, substitui-se o último por um religador.
            if self.end_item.myItemType == Node.Barra:
                if self.start_item.myItemType == Node.NoConectivo:
                    self.removeItem(self.start_item)
                    self.start_item = Node(Node.Religador, self.myRecloserMenu)
                    self.addItem(self.start_item)
                    self.start_item.setPos(self.pressPos)

            # Teste de comprimento de linha. Se a linha criada for muito
            # pequena, a função retorna sem a criação da mesma.
            dist = math.sqrt(
                math.pow(
                    self.start_item.pos().x() -
                    self.end_item.pos().x(), 2) + math.pow(
                    self.start_item.pos().y() - self.end_item.pos().y(), 2))
            if dist < 15:
                print "Erro: Comprimento da ligação muito pequeno!"
                return
            # Se houver uma linha a ser quebrada, mas esta for fixa (ligada a
            # uma barra), a quebra não será realizada e a função retorna.
            if self.edge_broken is not None and self.edge_broken.isPermanent:
                print "Não se pode quebrar esta linha!"
                return
            # Correção de eventuais discrepâncias entre a associação de cena
            # para os itens supracitados.
            if self.start_item.scene() is None:
                self.addItem(self.start_item)
            if self.end_item.scene() is None:
                self.addItem(self.end_item)

            # Finalmente, faz-se a ligação entre start e end item e a adiciona
            # a linha à cena.
            edge = Edge(self.start_item, self.end_item, self.myLineMenu)
            self.addItem(edge)
            edge.set_color(QtCore.Qt.black)
            edge.update_position()

            # Chama a função de break_edge com seu devido modo de quebra
            self.break_edge(self.edge_broken, self.break_mode, edge)

            # Inversão dos itens w1 e w2 por conveniência, caso w1 seja um nó
            # conectivo
            if edge.w1.myItemType == Node.NoConectivo:
                aux = edge.w1
                edge.w1 = edge.w2
                edge.w2 = aux

            # Deseleciona itens selecionados
            for item in self.selectedItems():
                item.setSelected(False)

            self.no = None

        # Caso o modo seja de seleção de itens, seleciona os itens englobados
        # pelo retângulo de seleção.
        elif self.myMode == self.SelectItems and self.selectRect:
            path = QtGui.QPainterPath()
            path.addRect(self.selectRect.rect())
            self.setSelectionArea(path)
            self.removeItem(self.selectRect)
            self.selectRect = None

        self.line = None
        self.itemInserted.emit(3)
        super(SceneWidget, self).mouseReleaseEvent(mouse_event)

    def mouseDoubleClickEvent(self, mouse_event):
        '''
            Este método define as ações realizadas quando um evento do tipo
            mouseDoubleClick e detectado no diagrama grafico. Neste caso
            conecta os dois elementos que estão ligados pela linha criada no
            evento mousePress.
        '''
        # Se um item for clicado duplamente, abre o diálogo de configuração
        # de parâmetros.
        for item in self.selectedItems():
            if isinstance(item, Node):
                item.setSelected(True)
                self.launch_dialog()
                item.setSelected(False)
                return
        # Cria o item elipse de precisão.
        ell = QtGui.QGraphicsEllipseItem()
        ell.setRect(QtCore.QRectF(mouse_event.scenePos() -
                    QtCore.QPointF(10, 10), QtCore.QSizeF(30, 30)))
        self.addItem(ell)

        # Se o elipse de precisão englobar uma linha, abre o diálogo de
        # configuração de linha.
        for item in self.items():
            if item.collidesWithItem(ell) and isinstance(item, Edge):
                if ell.scene() is not None:
                    self.removeItem(ell)
                item.setSelected(True)
                self.launch_dialog()
                item.setSelected(False)
                return
            else:
                if ell.scene() is not None:
                    self.removeItem(ell)

    # Define a função de aperto de diversas teclas. O trecho a seguir é
    # auto-explicativo.
    def keyPressEvent(self, event):
        key = event.key()
        if self.keyControlIsPressed is True:
            if key == QtCore.Qt.Key_Z:
                self.undoStack.undo()
            if key == QtCore.Qt.Key_Y:
                self.undoStack.redo()
        if key == QtCore.Qt.Key_Space:
            self.change_state()
        if key == QtCore.Qt.Key_Up:
            for item in self.selectedItems():
                item.moveBy(0, -5)
        elif key == QtCore.Qt.Key_Down:
            for item in self.selectedItems():
                item.moveBy(0, 5)
        elif key == QtCore.Qt.Key_Left:
            for item in self.selectedItems():
                item.moveBy(-5, 0)
        elif key == QtCore.Qt.Key_Right:
            for item in self.selectedItems():
                item.moveBy(5, 0)
        elif key == QtCore.Qt.Key_Space or key == QtCore.Qt.Key_Enter:
            pass
        elif key == QtCore.Qt.Key_Control:
            self.keyControlIsPressed = True
        elif key == QtCore.Qt.Key_Delete:
            self.delete_item()
        elif key == QtCore.Qt.Key_Escape:
            self.clearSelection()
        else:
            pass
            super(SceneWidget, self).keyPressEvent(event)
        return

    def keyReleaseEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Control:
            self.keyControlIsPressed = False

    # Função break_edge usada para quebrar a linha quando a inserção é a partir
    # ou em cima de uma linha.
    def break_edge(self, edge, mode, original_edge, insert=None):
        if mode == 3:
            break_point = insert
        if mode == 2:
            command = AddRemoveCommand("Add", self, original_edge)
            self.undoStack.push(command)
            return
        if mode == 0:
            break_point = self.start_item
        if mode == 1:
            break_point = self.end_item
        edge.w1.remove_edge(edge)
        edge.w2.remove_edge(edge)
        self.removeItem(edge)
        new_edge_1 = Edge(edge.w1, break_point, self.myLineMenu)
        new_edge_2 = Edge(break_point, edge.w2, self.myLineMenu)
        self.addItem(new_edge_1)
        self.addItem(new_edge_2)
        new_edge_1.update_position()
        new_edge_2.update_position()

    # Definição da função de recuperar uma linha quando está foi quebrada.
    def recover_edge(self, item):
        w = []

        for edge in item.edges:
            if edge.w1 == item:
                w.append(edge.w2)
            elif edge.w2 == item:
                w.append(edge.w1)
        item.remove_edges()
        new_edge = Edge(w[0], w[1], self.myLineMenu)
        self.addItem(new_edge)
        new_edge.update_position()

    def set_item_type(self, type):
        '''
            Define em qual tipo de item sera inserido no diagrama grafico assim
            que um evento do tipo mousePress for detectado, podendo ser:
            Node.Subestacao
            Node.Religador
            Node.Barra
            Node.Agent
        '''
        self.myItemType = type

    def set_mode(self, mode):
        '''
            Define em qual modo
        '''
        self.myMode = mode

    def change_state(self):
        '''
            Define a função que muda o estado do religador. Esta função será
            chamada no momento que o usuário tiver selecionado um religador e
            pressionado a barra de espaço.
        '''
        print "entrou"
        for item in self.selectedItems():
            if item.myItemType == Node.Religador:
                aviso = AvisoReligador(item.chave.normalOpen, item.chave.nome)
                if aviso.dialog.result() == 1:
                    print item.chave.normalOpen
                    if item.chave.normalOpen == 1:
                        item.chave.normalOpen = 0
                    elif item.chave.normalOpen == 0:
                        item.chave.normalOpen = 1
                    item.setSelected(False)
                    item.setSelected(True)
                    print item.chave.normalOpen
                else:
                    continue

    def create_actions(self):
        '''
            Este metodo cria as ações que serão utilizadas nos menus dos itens
            gráficos. Auto-explicativo: ver QtGui.QAction na biblioteca Pyside.
        '''
        self.propertysAction = QtGui.QAction(
            'Abrir/Fechar', self, shortcut='Enter',
            triggered=self.change_state)
        self.deleteAction = QtGui.QAction(
            'Excluir Item', self, shortcut='Delete',
            triggered=self.delete_item)
        self.increaseBusAction = QtGui.QAction(
            'Aumentar Barra', self, shortcut='Ctrl + a',
            triggered=self.increase_bus)
        self.decreaseBusAction = QtGui.QAction(
            'Diminuir Barra', self, shortcut='Ctrl + d',
            triggered=self.decrease_bus)
        self.alignHLineAction = QtGui.QAction(
            'Alinha Linha H', self, shortcut='Ctrl + h',
            triggered=self.align_line_h)
        self.alignVLineAction = QtGui.QAction(
            'Alinhar Linha V', self, shortcut='Ctrl + v',
            triggered=self.align_line_v)
        self.simulate_action = QtGui.QAction(
            'Simular', self, shortcut='Ctrl + m',
            triggered=self.simulate)

    def create_menus(self):
        '''
            Este metodo cria os menus de cada um dos itens gráficos: religador,
            subestação, barra e linha. Auto-explicativo: ver QtGui.QMenu na
            biblioteca do Pyside.
        '''
        self.myBusMenu = QtGui.QMenu('Menu Bus')
        self.myBusMenu.addAction(self.increaseBusAction)
        self.myBusMenu.addAction(self.decreaseBusAction)
        self.myBusMenu.addAction(self.deleteAction)
        self.myBusMenu.addAction(self.propertysAction)

        self.myRecloserMenu = QtGui.QMenu('Menu Recloser')
        self.myRecloserMenu.addAction(self.propertysAction)
        self.myRecloserMenu.addAction(self.deleteAction)

        self.mySubstationMenu = QtGui.QMenu('Menu Subestacao')
        self.mySubstationMenu.addAction(self.propertysAction)
        self.mySubstationMenu.addAction(self.deleteAction)

        self.myLineMenu = QtGui.QMenu('Menu Linha')
        self.myLineMenu.addAction(self.alignHLineAction)
        self.myLineMenu.addAction(self.alignVLineAction)
        self.myLineMenu.addAction(self.propertysAction)
        self.myLineMenu.addAction(self.deleteAction)

    def delete_item(self):
        '''
            Este método implementa a ação de exclusão de um item gráfico do
            diagrama.
        '''
        for item in self.selectedItems():
            item.Noc = None
            if isinstance(item, Node):
                # Se o item selecionado não for um nó conectivo e tiver pelo
                # menos uma edge associada, este item é eliminado e em seu
                # lugar aparece um nó conectivo.
                if item.myItemType != Node.NoConectivo:
                    lista = item.edges
                    if len(item.edges) >= 1:
                        item.Noc = Node(Node.NoConectivo, self.myLineMenu)
                        self.addItem(item.Noc)
                        item.Noc.setPos(item.scenePos() +
                                        QtCore.QPointF(20, 20))
                        for edge in lista:
                            if edge.w1 == item:
                                new_edge = Edge(
                                    item.Noc, edge.w2, self.myLineMenu)
                            else:
                                new_edge = Edge(
                                    item.Noc, edge.w1, self.myLineMenu)
                            self.addItem(new_edge)
                    item.remove_edges()
                # Caso o item possua mais de duas linhas ligadas, o comporta
                # mento se torna imprevisível, então é emitida uma mensagem ao
                # usuário restringindo esta ação.
                if len(item.edges) > 2:
                    dialog = AvisoConexaoDialog()
                    return
                # Caso o item deletado seja um nó conectivo conectando duas
                # linhas, este é eliminado e é feito uma só linha conectada
                # aos objetos anteriormente ligados.
                elif (len(item.edges) == 2
                        and item.myItemType == Node.NoConectivo):
                    self.recover_edge(item)
            if isinstance(item, Edge):

                # Se o item selecionado for uma edge e o extremo analisado for
                # um nó conectivo solitário, este é deletado juntamente com
                # a linha.
                if (item.w1.myItemType == Node.NoConectivo
                        and len(item.w1.edges) <= 1):
                    self.removeItem(item.w1)
                if (item.w2.myItemType == Node.NoConectivo
                        and len(item.w2.edges) <= 1):
                    self.removeItem(item.w2)
                item.w1.remove_edge(item)
                item.w2.remove_edge(item)
            # Remove o item
            self.removeItem(item)
            command = AddRemoveCommand("Remove", self, item)
            self.undoStack.push(command)

    def launch_dialog(self):
        '''
            Este método inicia os diálogos de configuração de cada um dos itens
            gráficos do diagrama.
        '''
        for item in self.selectedItems():
            # O comentário explicativo abaixo é valido para o caso dos diversos
            # tipos de node.
            if isinstance(item, Node):
                # Caso Religador
                if item.myItemType == Node.Religador:
                    # Chama a função relativa à abertura do dialog referente
                    # ao religador
                    dialog = RecloserDialog(item)
                    # Caso o usuário aperte "OK":
                    if dialog.dialog.result() == 1:
                        item.text_config = unicode(
                            dialog.testeLineEdit.currentText())
                        # Válido para cada caixa de entrada: Se a entrada do
                        # usuário for em branco, o campo continua com o mesmo
                        # valor atribuído a ele anteriormente. Caso contrário,
                        # atribui o valor inserido pelo usuário ao parâmetro
                        # correspondente.
                        if dialog.identificaOLineEdit.text() == "":
                            pass
                        else:
                            item.chave.nome = dialog.identificaOLineEdit.text()
                            item.text.setPlainText(
                                dialog.identificaOLineEdit.text())
                        if dialog.correnteNominalLineEdit.text() == "":
                            pass
                        else:
                            item.chave.ratedCurrent = \
                                dialog.correnteNominalLineEdit.text()
                        if dialog.capacidadeDeInterrupOLineEdit.text() == "":
                            pass
                        else:
                            item.chave.breakingCapacity = \
                                dialog.capacidadeDeInterrupOLineEdit.text()
                        if dialog.nDeSequNciasDeReligamentoLineEdit.text() == \
                                "":
                            pass
                        else:
                            item.chave.recloseSequences = \
                                dialog.nDeSequNciasDeReligamentoLineEdit.text()
                    else:
                        return dialog.dialog.result()

                # Caso Barra
                if item.myItemType == Node.Barra:
                    dialog = BarraDialog(item)
                    if dialog.dialog.result() == 1:
                        if dialog.nomeLineEdit.text() == "":
                            pass
                        else:
                            item.text.setPlainText(dialog.nomeLineEdit.text())
                            item.barra.nome = dialog.nomeLineEdit.text()
                        if dialog.fasesLineEdit.text() == "":
                            pass
                        else:
                            item.barra.phases = dialog.fasesLineEdit.text()
                    else:
                        return dialog.dialog.result()

                # Caso Subestação
                if item.myItemType == Node.Subestacao:
                    dialog = SubstationDialog(item)
                    if dialog.dialog.result() == 1:
                        if dialog.nomeLineEdit.text() == "":
                            pass
                        else:
                            item.text.setPlainText(dialog.nomeLineEdit.text())
                            item.substation.nome = dialog.nomeLineEdit.text()
                        if dialog.tpLineEdit.text() == "":
                            pass
                        else:
                            item.substation.tensao_primario = \
                                dialog.tpLineEdit.text()
                    else:
                        return dialog.dialog.result()

                # Caso Nó de Carga
                if item.myItemType == Node.NoDeCarga:
                    dialog = EnergyConsumerDialog(item)
                    if dialog.dialog.result() == 1:
                        if dialog.identificaOLineEdit.text() == "":
                            pass
                        else:
                            item.text.setPlainText(
                                dialog.identificaOLineEdit.text())
                            item.no_de_carga.nome = \
                                dialog.identificaOLineEdit.text()
                        if dialog.potNciaAtivaLineEdit.text() == "":
                            pass
                        else:
                            item.no_de_carga.potencia_ativa = \
                                dialog.potNciaAtivaLineEdit.text()
                        if dialog.potNciaReativaLineEdit.text() == "":
                            pass
                        else:
                            item.no_de_carga.potencia_reativa = \
                                dialog.potNciaReativaLineEdit.text()
                    else:
                        return dialog.dialog.result()

            # Caso o item seja uma linha, abre-se o dialog referente às
            # configuração da linha. O procedimento é análogo ao feito para
            # o caso Node.
            if isinstance(item, Edge):
                print str(item.linha.id)
                dialog = ConductorDialog(item)
                if dialog.dialog.result() == 1:
                        if dialog.comprimentoLineEdit.text() == "":
                            pass
                        else:
                            item.linha.comprimento = \
                                dialog.comprimentoLineEdit.text()
                        if dialog.resistenciaLineEdit.text() == "":
                            pass
                        else:
                            item.linha.resistencia = \
                                dialog.resistenciaLineEdit.text()
                        if dialog.resistenciaZeroLineEdit.text() == "":
                            pass
                        else:
                            item.linha.resistencia_zero = \
                                dialog.resistenciaZeroLineEdit.text()
                        if dialog.reatanciaLineEdit.text() == "":
                            pass
                        else:
                            item.linha.reatancia = \
                                dialog.reatanciaLineEdit.text()
                        if dialog.reatanciaZeroLineEdit.text() == "":
                            pass
                        else:
                            item.linha.reatancia_zero = \
                                dialog.reatanciaZeroLineEdit.text()
                        if dialog.ampacidadeLineEdit.text() == "":
                            pass
                        else:
                            item.linha.ampacidade = \
                                dialog.ampacidadeLineEdit.text()
                else:
                        return dialog.dialog.result()

    def increase_bus(self):
        '''
            Este método implementa a ação de aumentar o tamanho do item gráfico
            barra.
        '''

        for item in self.selectedItems():
            if isinstance(item, Node):
                item.prepareGeometryChange()
                item.setRect(
                    item.rect().x(), item.rect().y(), item.rect().width(),
                    item.rect().height() * 1.25)

    def decrease_bus(self):
        '''
            Este método implementa a ação de diminuir o tamanho do item gráfico
            barra.
        '''
        for item in self.selectedItems():
            if isinstance(item, Node):
                item.prepareGeometryChange()
                item.setRect(
                    item.rect().x(), item.rect().y(), item.rect().width(),
                    item.rect().height() / 1.25)

    def align_line_h(self):
        w1_is_locked = False
        w2_is_locked = False
        for item in self.selectedItems():
            if isinstance(item, Edge):
                for edge in item.w1.edges:
                    if (edge.w1.myItemType == Node.Barra
                            or edge.w2.myItemType == Node.Barra):
                        w1_is_locked = True
                for edge in item.w2.edges:
                    if (edge.w1.myItemType == Node.Barra
                            or edge.w2.myItemType == Node.Barra):
                        w2_is_locked = True
                if w1_is_locked and not w2_is_locked:
                    pos = QtCore.QPointF(
                        item.w2.center().x(), item.w1.center().y())
                    item.w2.set_center(pos)
                    item.update_position()
                if w2_is_locked and not w1_is_locked:
                    pos = QtCore.QPointF(
                        item.w1.center().x(), item.w2.center().y())
                    item.w1.set_center(pos)
                    item.update_position()

                else:
                    pos = QtCore.QPointF(
                        item.w2.center().x(), item.w1.center().y())
                    item.w2.set_center(pos)
                    item.update_position()
        for item in self.items():
            if isinstance(item, Edge):
                item.update_position()

    def align_line_v(self):
        for item in self.selectedItems():
            if isinstance(item, Edge):
                if item.w1.x() < item.w2.x():
                    pos = QtCore.QPointF(
                        item.w1.center().x(), item.w2.center().y())
                    item.w2.set_center(pos)
                else:
                    pos = QtCore.QPointF(
                        item.w2.center().x(), item.w1.center().y())
                    item.w1.set_center(pos)
                item.update_position()
                item.update_ret()

    def h_align(self):
        has_pos_priority = False
        has_bar_priority = False
        y_pos_list = []
        for item in self.selectedItems():
            if isinstance(item, Node):
                if item.myItemType == Node.Religador:
                    has_pos_priority = True
                    pos_item = item.pos().y()
                if item.myItemType == Node.Barra and item.bar_busy is True:
                    has_bar_priority = True
                    pos_barra = item.pos().y()

        for item in self.selectedItems():
            if isinstance(item, Node):
                if item.myItemType != Node.Barra:
                    if has_bar_priority:
                        continue
                else:
                    y_pos_list.append(item.pos().y())
                    continue

                if item.myItemType == Node.NoConectivo:
                    if has_pos_priority:
                        continue
                    else:
                        y_pos_list.append(item.pos().y())
                else:
                    y_pos_list.append(item.pos().y())

        max_pos = max(y_pos_list)
        min_pos = min(y_pos_list)
        mean_pos = max_pos - abs(max_pos - min_pos) / 2.0

        for item in self.selectedItems():
            if isinstance(item, Node):
                if item.Fixed is True:
                        mean_pos = item.pos().y()
                        item.mean_pos = mean_pos

        for item in self.selectedItems():
            if isinstance(item, Node):
                pos = mean_pos

                if item.Fixed is True:
                    continue
                if (has_bar_priority is True
                        and item.myItemType == Node.Subestacao):
                    pos = pos_barra + 25

                elif has_pos_priority:
                    pos = pos_item

                if item.myItemType == Node.NoConectivo:
                    pos = pos + 17

                if item.myItemType == Node.NoDeCarga:
                    pos = pos + 15

                if item.myItemType == Node.Barra:
                    pos = pos_barra

                item.setY(pos)

        for item in self.selectedItems():
            if isinstance(item, Edge):
                item.update_position()

    def v_align(self):
        x_pos_list = []
        for item in self.selectedItems():
            if isinstance(item, Node):
                x_pos_list.append(item.pos().x())
        max_pos = max(x_pos_list)
        min_pos = min(x_pos_list)
        mean_pos = max_pos - abs(max_pos - min_pos) / 2.0

        for item in self.selectedItems():
            if isinstance(item, Node):
                item.setX(mean_pos)

        for item in self.selectedItems():
            if isinstance(item, Edge):
                item.update_position()

    def set_grid(self):
        if self.my_background_style == self.GridStyle:
            self.setBackgroundBrush(QtGui.QBrush(
                QtCore.Qt.white, QtCore.Qt.NoBrush))
            self.my_background_style = self.NoStyle
        elif self.my_background_style == self.NoStyle:
            self.setBackgroundBrush(QtGui.QBrush(
                QtCore.Qt.lightGray, QtCore.Qt.CrossPattern))
            self.my_background_style = self.GridStyle

    def simulate(self):

        '''
        Inicia a simulação: cálculos de fluxo de carga e curto circuito
        '''
        # Força o usuário a salvar o diagrama antes da simulação
        path = self.main_window.save()
        # Roda o algoritmo conversor CIM >> XML padrão RNP
        bridge = Bridge.Convert(path)        
        #Monta a RNP, carregando o caminho do XML em padrão RNP
        load = xml2objects.Carregador(bridge.path)
        # Carrega a topologia
        top = load.carregar_topologia()
        sub1 = top["subestacoes"]["SE1"]
        sub1.calculaimpedanciaeq()
        data1 = sub1.calculacurto('monofasico')
        #print data1[0]
        # sub1.calculacurto('trifasico')
        # sub1.calculacurto('bifasico')
        # sub1.calculacurto('monofasico_minimo')
        # sub1.calcular_fluxo_de_carga()
        # Abre a aba de simulação
        self.main_window.sim_view = QtGui.QTabWidget()  
        self.main_window.centralwidget.addTab(self.main_window.sim_view,QtGui.QApplication.translate(
                    "main_window", "Simulação", None,
                    QtGui.QApplication.UnicodeUTF8))
        # Cria uma tabela para apresentar os dados de curto-circuito e a adiciona como uma tab da tab
        # simulação.
        self.main_window.sim_sc_table = QtGui.QTableWidget()
        self.main_window.sim_sc_grid_layout = QtGui.QGridLayout()
        self.main_window.sim_sc_grid_layout.addWidget(self.main_window.sim_sc_table,0,0)
        self.main_window.sim_view.addTab(self.main_window.sim_sc_table,QtGui.QApplication.translate(
                    "main_window", "Curto-Circuito", None))
        # Seta o número de colunas da tabela
        self.main_window.sim_sc_table.setColumnCount(3)
        # Seta o número de linhas de dados
        self.main_window.sim_sc_table.setRowCount(len(sub1.alimentadores.values()[0].trechos))
        # Adiciona os cabeçalhos horizontal e vertical a partir dos dados obtidos
        self.main_window.sim_sc_table.setHorizontalHeaderLabels(data1[0])
        data1.pop(0)
        for row in data1:
            for col in range(self.main_window.sim_sc_table.columnCount()):
                self.main_window.sim_sc_table.setItem(data1.index(row),col, QtGui.QTableWidgetItem(row[col]))


        # Cria uma tabela para apresentar os dados de fluxo de carga e a adiciona como uma tab da tab
        # simulação.
        self.main_window.sim_pf_table = QtGui.QTableWidget()
        self.main_window.sim_pf_grid_layout = QtGui.QGridLayout()
        self.main_window.sim_pf_grid_layout.addWidget(self.main_window.sim_pf_table,0,0)
        self.main_window.sim_view.addTab(self.main_window.sim_pf_table,QtGui.QApplication.translate(
                    "main_window", "Fluxo de Carga", None))
        # Adiciona uma tabela à aba de simulação
        # for sub in top["subestacoes"].values():
            
        #     self.main_window.sim_table.setRowCount()
        #     self.main_window.sim_table.setColumnCount(len(top["trechos"]))
        #     self.main_window.sim_table.adjustSize()
            


        




class ViewWidget(QtGui.QGraphicsView):
    '''
        Esta classe implementa o container QGraphicsView
        onde residirá o objeto QGraphicsScene.
    '''
    def __init__(self, scene):

        super(ViewWidget, self).__init__(scene)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)

    def wheelEvent(self, event):
        self.scale_view(math.pow(2.0, -event.delta() / 240.0))

    def scale_view(self, scale_factor):
        factor = self.matrix().scale(scale_factor, scale_factor).mapRect(
            QtCore.QRectF(0, 0, 1, 1)).width()
        if factor < 0.5 or factor > 3:
            return
        self.scale(scale_factor, scale_factor)


class AddRemoveCommand(QtGui.QUndoCommand):
    def __init__(self, mode, scene, item):
        super(AddRemoveCommand, self).__init__(mode)
        self.mode = mode
        self.item = item
        self.scene = scene
        self.count = 0

    def redo(self):
        self.count += 1
        if self.count <= 1:
            return
        if self.mode == "Add":
            self.scene.addItem(self.item)
            self.scene.addItem(self.item.text)
        if self.mode == "Remove":
            self.scene.removeItem(self.item)

    def undo(self):
        if self.mode == "Add":
            self.scene.removeItem(self.item)
        if self.mode == "Remove":
            self.scene.addItem(self.item)
            if self.item.Noc is not None:
                lista = self.item.Noc.edges
                for edge in lista:
                    if edge.w1 == self.item.Noc:
                        new_edge = Edge(
                            self.item, edge.w2, self.scene.myLineMenu)
                    else:
                        new_edge = Edge(
                            self.item, edge.w1, self.scene.myLineMenu)
                    self.scene.addItem(new_edge)
                self.item.Noc.remove_edges()
                self.scene.removeItem(self.item.Noc)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    scene = SceneWidget()
    widget = ViewWidget(scene)
    widget.show()
    sys.exit(app.exec_())
