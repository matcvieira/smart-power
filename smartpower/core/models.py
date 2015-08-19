# -*- encoding: utf-8 -*-
from xml.etree import ElementTree
from xml.dom import minidom
from PySide import QtCore, QtGui
from graphics import Node, Edge, Text
from bs4 import BeautifulSoup
from elementos import NoConect, Terminal, Religador, EnergyConsumer, Substation, BusBarSection




class DiagramToXML(ElementTree.Element):
    '''
        Esta classe possui as funções que armazenam as informações
        necessárias à reconstrução do diagrama grafico em um
        arquivo XML
    '''
    def __init__(self, scene):
        '''
            Função que inicializa o objeto criado pela classe DiagramToXML
        '''
        super(DiagramToXML, self).__init__('items')

        self.scene = scene
        lista = self.scene.items()
        lista.reverse()
        for item in self.scene.items():
            if isinstance(item, Node):
                CE = ElementTree.Element(
                    'CE', attrib={'type': str(item.myItemType)})
                id = ElementTree.Element('id')
                id.text = str(item.id)
                CE.append(id)

                x = ElementTree.Element('x')
                x.text = str(item.scenePos().x())
                CE.append(x)

                y = ElementTree.Element('y')
                y.text = str(item.scenePos().y())
                CE.append(y)

                width = ElementTree.Element('width')
                width.text = str(item.rect().width())
                CE.append(width)

                height = ElementTree.Element('height')
                height.text = str(item.rect().height())
                CE.append(height)

                # Salva as informações referente ao item gráfico religador
                # e os parâmetros da sua chave associada 

                if item.myItemType == Node.Religador:

                    padrao = ElementTree.Element('padrao')
                    padrao.text = str(item.text_config)

                    identificador = ElementTree.Element('identificador')
                    identificador.text = str(item.text.toPlainText())

                    corrente = ElementTree.Element('corrente')
                    corrente.text = str(item.chave.ratedCurrent)

                    in_tt = ElementTree.Element('intt')
                    in_tt.text = str(item.chave.inTransitTime)

                    cap_int = ElementTree.Element('capint')
                    cap_int.text = str(item.chave.breakingCapacity)

                    seq_rel = ElementTree.Element('seqrel')
                    seq_rel.text = str(item.chave.recloseSequences)

                    estado = ElementTree.Element('estado')
                    estado.text = str(item.chave.normalOpen)
                    
                    CE.append(estado)
                    CE.append(corrente)
                    CE.append(in_tt)
                    CE.append(cap_int)
                    CE.append(seq_rel)
                    CE.append(padrao)
                    CE.append(identificador)

                if item.myItemType == Node.NoDeCarga:
                    identificador = ElementTree.Element('identificador')
                    identificador.text = str(item.text.toPlainText())

                    p_ativa = ElementTree.Element('pativa')
                    p_ativa.text = str(item.no_de_carga.potencia_ativa)

                    p_reativa = ElementTree.Element('preativa')
                    p_reativa.text = str(item.no_de_carga.potencia_reativa)

                    CE.append(identificador)
                    CE.append(p_ativa)
                    CE.append(p_reativa)

                if item.myItemType == Node.Subestacao:
                    identificador = ElementTree.Element('identificador')
                    identificador.text = str(item.text.toPlainText())
                    
                    tensao_p = ElementTree.Element('tensaop')
                    tensao_p.text = str(item.substation.tensao_primario)

                    tensao_s = ElementTree.Element('tensaos')
                    tensao_s.text = str(item.substation.tensao_secundario)

                    potencia = ElementTree.Element('potencia')
                    potencia.text = str(item.substation.potencia)

                    impedancia = ElementTree.Element('impedancia')
                    impedancia.text = str(item.substation.impedancia)

                    CE.append(identificador)
                    CE.append(tensao_p)
                    CE.append(tensao_s)
                    CE.append(potencia)
                    CE.append(impedancia)

                if item.myItemType == Node.Barra:
                    identificador = ElementTree.Element('identificador')
                    identificador.text = str(item.text.toPlainText())

                    fases = ElementTree.Element('fases')
                    fases.text = str(item.barra.phases)

                    CE.append(identificador)
                    CE.append(fases)












                self.append(CE)
        for item in lista:

            if isinstance(item, Edge):
                edge = ElementTree.Element('edge')
                w1 = ElementTree.Element('w1')
                w1.text = str(item.w1.id)

                w2 = ElementTree.Element('w2')
                w2.text = str(item.w2.id)

                comprimento = ElementTree.Element('comprimento')
                comprimento.text = str(item.linha.comprimento)

                edge.append(comprimento)
                edge.append(w1)
                edge.append(w2)
                self.append(edge)

    def write_xml(self, path):
        '''
            Função que cria o arquivo XML na localização indicada pelo
            argumento path
        '''
        xml_string = ElementTree.tostring(self)
        dom_element = (minidom.parseString(xml_string))
        f = open(path, 'w')
        f.write(dom_element.toprettyxml())
        f.close()



