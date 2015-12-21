#! /usr/bin/python
# -*- coding: utf-8 -*-

# Criado em: Sun Jan 26 16:58:45 2014
#        por: Lucas S Melo
#

from PySide import QtCore, QtGui
from smartpower.core.graphics import SceneWidget, ViewWidget
from smartpower.core.cursor import Cursor
import sys
import os
import smartpower.core.models as models


class JanelaPrincipal(object):
    '''
        Esta classe implementa a interface grafica do simulador
    '''

    def __init__(self):
        self.cursor = Cursor("") #cww
        pass

    def inicializar_componentes(self, main_window):
        '''
            Este metodo implementa os componentes da interface grafica
        '''

        # define a janela pricipal do aplicativo
        main_window.setObjectName('main_window')
        main_window.setWindowIcon(QtGui.QIcon('icon.png'))
        main_window.resize(900, 700)

        # define o widget central do aplicativo
        self.centralwidget = QtGui.QTabWidget(main_window)
        self.centralwidget.setObjectName('centralwidget')

        # define o tipo de layout do widget central como gridLayout
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName('gridLayout')

        # define a classe SceneWidget e ViewWidget como containers dos widgets
        self.sceneWidget = SceneWidget(self)
        self.graphicsView = ViewWidget(self.sceneWidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(256, 0))
        self.graphicsView.setObjectName('graphicsView')
        self.centralwidget.addTab(self.graphicsView,'Diagrama')

        # adiciona os sinais ao objeto sceneWidget
        self.sceneWidget.itemInserted.connect(self.itemInserted)
        # conecta os botoes aos signals da sceneWidget
        # self.sceneWidget.InsertItem.connect(self.itemInserted)

        # seta o objeto QGraphicsView no gridLayout
        #self.gridLayout.addWidget(self.graphicsView, 0, 0)
        main_window.setCentralWidget(self.centralwidget)

        # define a barra de menus
        self.menubar = QtGui.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 25))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)

        #Cria os Menu e Submenus na barra de menu
        self.fileMenu = self.menubar.addMenu('Arquivo')
        self.showMenu = self.menubar.addMenu('Exibir')
        self.orgMenu = self.menubar.addMenu('Organizar')
        self.simulationMenu = self.menubar.addMenu(u'Simulação')
        self.helpMenu = self.menubar.addMenu('Ajuda')
        #Cria o submenu Alinhar e o coloca no menu Organizar
        self.alignSubmenu = self.orgMenu.addMenu('Alinhar')
        #Cria o submenu Texto e o coloca no menu Organizar CW
        self.textSubmenu = self.showMenu.addMenu('Texto')

        # define a barra de status
        self.statusbar = QtGui.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)
        '''
        # define a barra de ferramentas
        self.toolBar = QtGui.QToolBar(main_window)
        self.toolBar.setEnabled(True)
        self.toolBar.setObjectName("toolBar")
        main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        '''
        # define o widget dockWidget dockWidget_Buttons e configura seu
        # conteudo dockWidget_Buttons_Contents CWW
        self.dockWidget_Buttons = QtGui.QDockWidget(main_window)#QtGui.QDockWidget(main_window)
        self.dockWidget_Buttons.setCursor(self.cursor) #CWW'
        self.dockWidget_Buttons.setObjectName("dockWidget_Buttons")
        self.dockWidget_Buttons_Contents = QtGui.QWidget()
        self.dockWidget_Buttons_Contents.setMinimumWidth(230)
        self.dockWidget_Buttons_Contents.setObjectName(
            "dockWidget_Buttons_Contents")

        #  define o layput dos botoes no dockWidget  gridLayout
        self.gridLayout_dockWidget = QtGui.QGridLayout(
            self.dockWidget_Buttons_Contents)
        self.gridLayout_dockWidget.setObjectName("gridLayout_dockWidget")

        # define o objeto QToolBox que comportara as abas de botoes
        self.toolBox = QtGui.QToolBox(self.dockWidget_Buttons_Contents)
        self.toolBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBox.setObjectName("toolBox")

        # define a primeira pagina do dockWidget
        self.page_1 = QtGui.QWidget()
        self.page_1.setGeometry(QtCore.QRect(0, 0, 100, 50))

        # configura a primeira pagina do dockWidget
        size_policy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(
            self.page_1.sizePolicy().hasHeightForWidth())
        self.page_1.setSizePolicy(size_policy)
        self.page_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.page_1.setAutoFillBackground(True)
        self.page_1.setObjectName("page_1")

        # define o Layout da primeira pagina do dockWidget
        self.gridlayout_page_1 = QtGui.QGridLayout(self.page_1)
        self.gridlayout_page_1.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridlayout_page_1.setObjectName("gridlayout_page_1")

        # define os botoes da primeira pagina do dockWidget e insere no
        # FormLayout cw
        self.iconSubstation = QtGui.QIcon("icones/iconSubstation.png")
        self.iconBus = QtGui.QIcon("icones/iconBus.png")
        self.iconRecloser = QtGui.QIcon("icones/iconRecloser.png")
        self.iconLine = QtGui.QIcon("icones/iconLine.png")
        self.iconNode = QtGui.QIcon("icones/iconNode.png")
        self.icontam = QtCore.QSize(90,90)
        self.substationButton = QtGui.QToolButton(self.page_1)
        self.substationButton.setIcon(self.iconSubstation)
        self.substationButton.setIconSize(self.icontam)
        self.substationButton.setObjectName("substationButton")
        self.substationButton.setCheckable(True)
        self.busButton = QtGui.QToolButton(self.page_1)
        self.busButton.setIcon(self.iconBus)
        self.busButton.setIconSize(self.icontam)
        self.busButton.setObjectName("busButton")
        self.busButton.setCheckable(True)
        self.recloserButton = QtGui.QToolButton(self.page_1)
        self.recloserButton.setIcon(self.iconRecloser)
        self.recloserButton.setIconSize(self.icontam)
        self.recloserButton.setObjectName("recloserButton")
        self.recloserButton.setCheckable(True)
        self.lineButton = QtGui.QToolButton(self.page_1)
        self.lineButton.setIcon(self.iconLine)
        self.lineButton.setIconSize(self.icontam)
        self.lineButton.setObjectName("lineButton")
        self.lineButton.setCheckable(True)
        self.noButton = QtGui.QToolButton(self.page_1)
        self.noButton.setIcon(self.iconNode)
        self.noButton.setIconSize(self.icontam)
        self.noButton.setObjectName("noButton")
        self.noButton.setCheckable(True)


        # define o grupo de botoes da pagina 1 do notebook
        self.buttonGroup = QtGui.QButtonGroup()
        self.buttonGroup.addButton(self.substationButton, 0)
        self.buttonGroup.addButton(self.recloserButton, 1)
        self.buttonGroup.addButton(self.busButton, 2)
        self.buttonGroup.addButton(self.lineButton, 3)
        self.buttonGroup.addButton(self.noButton, 4)
        self.buttonGroup.setExclusive(False)

        self.buttonGroup.buttonClicked[int].connect(self.buttonGroupClicked)
        self.buttonGroup.buttonPressed[int].connect(self.buttonGroupPressed)
        self.buttonGroup.buttonPressed[int].connect(main_window.setCursorIcon)
        #self.buttonGroup.buttonReleased[int].connect(main_window.setCursorPad)
        #self.buttonGroup.buttonReleased[int].connect(self.buttonGroupReleased)

        # define labels da primeira pagina do dockWidget
        self.substationLabel = QtGui.QLabel('')
        self.substationLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.substationLabel.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.substationLabel.setObjectName("substationLabel")
        self.recloserLabel = QtGui.QLabel('')
        self.recloserLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.recloserLabel.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.recloserLabel.setObjectName("recloserLabel")
        self.busLabel = QtGui.QLabel('')
        self.busLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.busLabel.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.busLabel.setObjectName("busLabel")
        self.lineLabel = QtGui.QLabel('')
        self.lineLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.lineLabel.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.lineLabel.setObjectName("lineLabel")
        self.noLabel = QtGui.QLabel('')
        self.noLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.noLabel.setSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.noLabel.setObjectName("noLabel")

        # adiciona os botoes ao gridLayout_3
        self.gridlayout_page_1.addWidget(self.substationButton, 0, 0)
        self.gridlayout_page_1.addWidget(self.recloserButton, 0, 1)
        self.gridlayout_page_1.addWidget(self.substationLabel, 1, 0)
        self.gridlayout_page_1.addWidget(self.recloserLabel, 1, 1)
        self.gridlayout_page_1.addWidget(self.busButton, 2, 0)
        self.gridlayout_page_1.addWidget(self.lineButton, 2, 1)
        self.gridlayout_page_1.addWidget(self.busLabel, 3, 0)
        self.gridlayout_page_1.addWidget(self.lineLabel, 3, 1)
        self.gridlayout_page_1.addWidget(self.noButton, 4, 0)
        self.gridlayout_page_1.addWidget(self.noLabel, 5, 0) 

        # adiciona o gridLayout_3 a pagina_1 do dockWidget
        self.page_1.setLayout(self.gridlayout_page_1)

        # seta a primeira pagina do dockWidget
        self.toolBox.addItem(self.page_1, "")

        # define a segunda pagina do dockWidget
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 100, 50))
        self.page_2.setObjectName("page_2")
        self.toolBox.addItem(self.page_2, "")

        self.gridLayout_dockWidget.addWidget(self.toolBox, 0, 0)
        self.dockWidget_Buttons.setWidget(self.dockWidget_Buttons_Contents)

        main_window.addDockWidget(
            QtCore.Qt.DockWidgetArea(1), self.dockWidget_Buttons)

        # configura os botoes da barra de ferramentas

        # cria e configura acao de sair do programa
        self.actionExit = QtGui.QAction(main_window)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setShortcut('Ctrl+Q')
        #self.toolBar.addAction(self.actionExit)
        self.fileMenu.addAction(self.actionExit)

        # cria e configura acao de salvar o estado atual do programa
        self.actionSave = QtGui.QAction(
            main_window, triggered=self.save)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setShortcut('Ctrl+S')
        #self.toolBar.addAction(self.actionSave)
        self.fileMenu.addAction(self.actionSave)

        # cria e configura acao de abrir um arquivo com uma configuração da
        # rede montada anteriormente
        self.actionOpen = QtGui.QAction(main_window, triggered=self.open)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.setShortcut('Ctrl+A')
        #self.toolBar.addAction(self.actionOpen)
        self.fileMenu.addAction(self.actionOpen)

        # cria e configura acao de inserir ou retirar grade no diagrama grafico
        self.actionGrid = QtGui.QAction(
            main_window, triggered=self.sceneWidget.set_grid)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGrid.setIcon(icon)
        self.actionGrid.setObjectName("actionGrid")
        self.actionGrid.setShortcut('Ctrl+G')
        #self.toolBar.addAction(self.actionGrid)
        self.showMenu.addAction(self.actionGrid)

        # cria e configura ação de alinhar horizontalmente itens no diagrama
        # gráfico
        self.actionHalign = QtGui.QAction(
            main_window, triggered=self.sceneWidget.h_align)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGrid.setIcon(icon)
        self.actionGrid.setObjectName("actionHalign")
        self.actionHalign.setShortcut('Ctrl+H')
        #self.toolBar.addAction(self.actionHalign)
        self.alignSubmenu.addAction(self.actionHalign)

        # cria e configura ação de alinhar verticalmente items no diagrama
        # gráfico
        self.actionValign = QtGui.QAction(
            main_window, triggered=self.sceneWidget.v_align)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGrid.setIcon(icon)
        self.actionGrid.setObjectName("actionValign")
        self.actionValign.setShortcut('Ctrl+V')
        #self.toolBar.addAction(self.actionValign)
        self.alignSubmenu.addAction(self.actionValign)

        # cria e configura acao de selecionar items no diagrama grafico
        self.actionSelect = QtGui.QAction(
            main_window, triggered=self.setSelect)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelect.setIcon(icon)
        self.actionSelect.setObjectName("actionSelect")
        self.actionSelect.setShortcut('Ctrl+E')
        #self.toolBar.addAction(self.actionSelect)
        self.orgMenu.addAction(self.actionSelect)

        # cria e configura ação de abrir a interface de simulação
        self.action_simulate = QtGui.QAction(
            main_window, triggered=self.sceneWidget.simulate)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGrid.setIcon(icon)
        self.actionGrid.setObjectName("actionSimulate")
        self.action_simulate.setShortcut('Ctrl+M')
        #self.toolBar.addAction(self.action_simulate)
        self.simulationMenu.addAction(self.action_simulate)

        # cria e configura a acao de tornar o texto visível ou não CW
        ### subestação
        self.actionTextVisibleSubstation = QtGui.QAction(
            main_window, triggered=self.sceneWidget.setTextSubstation)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTextVisibleSubstation.setIcon(icon)
        self.actionTextVisibleSubstation.setObjectName("actionTextVisibleSubstation")
        self.textSubmenu.addAction(self.actionTextVisibleSubstation)
        ### religador
        self.actionTextVisibleRecloser =QtGui.QAction(
            main_window, triggered=self.sceneWidget.setTextRecloser)
        self.actionTextVisibleRecloser.setIcon(icon)
        self.actionTextVisibleRecloser.setObjectName("actionTextVisibleRecloser")
        self.textSubmenu.addAction(self.actionTextVisibleRecloser)
        ### barra
        self.actionTextVisibleBus =QtGui.QAction(
            main_window, triggered=self.sceneWidget.setTextBus)
        self.actionTextVisibleBus.setIcon(icon)
        self.actionTextVisibleBus.setObjectName("actionTextVisibleBus")
        self.textSubmenu.addAction(self.actionTextVisibleBus)
        ### no de carga
        self.actionTextVisibleNodeC =QtGui.QAction(
            main_window, triggered=self.sceneWidget.setTextNodeC)
        self.actionTextVisibleNodeC.setIcon(icon)
        self.actionTextVisibleNodeC.setObjectName("actionTextVisibleNodeC")
        self.textSubmenu.addAction(self.actionTextVisibleNodeC)

        # configurações adicionais
        self.retranslateUi(main_window)
        #self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def itemInserted(self, item_type):
        '''
            Callback chamada no momento em que um item e inserido
            no diagrama grafico
        '''
        # self.buttonGroup.button(item_type).setChecked(False)
        # self.sceneWidget.set_mode(self.sceneWidget.MoveItem)
        pass

    def save(self):
        '''
            Função que salva o diagrama gráfico em um arquivo .XML 
        '''
        filename = QtGui.QFileDialog.getSaveFileName(
            None, 'Salvar Diagrama', os.getenv('HOME'))
        file = models.DiagramToXML(self.sceneWidget)
        file.write_xml(filename[0])
        filename_CIM = filename[0] + '_CIM'

        file2 = models.CimXML(self.sceneWidget)
        file2.write_xml(filename_CIM)

        return filename_CIM

    def open(self):
        '''
            Função que redesenha um diagrama gráfico que foi salvo anteriormente em um arquivo .XML
        '''
        filename = QtGui.QFileDialog.getOpenFileName(
            None, 'Abrir Diagrama', os.getenv('HOME'))
        file = models.XMLToDiagram(self.sceneWidget, filename[0])

    def setSelect(self):
        '''
            Callback chamada no momento em que se faz necessario
            alterar do modo de selecao para movimentacao de items
            no diagrama grafico ou vice-versa
        '''
        if self.sceneWidget.myMode == self.sceneWidget.SelectItems:
            self.sceneWidget.set_mode(self.sceneWidget.MoveItem)
        else:
            self.sceneWidget.set_mode(self.sceneWidget.SelectItems)

        for id in range(6):
            self.buttonGroup.button(id).setChecked(False)       

    def buttonGroupClicked(self, id):
        '''
            Callback chamada no momento em que um botão de inserção
            de itens é clicado. CW
        '''
        if id==3:
           self.buttonGroup.button(id).setChecked(True) 
        pass

    def buttonGroupPressed(self, id):
        '''
            Callback chamada no momento em que um botão de inserção
            de itens é pressionado. CW
        '''
        self.buttonGroup.button(id).setChecked(True) #cwwww

        # Altera o icone de acordo com o button pressionado: AQUIIII!!!!!
        #self.main_window.cursor.setShapeRecl(self.main_window)
        #print "mudou"
        '''
        buttons = self.buttonGroup.buttons() 
        for button in buttons:
            if self.buttonGroup.button(id).isChecked():
                if self.buttonGroup.button(id) != button:
                    button.setChecked(False)
            #else:
                #button.setChecked(False)

        # Altera o modo para: inserir linha, inserir item ou mover item.
        if self.buttonGroup.button(id).isChecked():
            if id == 3:
                self.sceneWidget.set_mode(SceneWidget.InsertLine)
            else:
                self.sceneWidget.set_item_type(id)
                self.sceneWidget.set_mode(SceneWidget.InsertItem)
        else:
            self.sceneWidget.set_mode(SceneWidget.MoveItem)
        '''

        buttons = self.buttonGroup.buttons() 
        for button in buttons:
            if self.buttonGroup.button(id) != button:
                button.setChecked(False)

        # Altera o modo para: inserir linha, inserir item ou mover item.
        if id == 3:
            self.sceneWidget.set_mode(SceneWidget.InsertLine)
        else:
            self.sceneWidget.set_item_type(id)
            self.sceneWidget.set_mode(SceneWidget.InsertItem)
        print "press group"

    def buttonGroupReleased(self):
        '''
            Callback chamada no momento em que um botão de inserção
            de itens é liberado. CW
        '''
        print "group release"
        self.dockWidget_Buttons.setCursor(Cursor(""))


    def buttonGroupUncheck(self):
        '''
            Callback chamada para remover a seleção de todos os buttons.
        '''
        buttons = self.buttonGroup.buttons()

        for button in buttons:
            button.setChecked(False)

        self.sceneWidget.set_mode(SceneWidget.MoveItem)

    def retranslateUi(self, main_window):

        main_window.setWindowTitle(QtGui.QApplication.translate(
            "main_window", "Smart Power v0.2 - Simulador de Redes Elétricas de Distribuição",
            None, QtGui.QApplication.UnicodeUTF8))

        #self.toolBar.setWindowTitle(
        #    QtGui.QApplication.translate("main_window", "toolBar", None,
        #                                 QtGui.QApplication.UnicodeUTF8))

        self.substationButton.setText(
            QtGui.QApplication.translate(
                "main_window", "Subestação", None,
                QtGui.QApplication.UnicodeUTF8))

        self.busButton.setText(
            QtGui.QApplication.translate(
                "main_window", "Barra", None, QtGui.QApplication.UnicodeUTF8))

        self.busLabel.setText(
            QtGui.QApplication.translate(
                "main_window", "Barra", None, QtGui.QApplication.UnicodeUTF8))

        self.substationLabel.setText(
            QtGui.QApplication.translate(
                "main_window", "Subestação", None,
                QtGui.QApplication.UnicodeUTF8))

        self.recloserButton.setText(
            QtGui.QApplication.translate(
                "main_window", "Religador", None,
                QtGui.QApplication.UnicodeUTF8))

        self.recloserLabel.setText(
            QtGui.QApplication.translate(
                "main_window", "Religador", None,
                QtGui.QApplication.UnicodeUTF8))

        self.lineButton.setText(
            QtGui.QApplication.translate(
                "main_window", "Linha", None, QtGui.QApplication.UnicodeUTF8))

        self.lineLabel.setText(
            QtGui.QApplication.translate(
                "main_window", "Linha", None, QtGui.QApplication.UnicodeUTF8))

        self.noButton.setText(
            QtGui.QApplication.translate(
                "main_window", "Nó de Carga", None, QtGui.QApplication.UnicodeUTF8))

        self.noLabel.setText(
            QtGui.QApplication.translate(
                "main_window", "Nó de Carga", None, QtGui.QApplication.UnicodeUTF8))

        self.toolBox.setItemText(
            self.toolBox.indexOf(self.page_1),
            QtGui.QApplication.translate(
                "main_window", "Pagina 1", None,
                QtGui.QApplication.UnicodeUTF8))

        self.toolBox.setItemText(
            self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate(
                "main_window", "Pagina 2", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionExit.setText(
            QtGui.QApplication.translate(
                "main_window", "Sair", None, QtGui.QApplication.UnicodeUTF8))

        self.actionExit.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Sair", None, QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionExit.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "4, Backspace", None,
                QtGui.QApplication.UnicodeUTF8))
        '''    
        self.actionSave.setText(
            QtGui.QApplication.translate(
                "main_window", "Salvar", None, QtGui.QApplication.UnicodeUTF8))
    
        self.actionSave.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Salvar", None, QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionSave.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "4, Ctrl + S", None,
                QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionOpen.setText(
            QtGui.QApplication.translate(
                "main_window", "Abrir", None, QtGui.QApplication.UnicodeUTF8))

        self.actionOpen.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Abrir", None, QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionOpen.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "4, Ctrl + A", None,
                QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionGrid.setText(
            QtGui.QApplication.translate(
                "main_window", "Grade", None, QtGui.QApplication.UnicodeUTF8))

        self.actionGrid.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Grade", None, QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionGrid.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "Ctrl, g", None,
                QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionHalign.setText(
            QtGui.QApplication.translate(
                "main_window", "Horizontalmente", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionHalign.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Alinha Horizontalmente", None,
                QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionHalign.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "Ctrl, h", None,
                QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionValign.setText(
            QtGui.QApplication.translate(
                "main_window", "Verticalmente", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionValign.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Alinha Verticalmente", None,
                QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionValign.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "Ctrl, h", None,
                QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionSelect.setText(
            QtGui.QApplication.translate(
                "main_window", "Selecionar Items", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionSelect.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Selecionar Items", None,
                QtGui.QApplication.UnicodeUTF8))
        '''
        self.actionSelect.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "Ctrl, e", None,
                QtGui.QApplication.UnicodeUTF8))
        '''
        self.action_simulate.setText(
            QtGui.QApplication.translate(
                "main_window", "Simular", None,
                QtGui.QApplication.UnicodeUTF8))

        self.action_simulate.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Simular", None,
                QtGui.QApplication.UnicodeUTF8))
        
        ## Configuração das QActions para exibir textos dos elementos, sem atalhos. CW
        self.actionTextVisibleSubstation.setText(
            QtGui.QApplication.translate(
                "main_window", "Subestações", None, QtGui.QApplication.UnicodeUTF8))

        self.actionTextVisibleSubstation.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Exibe ou apaga os textos dos elementos do tipo Subestação", None, QtGui.QApplication.UnicodeUTF8))

        self.actionTextVisibleRecloser.setText(
            QtGui.QApplication.translate(
                "main_window", "Religadores", None, QtGui.QApplication.UnicodeUTF8))

        self.actionTextVisibleRecloser.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Exibe ou apaga os textos dos elementos do tipo Religador", None, QtGui.QApplication.UnicodeUTF8))

        self.actionTextVisibleBus.setText(
            QtGui.QApplication.translate(
                "main_window", "Barras", None, QtGui.QApplication.UnicodeUTF8))

        self.actionTextVisibleBus.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Exibe ou apaga os textos dos elementos do tipo Religador", None, QtGui.QApplication.UnicodeUTF8))

        self.actionTextVisibleNodeC.setText(
            QtGui.QApplication.translate(
                "main_window", "Nós de Carga", None, QtGui.QApplication.UnicodeUTF8))

        self.actionTextVisibleNodeC.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Exibe ou apaga os textos dos elementos do tipo Nó de Carga", None, QtGui.QApplication.UnicodeUTF8))

#
#class ButtonWidget(QtGui.QDockWidget):
#    '''
        #Classe que cria a widget que conterá os buttons. CWWWW
