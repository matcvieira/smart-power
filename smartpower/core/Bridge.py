# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from xml.dom import minidom

class Setor(object):
    def __init__(self):
        self.vizinhos = []
        self.nos = []

class Substation(object):
    def __init__(self, lista_alimentadores):
        self.alimentadores = lista_alimentadores



class Convert(object):
    def __init__(self, cim_path = None):

        if cim_path == None:
            return
        self.xml_cim = BeautifulSoup(open(cim_path))
        xml_rnp = BeautifulSoup()
        tag_rede = xml_rnp.new_tag("rede")
        tag_elementos = xml_rnp.new_tag("elementos")
        tag_topologia = xml_rnp.new_tag("topologia")
        tag_rede.append(tag_elementos)
        tag_rede.append(tag_topologia)
        xml_rnp.append(tag_rede)

        # Representação de todos os religadores

        for breaker in self.xml_cim.findAll('breaker'):
            breaker.nos = []
            mrid = str(breaker.find('mrid').text).strip()
            nome = mrid
            estado = str(breaker.find('normalopen').text)[3]
            if estado == '1':
                estado = "aberto"
            else:
                estado = "fechado"
            chave = xml_rnp.new_tag("chave")
            chave["nome"] = nome
            chave["estado"] = estado
            tag_elementos.append(chave)

        tag_condutor = xml_rnp.new_tag("condutor")
        tag_condutor["nome"] = "CAA 266R"
        tag_condutor["rp"] = "0.2391"
        tag_condutor["xp"] = "0.37895"
        tag_condutor["rz"] = "0.41693"
        tag_condutor["xz"] = "1.55591"
        tag_condutor["ampacidade"] = "301"
        tag_elementos.append(tag_condutor)

        # Representação de todos os nós de carga. A representação dos
        # nós da barra tem de ser feita posteriormente, após definição
        # de setores e alimentadores
        for no_carga in self.xml_cim.findAll('energyconsumer'):
            no = xml_rnp.new_tag("no")
            nome = str(no_carga.find('mrid').text).strip()
            potencia_ativa = no_carga.find('pfixed').text
            potencia_reativa = no_carga.find('qfixed').text

            
            no["nome"] = str(no_carga.find('mrid').text).strip()

            potencia_ativa_tag = xml_rnp.new_tag("potencia")
            potencia_ativa_tag["tipo"] = "ativa"
            potencia_ativa_tag["multip"] = "k"
            potencia_ativa_tag["unid"] = "W"
            potencia_ativa_tag.append(str(potencia_ativa))

            potencia_reativa_tag = xml_rnp.new_tag("potencia")
            potencia_reativa_tag["tipo"] = "reativa"
            potencia_reativa_tag["multip"] = "k"
            potencia_reativa_tag["unid"] = "VAr"
            potencia_reativa_tag.append(str(potencia_reativa))

            no.append(potencia_ativa_tag)
            no.append(potencia_reativa_tag)

            tag_elementos.append(no)


        # Representação de todos os trechos
        self.trechos_min = []
        self.trechos_min2 = []

        for trecho in self.xml_cim.findAll("conductor"):
            trecho.nos = []
            trecho_tag = xml_rnp.new_tag("trecho")
            nome = str(trecho.find('mrid').text).strip()

            trecho_tag["nome"] = nome

            comprimento = xml_rnp.new_tag('comprimento')
            comprimento["multip"] = "k"
            comprimento ["unid"] = "m"
            comprimento.append(trecho.find('length').text)

            trecho_tag.append(comprimento)
            if float(trecho.find('length').text) == 0.01:
                self.trechos_min.append(trecho)
                self.trechos_min2.append(trecho)
            tag_elementos.append(trecho_tag)

            

        # Definição dos setores

        # Definir lista geral de todos os terminais com seus mrid's
        self.lista_terminais = self.xml_cim.findAll("terminal")
        # Definir lista geral de todos os nós conectivos com seus mrid's
        self.lista_nosconect = self.xml_cim.findAll("connectivitynode")
        # Definir a lista de barras
        # lista_barras = self.xml_cim.findAll("busbarsection")
        
        

        for substation in self.xml_cim.findAll('substation'):
            substation.alimentadores = []
            substation_tag = xml_rnp.new_tag('subestacao')
            substation_tag["nome"] = str(substation.find('mrid').text).strip()
            transformador_tag = xml_rnp.new_tag('transformador')

            # FALTA AJEITAR A JANELA PARA INSERÇÃO DOS VALORES CORRETOS
            transformador_tag["nome"] = str(substation.find('mrid').text).strip() + "T"
            transformador_tag_potencia_aparente = xml_rnp.new_tag('potencia')
            transformador_tag_potencia_aparente["tipo"] = "aparente"
            transformador_tag_potencia_aparente["multip"] = "M"
            transformador_tag_potencia_aparente["unid"] = "VA"
            transformador_tag_potencia_aparente.append(str(5))
            transformador_tag.append(transformador_tag_potencia_aparente)

            transformador_tag_impedancia_pos = xml_rnp.new_tag('impedancia')
            transformador_tag.append(transformador_tag_impedancia_pos)
            transformador_tag_impedancia_pos["tipo"] = "seq_pos"
            transformador_tag_impedancia_pos_resistencia = xml_rnp.new_tag('resistencia')
            transformador_tag_impedancia_pos_resistencia["multip"] = ""
            transformador_tag_impedancia_pos_resistencia["unid"] = "ohms"
            transformador_tag_impedancia_pos_resistencia.append(str(10))
            transformador_tag_impedancia_pos.append(transformador_tag_impedancia_pos_resistencia)
            transformador_tag_impedancia_pos_reatancia = xml_rnp.new_tag('reatancia')
            transformador_tag_impedancia_pos_reatancia["multip"] = ""
            transformador_tag_impedancia_pos_reatancia["unid"] = "ohms"
            transformador_tag_impedancia_pos_reatancia.append(str(3))
            transformador_tag_impedancia_pos.append(transformador_tag_impedancia_pos_reatancia)

            transformador_tag_impedancia_zero = xml_rnp.new_tag('impedancia')
            transformador_tag.append(transformador_tag_impedancia_zero)
            transformador_tag_impedancia_zero["tipo"] = "seq_zero"
            transformador_tag_impedancia_zero_resistencia = xml_rnp.new_tag('resistencia')
            transformador_tag_impedancia_zero_resistencia["multip"] = ""
            transformador_tag_impedancia_zero_resistencia["unid"] = "ohms"
            transformador_tag_impedancia_zero_resistencia.append(str(10))
            transformador_tag_impedancia_zero.append(transformador_tag_impedancia_zero_resistencia)
            transformador_tag_impedancia_zero_reatancia = xml_rnp.new_tag('reatancia')
            transformador_tag_impedancia_zero_reatancia["unid"] = "ohms"
            transformador_tag_impedancia_zero_reatancia["multip"] = ""
            transformador_tag_impedancia_zero_reatancia.append(str(10))
            transformador_tag_impedancia_zero.append(transformador_tag_impedancia_zero_reatancia)

            transformador_tag_enrolamento_p = xml_rnp.new_tag('enrolamento')
            transformador_tag.append(transformador_tag_enrolamento_p)
            transformador_tag_enrolamento_p["tipo"] = "primario"
            transformador_tag_enrolamento_p_tensao = xml_rnp.new_tag('tensao')
            transformador_tag_enrolamento_p_tensao["multip"] = "k"
            transformador_tag_enrolamento_p_tensao["unid"] = "V"
            transformador_tag_enrolamento_p_tensao.append(str(13.8))
            transformador_tag_enrolamento_p.append(transformador_tag_enrolamento_p_tensao)

            transformador_tag_enrolamento_s = xml_rnp.new_tag('enrolamento')
            transformador_tag.append(transformador_tag_enrolamento_s)
            transformador_tag_enrolamento_s["tipo"] = "secundario"
            transformador_tag_enrolamento_s_tensao = xml_rnp.new_tag('tensao')
            transformador_tag_enrolamento_s_tensao["multip"] = "k"
            transformador_tag_enrolamento_s_tensao["unid"] = "V"
            transformador_tag_enrolamento_s_tensao.append(str(69))
            transformador_tag_enrolamento_s.append(transformador_tag_enrolamento_s_tensao)
        
            tag_elementos.append(transformador_tag)
            tag_elementos.append(substation_tag)

        self.lista_barras = []
        self.lista_nos_de_carga = self.xml_cim.findAll('energyconsumer')
        
        for no in self.lista_nos_de_carga:
            (vizinhos, chaves) = self.definir_vizinhos(no, 0)
            no.vizinhos = vizinhos
            no.chaves = chaves


        for no in self.lista_barras:
            (vizinhos, chaves) = self.definir_vizinhos(no, 1)
            no.vizinhos = vizinhos
            no.chaves = chaves

        for no in self.lista_barras:
            tag_elemento_no = xml_rnp.new_tag("elemento")
            tag_elemento_no["nome"] = str(no.find('mrid').text).strip()
            tag_elemento_no["tipo"] = "no"            
            tag_vizinhos = xml_rnp.new_tag("vizinhos")
            tag_chaves = xml_rnp.new_tag("chaves")
            tag_elemento_no.append(tag_vizinhos)
            tag_elemento_no.append(tag_chaves)
            for vizinho in no.vizinhos:
                tag_vizinho_no = xml_rnp.new_tag("no")
                tag_vizinho_no["nome"] = str(vizinho.find('mrid').text).strip()
                tag_vizinhos.append(tag_vizinho_no)
            for chave in no.chaves:
                tag_chave = xml_rnp.new_tag("chave")
                tag_chave["nome"] = str(chave.find('mrid').text).strip()
                tag_chaves.append(tag_chave)
            tag_topologia.append(tag_elemento_no)

        # for no in self.lista_nos_de_carga:
        #     # print "VIZINHOS DE " + str(no.find('mrid'))
        #     for vizinho in no.vizinhos:
        #         print str(vizinho.find('mrid'))
        #     print "CHAVES: "
        #     for chave in no.chaves:
        #         print str(chave.find('mrid').text).strip()
        for no in self.lista_nos_de_carga:
            tag_elemento_no = xml_rnp.new_tag("elemento")
            tag_elemento_no["nome"] = str(no.find('mrid').text).strip()
            tag_elemento_no["tipo"] = "no"            
            tag_vizinhos = xml_rnp.new_tag("vizinhos")
            tag_chaves = xml_rnp.new_tag("chaves")
            tag_elemento_no.append(tag_vizinhos)
            tag_elemento_no.append(tag_chaves)
            for vizinho in no.vizinhos:
                tag_vizinho_no = xml_rnp.new_tag("no")
                tag_vizinho_no["nome"] = str(vizinho.find('mrid').text).strip()
                tag_vizinhos.append(tag_vizinho_no)
            for chave in no.chaves:
                tag_chave = xml_rnp.new_tag("chave")
                tag_chave["nome"] = str(chave.find('mrid').text).strip()
                tag_chaves.append(tag_chave)
            tag_topologia.append(tag_elemento_no)

        setores = self.definir_setores()

        for barra in self.lista_barras:
            setor = Setor()
            setor.nos.append(barra)
            barra.setor = setor
            barra.setor.nome = str(barra.find('mrid').text).strip()
            setores.append(setor)


        for setor in setores:
            setor.vizinhos =[]

            setor_tag = xml_rnp.new_tag("setor")
            if setor.nos[0].name == "busbarsection":
                setor_tag["nome"] = str(setor.nos[0].find('mrid').text).strip()
            else:
                setor_tag["nome"] = setor.nome
            tag_elementos.append(setor_tag)

        for chave in self.xml_cim.findAll('breaker'):
            chave.setores = []

        for no in self.lista_nos_de_carga:
            for no2 in no.vizinhos:
                if no.setor != no2.setor:
                    no.setor.vizinhos.append(no2.setor)
            for chave in no.chaves:
                chave.setores.append(no.setor)

        for no in self.lista_barras:
            for no2 in no.vizinhos:
                if no.setor != no2.setor:
                    no.setor.vizinhos.append(no2.setor)
            for chave in no.chaves:
                chave.setores.append(no.setor)

        for setor in setores:
            tag_elemento_setor = xml_rnp.new_tag("elemento")
            tag_elemento_setor["tipo"] = "setor"
            tag_elemento_setor["nome"] = setor.nome
            tag_vizinhos = xml_rnp.new_tag("vizinhos")
            tag_nos = xml_rnp.new_tag("nos")
            tag_elemento_setor.append(tag_vizinhos)
            tag_elemento_setor.append(tag_nos)
            for vizinho in setor.vizinhos:
                tag_setor = xml_rnp.new_tag("setor")
                tag_setor["nome"] = vizinho.nome
                tag_vizinhos.append(tag_setor)
            for no in setor.nos:
                tag_no = xml_rnp.new_tag("no")
                tag_no["nome"] = str(no.find('mrid').text).strip()
                tag_nos.append(tag_no)
            tag_topologia.append(tag_elemento_setor)

        lista_chaves = self.xml_cim.findAll('breaker')
        for chave in lista_chaves:
            tag_elemento_chave = xml_rnp.new_tag("elemento")
            tag_elemento_chave["tipo"] = "chave"
            tag_elemento_chave["nome"] = str(chave.find('mrid').text).strip()
            tag_n1 = xml_rnp.new_tag("n1")
            tag_n2 = xml_rnp.new_tag("n2")
            tag_elemento_chave.append(tag_n1)
            tag_elemento_chave.append(tag_n2)
            
            tag_n1_setor = xml_rnp.new_tag("setor")
            tag_n1_setor["nome"] = str(chave.setores[0].nome)
            tag_n1.append(tag_n1_setor)
            
            tag_n2_setor = xml_rnp.new_tag("setor")
            tag_n2_setor["nome"] = str(chave.setores[1].nome)
            tag_n2.append(tag_n2_setor)
            tag_topologia.append(tag_elemento_chave)


        for trecho in self.xml_cim.findAll("conductor"):
            
            if len(trecho.nos) != 0:
                tag_elemento_trecho = xml_rnp.new_tag("elemento")
                tag_elemento_trecho["nome"] = str(trecho.find('mrid').text).strip()
                tag_elemento_trecho["tipo"] = "trecho"
                tag_n1 = xml_rnp.new_tag("n1")
                tag_n2 = xml_rnp.new_tag("n2")
                tag_condutores = xml_rnp.new_tag("condutores")
                tag_condutor = xml_rnp.new_tag("condutor")
                tag_condutor["nome"] = "CAA 266R"
                tag_condutores.append(tag_condutor)
                tag_elemento_trecho.append(tag_n1)
                tag_elemento_trecho.append(tag_n2)
                tag_elemento_trecho.append(tag_condutores)

                if trecho.nos[0].name == "breaker":
                    tag_chave = xml_rnp.new_tag("chave")
                    tag_chave["nome"] = str(trecho.nos[0].find('mrid').text).strip()
                    tag_n1.append(tag_chave)
                if trecho.nos[0].name == "energyconsumer":
                    tag_no = xml_rnp.new_tag("no")
                    tag_no["nome"] = str(trecho.nos[0].find('mrid').text).strip()
                    tag_n1.append(tag_no)

                if trecho.nos[1].name == "breaker":
                    tag_chave = xml_rnp.new_tag("chave")
                    tag_chave["nome"] = str(trecho.nos[1].find('mrid').text).strip()
                    tag_n2.append(tag_chave)
                if trecho.nos[1].name == "energyconsumer":
                    tag_no = xml_rnp.new_tag("no")
                    tag_no["nome"] = str(trecho.nos[1].find('mrid').text).strip()
                    tag_n2.append(tag_no)

                tag_topologia.append(tag_elemento_trecho)
                      
        

        for setor in setores:
            setor.breakers = []
            for breaker in setor.breakers:
                if breaker.name == "busbarsection":
                    setor.setores = []

        setores_conectados = []
        for breaker in self.xml_cim.findAll('breaker'):
            breaker.setores = []
            for no in breaker.nos:
                breaker.setores.append(no.setor)
            estado = str(breaker.find('normalopen').text)[3]
            breaker.setores[0].breakers.append(breaker)
            breaker.setores[1].breakers.append(breaker)

        alimentadores = self.definir_alimentadores()

        for alimentador in alimentadores:
            tag_alimentador = xml_rnp.new_tag("alimentador")
            tag_alimentador["nome"] = str(id(alimentador))
            tag_elementos.append(tag_alimentador)



        # Primeiramente se resolvem as pendências no XML que necessitavam da definição
        # dos alimentadores

        # Representação dos Nós da barra, que são nós de carga com
        # potência aparente nula
        alimentadores_aux = list(alimentadores)
        for breaker in self.xml_cim.findAll("breaker"):
            if self.detectar_barra(breaker).name == "busbarsection":
                tag_no = xml_rnp.new_tag("no")

                potencia_ativa = 0
                potencia_reativa = 0

                for alimentador in alimentadores:
                    if alimentador[0].nome == breaker.setores[0].nome or alimentador[0].nome == breaker.setores[1].nome:
                        no = alimentador[0]

                
                tag_no["nome"] = no.nome

                potencia_ativa_tag = xml_rnp.new_tag("potencia")
                potencia_ativa_tag["tipo"] = "ativa"
                potencia_ativa_tag["multip"] = "k"
                potencia_ativa_tag["unid"] = "W"
                potencia_ativa_tag.append(str(potencia_ativa))

                potencia_reativa_tag = xml_rnp.new_tag("potencia")
                potencia_reativa_tag["tipo"] = "reativa"
                potencia_reativa_tag["multip"] = "k"
                potencia_reativa_tag["unid"] = "VAr"
                potencia_reativa_tag.append(str(potencia_reativa))

                tag_no.append(potencia_ativa_tag)
                tag_no.append(potencia_reativa_tag)

                tag_elementos.append(tag_no)


        # Adiciona os trechos que conectam barras e religadores. Por serem uma exceção,
        # eles necessitavam da definição dos alimentadores antes.
        for breaker in self.xml_cim.findAll("breaker"):
            barra = self.detectar_barra(breaker)
            if barra.name == "busbarsection":
                trecho = self.trechos_min.pop()
                trecho.nos.append(breaker)
                trecho.nos.append(barra)
                
                tag_elemento_trecho = xml_rnp.new_tag("elemento")
                tag_elemento_trecho["nome"] = str(trecho.find('mrid').text).strip()
                tag_elemento_trecho["tipo"] = "trecho"
                tag_n1 = xml_rnp.new_tag("n1")
                tag_n2 = xml_rnp.new_tag("n2")
                tag_condutores = xml_rnp.new_tag("condutores")
                tag_condutor = xml_rnp.new_tag("condutor")
                tag_condutor["nome"] = "CAA 266R"
                tag_condutores.append(tag_condutor)
                tag_elemento_trecho.append(tag_n1)
                tag_elemento_trecho.append(tag_n2)
                tag_elemento_trecho.append(tag_condutores)
                for alimentador in alimentadores:
                    if alimentador[0].nome == breaker.setores[0].nome or alimentador[0].nome == breaker.setores[1].nome:
                        no = alimentador[0]
                tag_no = xml_rnp.new_tag("no")
                tag_no["nome"] = no.nome
                tag_n1.append(tag_no)
                tag_chave = xml_rnp.new_tag("chave")
                tag_chave["nome"] = str(breaker.find('mrid').text).strip()
                tag_n2.append(tag_chave)
                tag_topologia.append(tag_elemento_trecho)





        for alimentador in alimentadores:

            lista_duplas = []
            for breaker in self.xml_cim.findAll('breaker'):
                estado = str(breaker.find('normalopen').text)[3]
                if estado == '0':
                    lista_duplas.append(breaker.setores)

            trechos = []
            breakers = []
            breakers_remova = []
            tag_elemento_alimentador = xml_rnp.new_tag("elemento")
            tag_elemento_trechos = xml_rnp.new_tag("trechos")
            tag_elemento_chaves = xml_rnp.new_tag("chaves")
            tag_elemento_raiz = xml_rnp.new_tag("raiz")
            tag_elemento_alimentador["tipo"] = "alimentador"
            tag_elemento_alimentador["nome"] = str(id(alimentador))
            tag_setores = xml_rnp.new_tag("setores")
            tag_elemento_alimentador.append(tag_setores)
            tag_elemento_alimentador.append(tag_elemento_trechos)
            tag_elemento_alimentador.append(tag_elemento_chaves)
            tag_elemento_alimentador.append(tag_elemento_raiz)
            tag_setor_raiz = xml_rnp.new_tag("setor")
            tag_elemento_raiz.append(tag_setor_raiz)
            tag_setor_raiz["nome"] = str(alimentador[0].nome)
            for setor in alimentador:
                tag_setor = xml_rnp.new_tag("setor")
                tag_setores.append(tag_setor)
                tag_setor["nome"] = setor.nome

                breakers = breakers + list(setor.breakers)

                for trecho in self.xml_cim.findAll("conductor"):
                    for no in trecho.nos:
                        if no.name == "breaker":
                            estado = str(no.find('normalopen').text)[3]
                                
                            for setor2 in no.setores:
                                if setor2.nome == setor.nome and estado == '0' and setor2.nome != alimentador[0].nome:
                                    
                                    trechos.append(trecho)

                        if no.name == "energyconsumer":
                            if no.setor.nome == setor.nome:
                                trechos.append(trecho)

                        # if no.name == "busbarsection":
                        #     trechos.append(trecho)
            trechos = set(trechos)

            #breakers = set(breakers)
                # for breaker in breakers:
                #     for alimentador2 in alimentadores:
                #         if alimentador2 == alimentador:
                #             continue
                #         else:
                #             for setor_aux in breaker.setores:
                #                 if self.pertence_a_lista(alimentador2, setor_aux):
                #                     breakers.remove(breaker)
                # print "breakeRS ALHEIOS"
                # print len(breakers_remova)
                # if len(breakers_remova) != 1:
                #     for breaker in breakers_remova:
                #         breakers.remove(breaker)
            
            for breaker in breakers:
                trigger = 0

                for alimentador2 in alimentadores:
                    if alimentador2 == alimentador:
                        continue
                    else:
                        for setor in alimentador2:
                            if breaker.setores[0] == setor or breaker.setores[1] == setor:
                                trigger += 1
                                if trigger > 1:

                                    breakers_remova.append(breaker)
                                    trigger = 0


            for breaker in breakers_remova:
                if self.pertence_a_lista(breakers, breaker):
                    breakers.remove(breaker)
            breakers = set(breakers)
            for breaker in breakers:
                tag_elemento_chave = xml_rnp.new_tag("chave")
                tag_elemento_chave["nome"] = str(breaker.find('mrid').text).strip()
                tag_elemento_chaves.append(tag_elemento_chave)
                
            
            for trecho in trechos:
                tag_elemento_trecho = xml_rnp.new_tag("trecho")
                tag_elemento_trecho["nome"] = str(trecho.find('mrid').text).strip()
                tag_elemento_trechos.append(tag_elemento_trecho)



            subestacoes = []
            tag_topologia.append(tag_elemento_alimentador)
        lista_auxiliar = list(alimentadores)
        lista_auxiliar_remova = []
        lista_subestacoes = []
        for substation in self.xml_cim.findAll('substation'):
            lista_subestacoes.append(substation)

        #RESOLVENDO DUPLICAÇÃO DE SUBESTACOES
        for alimentador in alimentadores:
            alimentador[0].usado = False
        for alimentador in alimentadores:
            dupla = []
            al = lista_auxiliar.pop(0)
            if al[0].usado:
                pass
            else:
                dupla.append(al)
                al[0].usado = True
            for alimentador2 in lista_auxiliar:
                if alimentador2[0].nome == alimentador[0].nome:
                    dupla.append(alimentador2)
            if len(dupla) > 0:
                sub = lista_subestacoes.pop(0)
                sub.alimentadores = dupla
                subestacoes.append(sub)
        # for subestacao in subestacoes:
        #     for subestacao2 in subestacoes:
        #         if set(subestacao.alimentadores) == set(self.subestacao2.alimentadores) and subestacao != subestacao2:
        #             subestacoes_remova.append(subestacao2)

        # for subestacao in subestacos_remova:
        #     subestacoes.remove(subestacao)


        for subestacao in subestacoes:
            tag_subestacao = xml_rnp.new_tag("elemento")
            tag_subestacao["tipo"] = "subestacao"
            tag_subestacao["nome"] = str(subestacao.find('mrid').text).strip()
            tag_alimentadores = xml_rnp.new_tag("alimentadores")
            tag_subestacao.append(tag_alimentadores)
            for alimentador in subestacao.alimentadores:
                tag_subestacao_alimentador = xml_rnp.new_tag("alimentador")
                tag_subestacao_alimentador["nome"] = str(id(alimentador))
                tag_alimentadores.append(tag_subestacao_alimentador)
            tag_transformadores = xml_rnp.new_tag("transformadores")
            tag_transformador = xml_rnp.new_tag("transformador")
            tag_transformador["nome"] = str(subestacao.find('mrid').text).strip() + "T"
            tag_transformadores.append(tag_transformador)
            tag_subestacao.append(tag_transformadores)
            tag_topologia.append(tag_subestacao)






        # k=0
        # while(k<10):
        #     for dupla in lista_duplas:
        #         print "DUPLA ROTATIVA"
        #         print dupla[0].nome
        #         print dupla[1].nome
        #         print "SETORES"
        #         for dupla2 in dupla_raiz:
        #             if dupla[0].nome == dupla2.nome and dupla[1].nome != dupla2.nome:
        #                 if self.pertence_a_lista(dupla_raiz, dupla[1])== False:
        #                     dupla_raiz.append(dupla[1])
        #                     k-=1
        #                 break

        #             if dupla[1].nome == dupla2.nome and dupla[0].nome != dupla2.nome:
        #                 if self.pertence_a_lista(dupla_raiz, dupla[0])== False:
        #                     dupla_raiz.append(dupla[0])
        #                     k-=1
        #                 break
        #     k+=1


        
        # for alimentador in alimentadores:
        #     print "SETORES POR ALIMENTADOR"
        #     for setor in alimentador:
        #         print setor.nome
        #     for setor in alimentador[0].setores:
        #         print setor.nome


            #self.obter_vizinhos(breaker
       
                        
        



        

        self.xml_final = xml_rnp
        print cim_path
        path = cim_path[0:len(cim_path)-3] + 'RNP'
        print path
        self.save_file(path)



    def definir_alimentadores(self):

        lista_duplas = []
        duplas_raiz = []
        alimentadores = []
        for breaker in self.xml_cim.findAll('breaker'):
            estado = str(breaker.find('normalopen').text)[3]
            if self.detectar_barra(breaker).name == "busbarsection":
                duplas_raiz = breaker.setores
                alimentadores.append(duplas_raiz)
            elif estado == '0':
                lista_duplas.append(breaker.setores)
             

        for alimentador in alimentadores:
            for setor in alimentador:
                if setor == alimentador[0]:
                    continue
                setor_raiz = setor
            fim = False
            lista_achados =[]
            while (fim is False):

                for dupla in lista_duplas:
                    if setor_raiz.nome == dupla[0].nome:
                        if self.pertence_a_lista(alimentador, dupla[1]) == False:
                            alimentador.append(dupla[1])
                            lista_achados.append(dupla[1])
                            continue
                    if setor_raiz.nome == dupla[1].nome:
                        if self.pertence_a_lista(alimentador, dupla[0]) == False:
                            alimentador.append(dupla[0])
                            lista_achados.append(dupla[0])
                            continue
                if len(lista_achados) > 0:
                    
                    setor_raiz = lista_achados.pop(0)
                else:
                    fim = True
        return alimentadores


    def detectar_barra(self, breaker):
        for terminal in breaker.findAll('terminal'):
            noconectivo = self.achar_terminal_noc(terminal)
            
            for terminal2 in noconectivo.findAll('terminal'):
                if terminal2.find('mrid').text != terminal.find('mrid').text:
                    parent = self.achar_parent(terminal2)
                else:
                    continue
                if parent.name == "conductor":
                    terminal_final = [terminal_cond for terminal_cond in parent.findAll('terminal') if terminal_cond.find('mrid') != terminal2.find('mrid')][0]
                    noconectivo_final = self.achar_terminal_noc(terminal_final)
                    for terminal_final2 in noconectivo_final.findAll("terminal"):
                        if terminal_final2.find('mrid') != terminal_final.find('mrid'):
                            parent_final = self.achar_parent(terminal_final2)
                if parent.name == "busbarsection":
                    return parent

                        # if parent_final.name == "busbarsection":
                        #     return parent_final
        return breaker
                        
        # print "Vizinhos de " + str(breaker.find('mrid'))
        # print len(vizinhos)
        # for vizinho in vizinhos:
        #     print str(vizinho.find('mrid'))





    def no_percorrido(self, no):
        for item in self.nos_percorridos:
            if no == item:
                return True
        return False

    def pertence_a_lista(self, lista, item):
        for elemento in lista:
            if elemento == item:
                return True
        return False

    def religador_usado(self, religador):
        for item in self.lista_religadores_usados:
            if religador == item:
                return True
        return False

    def no_raiz(self, no):
        for item in self.nos_raiz:
            if no == item:
                return True
        return False

    def no_setor(self, no, setor):
        if setor.nos == []:
            return False
        for item in setor.nos:
            if no == item:
                return True
        return False

    def achar_terminal_noc(self, terminal):
        lista = []
        for noc in self.lista_nosconect:
            lista_terminais = noc.findAll('terminal')
            for elemento in lista_terminais:
                if elemento.find('mrid') == terminal.find('mrid'):
                    no_achado = noc
                    return no_achado

    def achar_parent(self, terminal):
        for item in self.lista_terminais:
            if terminal.find('mrid') == item.find('mrid') and item.parent.name != 'connectivitynode':
                parent = item.parent
                return parent

    def is_vizinho(self, no, no_vizinho):
        for item in no.vizinhos:
            if item == no_vizinho:
                return True
        return False

    def is_chave(self, no, chave):
        for item in no.chaves:
            if item == chave:
                return True
        return False

    def is_lista_barras(self, barra):
        for item in self.lista_barras:
            if item == barra:
                return True
        return False

    def setor_pertence(self, breaker, setor):
        for item in breaker.setores:
            if item == setor:
                return True
        return False

    def trecho_pertence(self, trecho, no):
        for item in trecho.nos:


            if item == no:
                return True
        return False

    def no_de_breaker(self, breaker, no):
        for elemento in breaker.nos:
            if elemento == no:
                return True
        return False

    def definir_vizinhos(self, no, mode = 0):
         # Começar um caminho a partir de uma barra
        no_original = no
        no_raiz_encontrado = False
        no_rot = no
        no_original.vizinhos = []
        no_original.chaves = []
        fim = False
        terminal_counter = 0

        for item in self.xml_cim.findAll('energyconsumer'):
            item.counter = 0
            count = 0
            for item2 in item.findAll('terminal'):
                count += 1
            item.number = count

        for item in self.xml_cim.findAll('busbarsection'):
            item.counter = 0
            count = 0
            for item2 in item.findAll('terminal'):
                count += 1
            item.number = count
        count = 0
        # reset_counter = 0
        
        reset_counter = 0
        while terminal_counter < no_original.number:
            #if no_rot.name == "energyconsumer":
            if no_rot.name == "breaker":
                terminal_counter += 1
            # Loop geral: Varre todos os terminais do nó
            lista_base = no_rot.findAll('terminal')
            for terminal in lista_base:
                count = count + 1

                # Chama a função que acha o nó conectivo a que este terminal está associado
                no_conectivo = self.achar_terminal_noc(terminal)
                # Lista todos os terminais que o nó conectivo achado possui
                lista_conexoes = no_conectivo.findAll('terminal')
                # Loop interno: varre todos os terminais do referido nó conectivo, excetuando
                # o próprio terminal analisado, obviamente. Ou seja, o objetivo é descobrir com
                # que terminais o terminal em questão se conecta.
                

                for conexao in lista_conexoes:
                    if conexao.find('mrid') != terminal.find('mrid'):
                        # print conexao
                        # Chama a função que acha a que tipo de nó pertence o terminal conectado
                        # e.g Religador, Barra, Nó de Carga.
                        parent_conexao = self.achar_parent(conexao)
                        # print parent_conexao
                        # Analisa os casos possíveis

                        # if parent_conexao.name == 'breaker':
                        #     setores.append(setor)
                        #     setor = Setor()

                        # Se o item conectado ao nó raiz for um condutor, obviamente existe um nó
                        # em seguida. Precisa-se achar e identificar este nó.
                        if parent_conexao.name == 'conductor':
                        # Varre todos os terminais (2) do condutor, excetuando-se o próprio terminal
                        # analisado (primeiro extremo do condutor). O objetivo é encontrar o terminal
                        # referente ao segundo extremo do condutor.
                            for no in parent_conexao.findAll('terminal'):
                                
                                if no.find('mrid') != conexao.find('mrid'):
                                    # print "Terminal:"
                                    # print no
                        # Acha o nó conectivo referente a este terminal
                                    no_conectivo_2 = self.achar_terminal_noc(no)
                                    # print "No conectivo:"
                                    # print no_conectivo_2
                        # Lista todos terminais deste nó conectivo. O objetivo é encontrar qual nó
                        # está conectado na outra extremidade do condutor.
                                    lista_conexoes_2 = no_conectivo_2.findAll('terminal')
                        # Varre todos os terminais deste nó conectivo, excetuando-se o próprio terminal
                        # analisado, obviamente.
                                    for conexao2 in lista_conexoes_2:
                                        # print "Terminal do No:" + str(conexao2.find('mrid'))
                                        if conexao2.find('mrid') != no.find('mrid'):
                                            parent_conexao2 = self.achar_parent(conexao2)

                if parent_conexao.name == "substation":
                    terminal_counter += 1
                    continue
                if parent_conexao.name == "breaker":
                    if self.is_chave(no_original, parent_conexao) == False:
                        no_original.chaves.append(parent_conexao)
                        no_rot = parent_conexao
                        break
                    else:
                        continue
                if parent_conexao.name == 'busbarsection':
                    if mode == 1:
                        continue
                    no_original.vizinhos.append(parent_conexao)
                    if self.is_lista_barras(parent_conexao) == False:
                        self.lista_barras.append(parent_conexao)
                        no_rot = no_original
                        continue
                    else:
                        break
                
                if parent_conexao2.name == "breaker":
                    if no_rot.name == "breaker":
                        continue
                    if self.is_chave(no_original, parent_conexao2) == True:
                        continue
                    else:
                        no_original.chaves.append(parent_conexao2)
                        no_rot = parent_conexao2
                        break
                
                if parent_conexao2.name == "energyconsumer":
                    if no_rot.name == "breaker":
                        if parent_conexao2 == no_original:                            
                            continue
                        else:
                            if no_rot.name == "breaker":
                                if self.no_de_breaker(no_rot, no_original) == False:
                                    no_rot.nos.append(no_original)
                                if self.no_de_breaker(no_rot, parent_conexao2) == False:
                                    no_rot.nos.append(parent_conexao2)
                            no_original.vizinhos.append(parent_conexao2)
                            no_rot = no_original
                            break

                    if no_rot.name == "energyconsumer":
                        if parent_conexao2 == no_rot:
                            continue
                        if self.is_vizinho(no_original, parent_conexao2) == False:
                            no_original.vizinhos.append(parent_conexao2)
                            terminal_counter += 1
        return (no_original.vizinhos, no_original.chaves)

    def definir_setores(self):

        for terminal in self.lista_terminais:
            terminal.marcado = False
        for item in self.xml_cim.findAll('breaker'):
            item.setores = []
            item.counter = 0
            count = 0
            for item2 in item.findAll('terminal'):
                count += 1
            item.number = count
        for item in self.xml_cim.findAll('busbarsection'):
            item.counter = 0
            count = 0
            for item2 in item.findAll('terminal'):
                count += 1
            item.number = count
        for item in self.xml_cim.findAll('energyconsumer'):
            item.counter = 0
            count = 0
            for item2 in item.findAll('terminal'):
                count += 1
            item.number = count

        
        
        
        # Começar um caminho a partir de uma barra
        count = 0
        setores = []
        fim = False
        no_raiz_encontrado = False
        self.nos_percorridos = []
        self.nos_raiz = []

        for noconec in self.lista_nosconect:
            lista_terminais_noc = noconec.findAll('terminal')
            for terminal in lista_terminais_noc:
                parent = self.achar_parent(terminal)
                if parent.name == 'busbarsection':
                    no_raiz_encontrado = True
                    break
            for terminal in lista_terminais_noc:
                if no_raiz_encontrado:
                    parent = self.achar_parent(terminal)
                    if parent.name == 'breaker':
                        no_raiz = parent
                        break
        self.lista_religadores_nao_usados = []
        for breaker in self.xml_cim.findAll("breaker"):
            self.lista_religadores_nao_usados.append(breaker)
        self.lista_religadores_usados = []
        no_raiz_rot = no_raiz
        no_raiz_antigo = no_raiz
        setor = Setor()
        break_sign = False
        counter = 0
        # reset_counter = 0
        while fim is False:
            reset_counter = 0
            if no_raiz_rot.name == "breaker":
                self.nos_percorridos.append(no_raiz_rot)
                if self.religador_usado(no_raiz_rot) == True:                  
                    no_raiz = self.lista_religadores_nao_usados.pop(0)
                    no_raiz_rot = no_raiz
                    no_raiz_antigo = no_raiz


            if no_raiz_rot.name != "breaker":
                no_raiz_rot.counter += 1
            #print "Numero de Terminais: "
            count = 1
            # Loop geral: Varre todos os terminais do nó raiz
            for terminal in no_raiz_rot.findAll('terminal'):
                count = count + 1
                if no_raiz_rot.counter == no_raiz_rot.number:
                    no_raiz_rot = no_raiz
                    no_raiz_antigo = no_raiz
                    break

                # Chama a função que acha o nó conectivo a que este terminal está associado
                no_conectivo = self.achar_terminal_noc(terminal)
                # Lista todos os terminais que o nó conectivo achado possui
                lista_conexoes = no_conectivo.findAll('terminal')
                # Loop interno: varre todos os terminais do referido nó conectivo, excetuando
                # o próprio terminal analisado, obviamente. Ou seja, o objetivo é descobrir com
                # que terminais o terminal em questão se conecta.
                for conexao in lista_conexoes:
                    # parent_conexao2 = None
                    if conexao.find('mrid') != terminal.find('mrid'):
                        # print conexao
                        # Chama a função que acha a que tipo de nó pertence o terminal conectado
                        # e.g Religador, Barra, Nó de Carga.
                        parent_conexao = self.achar_parent(conexao)
                        # print parent_conexao
                        # Analisa os casos possíveis
                        if parent_conexao.name == 'busbarsection':
                            reset_counter += 1
                            break

                        # if parent_conexao.name == 'breaker':
                        #     setores.append(setor)
                        #     setor = Setor()

                        # Se o item conectado ao nó raiz for um condutor, obviamente existe um nó
                        # em seguida. Precisa-se achar e identificar este nó.
                        if parent_conexao.name == 'conductor':
                        # Varre todos os terminais (2) do condutor, excetuando-se o próprio terminal
                        # analisado (primeiro extremo do condutor). O objetivo é encontrar o terminal
                        # referente ao segundo extremo do condutor.
                            for no in parent_conexao.findAll('terminal'):
                                
                                if no.find('mrid') != conexao.find('mrid'):
                                    # print "Terminal:"
                                    # print no
                        # Acha o nó conectivo referente a este terminal
                                    no_conectivo_2 = self.achar_terminal_noc(no)
                                    # print "No conectivo:"
                                    # print no_conectivo_2
                        # Lista todos terminais deste nó conectivo. O objetivo é encontrar qual nó
                        # está conectado na outra extremidade do condutor.
                                    lista_conexoes_2 = no_conectivo_2.findAll('terminal')
                        # Varre todos os terminais deste nó conectivo, excetuando-se o próprio terminal
                        # analisado, obviamente.
                                    for conexao2 in lista_conexoes_2:
                                        # print "Terminal do No:" + str(conexao2.find('mrid'))
                                        if conexao2.find('mrid') != no.find('mrid'):
                                            parent_conexao2 = self.achar_parent(conexao2)
                else:
                    
                    if parent_conexao.name == 'conductor':
                        if self.trecho_pertence(parent_conexao, no_raiz_rot) == False:
                            parent_conexao.nos.append(no_raiz_rot)
                        if self.trecho_pertence(parent_conexao, parent_conexao2) == False:
                            parent_conexao.nos.append(parent_conexao2)
                    if parent_conexao2 == no_raiz_antigo:
                        if no_raiz_rot.counter ==  no_raiz_rot.number:
                            no_raiz_antigo = no_raiz
                            no_raiz_rot = no_raiz
                            break
                        else:
                            continue

                    if parent_conexao2.name == "energyconsumer":


                        if self.no_percorrido(parent_conexao2) == True:
                            reset_counter += 1
                            continue
                        else:
                            if self.no_setor(parent_conexao2, setor) == False:
                                setor.nos.append(parent_conexao2)
                            if self.no_raiz(parent_conexao2) == True and parent_conexao2.counter == parent_conexao2.number:
                                if no_raiz_rot == no_raiz:                                    
                                    setores.append(setor)
                                    for setor in setores:
                                        for item in setor.nos:
                                            item.setor = setor
                                    self.lista_religadores_usados.append(no_raiz)
                                    for elemento in setor.nos:
                                        self.nos_percorridos.append(elemento)
                                    setor = Setor()


                                    break
                                else:
                                    continue
                            else:
                                
                                no_raiz_antigo = no_raiz_rot
                                no_raiz_rot = parent_conexao2
                                self.nos_raiz.append(parent_conexao2)


                                break

                        # no_raiz_rot = parent_conexao2
                    elif parent_conexao2.name == "breaker":
                        if self.no_percorrido(parent_conexao2) == True:
                            break_sign = False
                            continue
                            
                        else:
                            self.nos_percorridos.append(parent_conexao2)
                            #self.lista_religadores_nao_usados.append(parent_conexao2)
                            
                            no_counter = no_raiz_rot.counter
                            no_number = no_raiz_rot.number
                            
                            if no_counter == no_number:
                                no_raiz_rot = no_raiz
                                no_raiz_antigo = no_raiz
                                break
                            else:
                                continue
                            
                            # no_raiz_rot.counter += 1
                            break
                                                        
                                                    # setores.append(setor)
                continue   

            if reset_counter == 2:
                if len(self.lista_religadores_nao_usados) > 1:
                    no_raiz = self.lista_religadores_nao_usados.pop(0)
                    no_raiz_rot = no_raiz
                    no_raiz_antigo = no_raiz
                    reset_counter = 0
                else:
                    fim = True

        counting = 0
        for item in self.nos_percorridos:
            counting += 1


        for setor in setores:
            for item in setor.nos:
                setor.nome = str(item.find('mrid').text).strip()

        return setores



            #print len(lista_conexoes)
            # print len(lista_conexoes)
            # for elemento in lista_conexoes:
            #     parent = self.achar_parent(elemento)
            #     print parent.name


    # def definir_alimentador(self, no_inicial):
    #     no = no_inicial
    #     for no2 in no.vizinhos:



    def save_file(self, path):
        f = open(path, 'w')
        f.write(self.xml_final.prettify(formatter = "xml"))

        

# bridge = Convert("/home/mateusvieira/Workspace/Valid_conversor/rede_teste_CIM")
# #print bridge.xml_final.prettify()
            

        


