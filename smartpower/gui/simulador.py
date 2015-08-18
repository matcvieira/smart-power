#! /usr/bin/python
# -*- coding: utf-8 -*-

# Criado em: Sun Jan 26 16:58:45 2014
#        por: Lucas S Melo
#

from PySide import QtCore, QtGui
from smartpower.core.graphics import SceneWidget, ViewWidget
from models import DiagramToXML
import sys
import os
import models


class JanelaPrincipal(object):
    '''
        Esta classe implementa a inteface grafica do simulador
    '''

    def __init__(self):
        pass
        # self.createActions()
        # self.createMenus()

    def inicializar_componentes(self, main_window):
        '''
            Este metodo implementa os componentes da inteface grafica
        '''

        # define a janela pricipal do aplicativo
        main_window.setObjectName('main_window')
        main_window.setWindowIcon(QtGui.QIcon('icon.png'))
        main_window.resize(900, 700)

        # define o widget central do aplicativo
        self.centralwidget = QtGui.QWidget(main_window)
        self.centralwidget.setObjectName('centralwidget')

        # define o tipo de layout do widget central como gridLayout
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName('gridLayout')

        # define a classe SceneWidget e ViewWidget como containers dos widgets
        self.sceneWidget = SceneWidget()
        self.graphicsView = ViewWidget(self.sceneWidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(256, 0))
        self.graphicsView.setObjectName('graphicsView')

        # adiciona os sinais ao objeto sceneWidget
        self.sceneWidget.itemInserted.connect(self.itemInserted)
        # conecta os botoes aos signals da sceneWidget
        # self.sceneWidget.InsertItem.connect(self.itemInserted)

        # seta o objeto QGraphicsView no gridLayout
        self.gridLayout.addWidget(self.graphicsView, 0, 0)
        main_window.setCentralWidget(self.centralwidget)

        # define a barra de menus
        self.menubar = QtGui.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 25))
        self.menubar.setObjectName("menubar")
        main_window.setMenuBar(self.menubar)

        # define a barra de status
        self.statusbar = QtGui.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        # define a barra de ferramentas
        self.toolBar = QtGui.QToolBar(main_window)
        self.toolBar.setEnabled(True)
        self.toolBar.setObjectName("toolBar")
        main_window.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        # define o widget dockWidget dockWidget_Buttons e configura seu
        # conteudo dockWidget_Buttons_Contents
        self.dockWidget_Buttons = QtGui.QDockWidget(main_window)
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
        # FormLayout
        self.substationButton = QtGui.QPushButton(self.page_1)
        self.substationButton.setObjectName("substationButton")
        self.substationButton.setCheckable(True)
        self.busButton = QtGui.QPushButton(self.page_1)
        self.busButton.setObjectName("busButton")
        self.busButton.setCheckable(True)
        self.recloserButton = QtGui.QPushButton(self.page_1)
        self.recloserButton.setObjectName("recloserButton")
        self.recloserButton.setCheckable(True)
        self.lineButton = QtGui.QPushButton(self.page_1)
        self.lineButton.setObjectName("lineButton")
        self.lineButton.setCheckable(True)
        self.noButton = QtGui.QPushButton(self.page_1)
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
        self.toolBar.addAction(self.actionExit)

        # cria e configura acao de salvar o estado atual do programa
        self.actionSave = QtGui.QAction(
            main_window, triggered=self.save)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon)
        self.actionSave.setObjectName("actionSave")
        self.toolBar.addAction(self.actionSave)

        # cria e configura acao de abrir um arquivo com uma configuração da
        # rede montada anteriormente
        self.actionOpen = QtGui.QAction(main_window, triggered=self.open)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.toolBar.addAction(self.actionOpen)

        # cria e configura acao de inserir ou retirar grade no diagrama grafico
        self.actionGrid = QtGui.QAction(
            main_window, triggered=self.sceneWidget.set_grid)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGrid.setIcon(icon)
        self.actionGrid.setObjectName("actionGrid")
        self.toolBar.addAction(self.actionGrid)

        # cria e configura ação de alinhar horizontalmente itens no diagrama
        # gráfico
        self.actionHalign = QtGui.QAction(
            main_window, triggered=self.sceneWidget.h_align)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGrid.setIcon(icon)
        self.actionGrid.setObjectName("actionHalign")
        self.toolBar.addAction(self.actionHalign)

        # cria e configura ação de alinhar verticalmente items no diagrama
        # gráfico
        self.actionValign = QtGui.QAction(
            main_window, triggered=self.sceneWidget.v_align)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGrid.setIcon(icon)
        self.actionGrid.setObjectName("actionValign")
        self.toolBar.addAction(self.actionValign)

        # cria e configura acao de selecionar items no diagrama grafico
        self.actionSelect = QtGui.QAction(
            main_window, triggered=self.setSelect)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSelect.setIcon(icon)
        self.actionSelect.setObjectName("actionSelect")
        self.toolBar.addAction(self.actionSelect)

        # configurações adicionais
        self.retranslateUi(main_window)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def itemInserted(self, item_type):
        '''
            Callback chamada no momento em que um item e iserido
            no diagrama grafico
        '''
        # self.buttonGroup.button(item_type).setChecked(False)
        # self.sceneWidget.set_mode(self.sceneWidget.MoveItem)
        pass

    def save(self):
        filename = QtGui.QFileDialog.getSaveFileName(
            None, 'Salvar Diagrama', os.getenv('HOME'))
        print filename
        file = models.DiagramToXML(self.sceneWidget)
        file.write_xml(filename[0])

        file2 = models.CimXML(self.sceneWidget)
        file2.write_xml(filename[0] + '_CIM')

    def open(self):
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

    def buttonGroupClicked(self, id):
        '''
            Callback chamada no momento em que um botão de inserção
            de itens e pressionado.
        '''

        if self.buttonGroup.button(id).isChecked():
            state = 'COMP 1'
        else:
            state = 'COMP 2'

        buttons = self.buttonGroup.buttons()
        for button in buttons:
            if state == 'COMP 1':
                if self.buttonGroup.button(id) != button:
                    button.setChecked(False)
            elif state == 'COMP 2':
                button.setChecked(False)

        if state == 'COMP 1':
            if id == 3:
                self.sceneWidget.set_mode(SceneWidget.InsertLine)
            else:
                self.sceneWidget.set_item_type(id)
                self.sceneWidget.set_mode(SceneWidget.InsertItem)
        elif state == 'COMP 2':
            self.sceneWidget.set_mode(SceneWidget.MoveItem)


    def retranslateUi(self, main_window):

        main_window.setWindowTitle(QtGui.QApplication.translate(
            "main_window", "Smart Power v0.2 - Simulador de Redes Elétricas de Distribuição",
            None, QtGui.QApplication.UnicodeUTF8))

        self.toolBar.setWindowTitle(
            QtGui.QApplication.translate("main_window", "toolBar", None,
                                         QtGui.QApplication.UnicodeUTF8))

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

        self.actionExit.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "4, Backspace", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionSave.setText(
            QtGui.QApplication.translate(
                "main_window", "Salvar", None, QtGui.QApplication.UnicodeUTF8))

        self.actionSave.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Salvar", None, QtGui.QApplication.UnicodeUTF8))

        self.actionSave.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "4, Ctrl + S", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionOpen.setText(
            QtGui.QApplication.translate(
                "main_window", "Abrir", None, QtGui.QApplication.UnicodeUTF8))

        self.actionOpen.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Abrir", None, QtGui.QApplication.UnicodeUTF8))

        self.actionOpen.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "4, Ctrl + A", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionGrid.setText(
            QtGui.QApplication.translate(
                "main_window", "Grade", None, QtGui.QApplication.UnicodeUTF8))

        self.actionGrid.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Grade", None, QtGui.QApplication.UnicodeUTF8))

        self.actionGrid.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "Ctrl, g", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionHalign.setText(
            QtGui.QApplication.translate(
                "main_window", "Alinha Horizontalmente", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionHalign.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Alinha Horizontalmente", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionHalign.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "Ctrl, h", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionValign.setText(
            QtGui.QApplication.translate(
                "main_window", "Alinha Verticalmente", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionValign.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Alinha Verticalmente", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionValign.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "Ctrl, h", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionSelect.setText(
            QtGui.QApplication.translate(
                "main_window", "Selecionar Items", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionSelect.setToolTip(
            QtGui.QApplication.translate(
                "main_window", "Selecionar Items", None,
                QtGui.QApplication.UnicodeUTF8))

        self.actionSelect.setShortcut(
            QtGui.QApplication.translate(
                "main_window", "Ctrl, e", None,
                QtGui.QApplication.UnicodeUTF8))


class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = JanelaPrincipal()
        self.ui.inicializar_componentes(self)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.show()
    sys.exit(app.exec_())