class XMLToDiagram():
    '''
        Classe que realiza a conversão do arquivo XML com as informações do 
        diagrama em um diagrama gráfico interativo.
    '''

    def __init__(self, scene, file_path):
        self.scene = scene
        self.file_path = file_path

        xml_tree = ElementTree.parse(self.file_path)
        xml_element = xml_tree.getroot()
        self.scene.clear()
        for child in xml_element:

            if child.tag == 'CE':

                if child.attrib['type'] == '0':
                    item = Node(
                        int(child.attrib['type']), self.scene.mySubstationMenu)
                    identificador = child.find('identificador').text
                    tensaop = child.find('tensaop').text
                    tensaos = child.find('tensaos').text
                    potencia = child.find('potencia').text
                    impedancia = child.find('impedancia').text
                    item.substation = Substation(identificador, float(tensaop), float(tensaos), float(potencia), impedancia)
                    self.scene.addItem(item)
                    item.setPos(
                        float(child.find('x').text), float(
                            child.find('y').text))
                    item.id = int(child.find('id').text)
                    item.text.setPlainText(identificador)

                #RELIGADOR
                elif child.attrib['type'] == '1':
                    item = Node(
                        int(child.attrib['type']), self.scene.myRecloserMenu)
                    item.text_config = str(child.find('padrao').text)
                    state = child.find('estado').text
                    corrente = child.find('corrente').text
                    in_tt = child.find('intt').text
                    cap_int = child.find('capint').text
                    seq_rel = child.find('seqrel').text
                    identificador = child.find('identificador').text
                    item.chave = Religador(identificador,int(corrente),int(in_tt),int(cap_int),int(seq_rel),int(state))
                    self.scene.create_dict_recloser(corrente,cap_int,seq_rel,item.text_config)
                    item.id = int(child.find('id').text)
                    item.setPos(float(child.find('x').text), float(
                        child.find('y').text))
                    self.scene.addItem(item)
                    item.text.setPlainText(identificador)
                    #item.text = Text(identificador, item, item.scene())

                #BARRA
                elif child.attrib['type'] == '2':
                    item = Node(int(
                        child.attrib['type']), self.scene.myBusMenu)
                    identificador = child.find('identificador').text
                    fases = child.find('fases').text
                    #item.barra = BusBarSection(identificador, int(fases))
                    item.setPos(float(child.find('x').text), float(
                        child.find('y').text))
                    item.id = int(child.find('id').text)
                    item.setRect(
                        0, 0, float(child.find('width').text), float(
                            child.find('height').text))
                    self.scene.addItem(item)
                    item.text.setPlainText(identificador)

                elif child.attrib['type'] == '3':
                    item = Node(int(child.attrib['type']), None)
                    item.setPos(
                        float(child.find('x').text), float(
                            child.find('y').text))
                    item.id = int(child.find('id').text)
                    self.scene.addItem(item)

                elif child.attrib['type'] == '4':
                    item = Node(int(child.attrib['type']), self.scene.mySubstationMenu)
                    p_ativa = child.find('pativa').text
                    p_reativa = child.find('preativa').text
                    identificador = str(child.find('identificador').text)
                    item.no_de_carga = EnergyConsumer(identificador, p_ativa, p_reativa)
                    item.setPos(
                        float(child.find('x').text), float(
                            child.find('y').text))
                    item.id = int(child.find('id').text)
                    self.scene.addItem(item)
                    
                    item.text.setPlainText(identificador)

                elif child.attrib['type'] == '5':
                    item = Node(int(child.attrib['type']), None)
                    item.setPos(
                        float(child.find('x').text), float(
                            child.find('y').text))
                    item.id = int(child.find('id').text)
                    self.scene.addItem(item)

            elif child.tag == 'edge':
                for item in self.scene.items():
                    if isinstance(item, Node) and item.id == int(child.find('w1').text):
                        w1 = item
                    elif isinstance(item, Node) and item.id == int(child.find('w2').text):
                        w2 = item
                edge = Edge(w1, w2, self.scene.myLineMenu)
                comprimento = str(child.find('comprimento').text)
                edge.linha.comprimento = comprimento
                self.scene.addItem(edge)
                edge.update_position()
                print "opa"