#    '''
#    def __init__(self, main_window):
##
 #   def mouseReleaseEvent(self, mouse_event):
#        print "ButtonWidget release"
#        self.setCursor(Cursor(""))
#        super(ButtonWidget, self).mouseReleaseEvent(mouse_event)
#    

class ControlMainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.cursor = Cursor("")
        self.setCursor(self.cursor)
        self.ui = JanelaPrincipal()
        self.ui.inicializar_componentes(self)

    def mouseReleaseEvent(self, mouse_event):
        '''
            Função da chamada no momento que o evento mouse release é enviado. Quando um
            item arrastado para a área de desenho é liberado, este item é desenhado e o 
            programa volta para o modo de seleção de itens.
        ''' 
        self.setCursorPad(1)
        super(ControlMainWindow, self).mouseReleaseEvent(mouse_event)
        sinal = QtGui.QGraphicsSceneMouseEvent(QtCore.QEvent.GraphicsSceneMouseRelease)
        sinal.setPos(self.ui.graphicsView.mapToScene(
            self.ui.graphicsView.mapFromGlobal(self.cursor.pos()))) 
        self.ui.sceneWidget.mouseReleaseEvent(sinal)
        self.ui.buttonGroupUncheck()

    def setCursorIcon(self, id):
        '''
            Callback que altera o formato do cursor dando a impressão visual de 
            'arrastar' o elemento para dentro do diagrama gráfico. cw
        '''
        self.cursor.setShape(self, id)
        self.ui.cursor.setShape(self.ui.dockWidget_Buttons, id)

    def setCursorPad(self, id):
        '''
            Função que altera o formato do cursor para a seta padrão. cw
        '''
        self.cursor.setShapePad(self)
        self.ui.cursor.setShapePad(self.ui.dockWidget_Buttons)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())