class CimXML():

    '''Classe que representa os dados dos componentes em padrão CIM'''

    def __init__(self, scene):
        self.scene = scene
        self.lista_no_conectivo = []
        self.lista_terminais = []
        self.montar_rede(scene)

        self.cim_xml = BeautifulSoup()

        for item in scene.items():
            if isinstance(item, Node):

                if item.myItemType == item.Religador:

                    tag_breaker = self.cim_xml.new_tag("Breaker")
                    self.cim_xml.append(tag_breaker)

                    tag_id = self.cim_xml.new_tag("mRID")
                    tag_id.append(item.text.toPlainText())
                    tag_breaker.append(tag_id)

                    tag_rc = self.cim_xml.new_tag("ratedCurrent")
                    tag_rc.append(str(item.chave.ratedCurrent))
                    tag_breaker.append(tag_rc)

                    tag_itt = self.cim_xml.new_tag("inTransitTime")
                    tag_itt.append(str(item.chave.inTransitTime))
                    tag_breaker.append(tag_itt)

                    tag_bc = self.cim_xml.new_tag("breakingCapacity")
                    tag_bc.append(str(item.chave.breakingCapacity))
                    tag_breaker.append(tag_bc)

                    tag_rs = self.cim_xml.new_tag("recloseSequences")
                    tag_rs.append(str(item.chave.recloseSequences))
                    tag_breaker.append(tag_rs)

                    tag_NO = self.cim_xml.new_tag("normalOpen")
                    tag_NO.append(str(item.chave.normalOpen))
                    tag_breaker.append(tag_NO)

                    tag_terminal1= self.cim_xml.new_tag("terminal")
                    tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                    tag_seqNumber.append("1")
                    tag_terminal1.append(tag_seqNumber)
                    tag_mRID = self.cim_xml.new_tag("mRID")
                    tag_mRID.append(str(item.terminal1.mRID))
                    tag_terminal1.append(tag_mRID)
                    tag_breaker.append(tag_terminal1)

                    tag_terminal2= self.cim_xml.new_tag("terminal")
                    tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                    tag_seqNumber.append("2")
                    tag_terminal2.append(tag_seqNumber)
                    tag_mRID = self.cim_xml.new_tag("mRID")
                    tag_mRID.append(str(item.terminal2.mRID))
                    tag_terminal2.append(tag_mRID)
                    tag_breaker.append(tag_terminal2)
                    

        for item in scene.items():
            if isinstance(item, Node):

                if item.myItemType == item.Barra:

                    tag_barra = self.cim_xml.new_tag("busBarSection")
                    self.cim_xml.append(tag_barra)

                    tag_id = self.cim_xml.new_tag("mRID")
                    tag_id.append(item.text.toPlainText())
                    tag_barra.append(tag_id)

                    tag_phases = self.cim_xml.new_tag("phases")
                    tag_phases.append(str(item.barra.phases))
                    tag_barra.append(tag_phases)

                    for Terminal in (item.terminals):
                        tag_terminal = self.cim_xml.new_tag("terminal")
                        tag_mRID = self.cim_xml.new_tag('mRID')
                        tag_mRID.append(str(Terminal.mRID)) 
                        tag_terminal.append(tag_mRID)
                        tag_barra.append(tag_terminal)
                    

        
        for item in scene.items():
            if isinstance(item, Node):

                if item.myItemType == item.Subestacao:

                    tag_substation = self.cim_xml.new_tag("Substation")
                    self.cim_xml.append(tag_substation)

                    tag_id = self.cim_xml.new_tag("mRID")
                    tag_id.append(str(item.id))
                    self.cim_xml.find("Substation").append(tag_id)

                    tag_terminal1= self.cim_xml.new_tag("terminal")
                    tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                    tag_seqNumber.append("1")
                    tag_terminal1.append(tag_seqNumber)
                    tag_mRID = self.cim_xml.new_tag("mRID")
                    tag_mRID.append(str(item.terminal1.mRID))
                    tag_terminal1.append(tag_mRID)
                    tag_substation.append(tag_terminal1)

                    tag_terminal2= self.cim_xml.new_tag("terminal")
                    tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                    tag_seqNumber.append("2")
                    tag_terminal2.append(tag_seqNumber)
                    tag_mRID = self.cim_xml.new_tag("mRID")
                    tag_mRID.append(str(item.terminal2.mRID))
                    tag_terminal2.append(tag_mRID)
                    tag_substation.append(tag_terminal2)


        for item in scene.items():
            if isinstance(item, Node):

                if item.myItemType == item.NoDeCarga:

                    tag_energyConsumer = self.cim_xml.new_tag("EnergyConsumer")
                    self.cim_xml.append(tag_energyConsumer)
                    
                    tag_id = self.cim_xml.new_tag("mRID")
                    tag_id.append(item.text.toPlainText())
                    tag_energyConsumer.append(tag_id)

                    tag_pFixed = self.cim_xml.new_tag("pFixed")
                    tag_pFixed.append(str(item.no_de_carga.potencia_ativa))
                    tag_energyConsumer.append(tag_pFixed)


                    tag_qFixed = self.cim_xml.new_tag("qFixed")
                    tag_qFixed.append(str(item.no_de_carga.potencia_reativa))
                    tag_energyConsumer.append(tag_qFixed)               


                    for Terminal in (item.terminals):
                        tag_terminal = self.cim_xml.new_tag("terminal")
                        tag_mRID = self.cim_xml.new_tag('mRID')
                        tag_mRID.append(str(Terminal.mRID)) 
                        tag_terminal.append(tag_mRID)
                        tag_energyConsumer.append(tag_terminal)

        for item in scene.items():
            if isinstance(item, Edge):

                if item.w1.myItemType == Node.Subestacao or item.w2.myItemType == Node.Subestacao:
                    continue

                tag_conductor = self.cim_xml.new_tag("Conductor")
                self.cim_xml.append(tag_conductor)
                
                tag_id = self.cim_xml.new_tag("mRID")
                tag_id.append(item.w1.text.toPlainText() + item.w2.text.toPlainText())
                tag_conductor.append(tag_id)

                tag_length = self.cim_xml.new_tag("length")
                tag_length.append(str(item.linha.comprimento))
                tag_conductor.append(tag_length)

                tag_r = self.cim_xml.new_tag("r")
                tag_r.append(str(item.linha.resistencia))
                tag_conductor.append(tag_r)

                tag_r0 = self.cim_xml.new_tag("r0")
                tag_r0.append(str(item.linha.resistencia_zero))
                tag_conductor.append(tag_r0)

                tag_x = self.cim_xml.new_tag("x")
                tag_x.append(str(item.linha.reatancia))
                tag_conductor.append(tag_x) 

                tag_x0 = self.cim_xml.new_tag("x0")
                tag_x0.append(str(item.linha.reatancia_zero))
                tag_conductor.append(tag_x0)

                tag_currentLimit = self.cim_xml.new_tag("currentLimit")
                tag_currentLimit.append(str(item.linha.ampacidade))
                tag_conductor.append(tag_currentLimit)                   

                tag_terminal1= self.cim_xml.new_tag("terminal")
                tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                tag_seqNumber.append("1")
                tag_terminal1.append(tag_seqNumber)
                tag_mRID = self.cim_xml.new_tag("mRID")
                tag_mRID.append(str(item.terminal1.mRID))
                tag_terminal1.append(tag_mRID)
                tag_conductor.append(tag_terminal1)

                tag_terminal2= self.cim_xml.new_tag("terminal")
                tag_seqNumber = self.cim_xml.new_tag("SequenceNumber")
                tag_seqNumber.append("2")
                tag_terminal2.append(tag_seqNumber)
                tag_mRID = self.cim_xml.new_tag("mRID")
                tag_mRID.append(str(item.terminal2.mRID))
                tag_terminal2.append(tag_mRID)
                tag_conductor.append(tag_terminal2)


        for no in self.lista_no_conectivo:
            tag_mRID = self.cim_xml.new_tag("mRID")
            tag_mRID.append(str(id(no)))

            tag_no_conectivo = self.cim_xml.new_tag("ConnectivityNode")
            tag_no_conectivo.append(tag_mRID)

            self.cim_xml.append(tag_no_conectivo)

            
            for terminal in no.terminal_list:
                tag_terminal = self.cim_xml.new_tag("terminal")
                tag_mRID_terminal = self.cim_xml.new_tag("mRID")
                tag_mRID_terminal.append(str(terminal.mRID))
                tag_terminal.append(tag_mRID_terminal)
                tag_no_conectivo.append(tag_terminal)  


                
    def write_xml(self, path):
        '''
            Função que cria o arquivo XML na localização indicada pelo
            argumento path
        '''
        f = open(path, 'w')
        f.write(self.cim_xml.prettify())
        f.close()


    def montar_rede(self, scene):

        for item in self.scene.items():
            if isinstance(item, Node):
                if item.myItemType != Node.NoConectivo and item.myItemType != Node.Barra and item.myItemType != Node.NoDeCarga:
                    item.terminal1 = Terminal(item)
                    item.terminal2 = Terminal(item)
                    self.lista_terminais.append(item.terminal1)
                    self.lista_terminais.append(item.terminal2)

                if item.myItemType == Node.Barra or item.myItemType == Node.NoDeCarga:
                    for i in range(len(item.edges)):
                        terminal = Terminal(item)
                        item.terminals.append(terminal)
                        self.lista_terminais.append(terminal)
            if isinstance(item, Edge):
                item.terminal1 = Terminal(item)
                item.terminal2 = Terminal(item)
                self.lista_terminais.append(item.terminal1)
                self.lista_terminais.append(item.terminal1)


        for edge in self.scene.items():
            if isinstance(edge, Edge):
                no_conectivo_1 = NoConect([])
                no_conectivo_2 = NoConect([])
                print "start"

                # Ligação do Nó Conectivo relativo à ligação do terminal de w1 com o terminal 1 da linha - CONVENÇÃO!
                if edge.w1.myItemType != Node.NoConectivo and edge.w1.myItemType != Node.Barra and edge.w2.myItemType != Node.Barra and edge.w1.myItemType != Node.NoDeCarga:

                    print "w1 is not NoC"
                    if edge.w1.terminal1.connected:
                        if edge.w1.terminal2.connected:
                            pass
                        else:
                            no_conectivo_1.terminal_list.append(edge.w1.terminal2)
                            edge.w1.terminal2.connect()
                            no_conectivo_1.terminal_list.append(edge.terminal1)
                            edge.terminal1.connect()
                            self.lista_no_conectivo.append(no_conectivo_1)
                    else:
                        no_conectivo_1.terminal_list.append(edge.w1.terminal1)
                        edge.w1.terminal1.connect()
                        no_conectivo_1.terminal_list.append(edge.terminal1)
                        edge.terminal1.connect()
                        self.lista_no_conectivo.append(no_conectivo_1)
                elif edge.w1.myItemType == Node.NoConectivo and edge.w1.con_lock is False:
                    print "w1 is noC"
                    edge.w1.con_lock = True

                    
                    print len(edge.w1.edges)
                    no_conectivo = NoConect([])  
                    print id(no_conectivo.terminal_list)                 
                    for derivation in edge.w1.edges:
                        
                        if derivation.terminal1.connected:
                            print "cp1"
                            if derivation.terminal2.connected:
                                pass
                            else:
                                no_conectivo.terminal_list.append(derivation.terminal2)
                                derivation.terminal2.connect()
                        else:
                            print "cp2"
                            no_conectivo.terminal_list.append(derivation.terminal1)
                            derivation.terminal1.connect()
                    self.lista_no_conectivo.append(no_conectivo)

                elif edge.w1.myItemType == Node.Barra:
                    for terminal in edge.w1.terminals:
                        no_conectivo = NoConect([])
                        if terminal.connected:
                            continue
                        else:
                            no_conectivo.terminal_list.append(terminal)
                            terminal.connect()
                            if edge.w2.terminal1.connected:
                                if edge.w2.terminal2.connected:
                                    pass
                                else:
                                    no_conectivo.terminal_list.append(edge.w2.terminal2)
                                    edge.w2.terminal2.connect()
                            else:
                                no_conectivo.terminal_list.append(edge.w2.terminal1)
                                edge.w2.terminal1.connect()
                            self.lista_no_conectivo.append(no_conectivo)
                            break

                elif edge.w1.myItemType == Node.NoDeCarga:
                    for terminal in edge.w1.terminals:
                        no_conectivo = NoConect([])
                        if terminal.connected:
                            continue
                        else:
                            if edge.terminal1.connected:
                                if edge.terminal2.connected:
                                    pass
                                else:
                                    no_conectivo.terminal_list.append(terminal)
                                    terminal.connect()
                                    no_conectivo.terminal_list.append(edge.terminal2)
                                    edge.terminal2.connect()
                            else:
                                no_conectivo.terminal_list.append(terminal)
                                terminal.connect()
                                no_conectivo.terminal_list.append(edge.terminal1)
                                edge.terminal1.connect()



                            self.lista_no_conectivo.append(no_conectivo)
                            break

                # Ligação do Nó Conectivo relativo à ligação do terminal de w2 com o terminal 2 da linha - CONVENÇÃO!
                if edge.w2.myItemType != Node.NoConectivo and edge.w2.myItemType != Node.Barra and edge.w1.myItemType != Node.Barra and edge.w2.myItemType != Node.NoDeCarga:
                    print "w2 is not NoC"
                    if edge.w2.terminal1.connected:
                        if edge.w2.terminal2.connected:
                            pass
                        else:
                            no_conectivo_2.terminal_list.append(edge.w2.terminal2)
                            edge.w2.terminal2.connect()
                            no_conectivo_2.terminal_list.append(edge.terminal2)
                            edge.terminal2.connect()
                            self.lista_no_conectivo.append(no_conectivo_2)
                    else:
                        no_conectivo_2.terminal_list.append(edge.w2.terminal1)
                        edge.w2.terminal1.connect()
                        no_conectivo_2.terminal_list.append(edge.terminal2)
                        edge.terminal1.connect()
                        self.lista_no_conectivo.append(no_conectivo_2)

                elif edge.w2.myItemType == Node.NoConectivo and edge.w2.con_lock is False:
                    print "w2 is noC"
                    edge.w2.con_lock = True
                    no_conectivo = NoConect([])
                    print id(no_conectivo.terminal_list)  
                    
                    for derivation in edge.w2.edges:
                        
                        if derivation.terminal1.connected:
                            if derivation.terminal2.connected:
                                pass
                            else:
                                no_conectivo.terminal_list.append(derivation.terminal2)
                                derivation.terminal2.connect()
                        else:
                            no_conectivo.terminal_list.append(derivation.terminal1)
                            derivation.terminal1.connect()
                            
                    self.lista_no_conectivo.append(no_conectivo)

                elif edge.w2.myItemType == Node.Barra:
                    for terminal in edge.w2.terminals:
                        no_conectivo = NoConect([])
                        if terminal.connected:
                            continue
                        else:
                            no_conectivo.terminal_list.append(terminal)
                            terminal.connect()
                            if edge.w1.terminal1.connected:
                                if edge.w1.terminal2.connected:
                                    pass
                                else:
                                    no_conectivo.terminal_list.append(edge.w1.terminal2)
                                    edge.w1.terminal2.connect()
                            else:
                                no_conectivo.terminal_list.append(edge.w1.terminal1)
                                edge.w1.terminal1.connect()
                            self.lista_no_conectivo.append(no_conectivo)
                            break

                elif edge.w2.myItemType == Node.NoDeCarga:
                    for terminal in edge.w2.terminals:
                        no_conectivo = NoConect([])
                        if terminal.connected:
                            continue
                        else:
                            if edge.terminal1.connected:
                                if edge.terminal2.connected:
                                    pass
                                else:
                                    no_conectivo.terminal_list.append(terminal)
                                    terminal.connect()
                                    no_conectivo.terminal_list.append(edge.terminal2)
                                    edge.terminal2.connect()
                            else:
                                no_conectivo.terminal_list.append(terminal)
                                terminal.connect()
                                no_conectivo.terminal_list.append(edge.terminal1)
                                edge.terminal1.connect()
                            self.lista_no_conectivo.append(no_conectivo)
                            break

                print "end"


        print "=========================Lista de Nós Conectivos=========================\n\n"
        for no in self.lista_no_conectivo:
            print str(id(no)) + "\n"
        print "=========================================================================\n\n"
        for no in self.lista_no_conectivo:
            print "===============================NÓ CONECTIVO - " + str(id(no)) + "============\n\n"
            for no2 in no.terminal_list:
                if isinstance(no2.parent, Edge):
                    print "terminal: " + str(id(no2)) + "\n" + "objeto: " + "Edge" + "\n" + "Posição: " + str(no2.parent.scenePos()) + "\n"
                else:
                    print "terminal: " + str(id(no2)) + "\n" + "objeto: " + str(no2.parent.text.toPlainText()) + "\n" + "Posição: " + str(no2.parent.scenePos()) + "\n"
            print "=====================================================================\n\n"

        print "--------------------------------------------------------------------------"




