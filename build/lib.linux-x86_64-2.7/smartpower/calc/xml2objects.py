# coding=utf-8

"""
Código para leitura de estruturas de redes elétricas no formato xml
O código em xml deve ter a seguinte estrutura:
<rede>
    <elementos>
        <chave/>...
        <no/>...
        <setor/>...
        <alimentador/>...
        <transformador/>
        <subestacao/>...
    </elementos>
    <topologia>
        <elemento tipo="chave"/>
        <elemento tipo="no"/>
        <elemento tipo="setor"/>
        <elemento tipo="alimentador"/>
        <elemento tipo="transformador">
        <elemento tipo="subestacao"/>
    </topologia>
</rede>
"""

# importaçoes necessárias
from rede import Chave, Setor, Condutor, Trecho, Alimentador, NoDeCarga, Subestacao, Transformador
from bs4 import BeautifulSoup
from util import Fasor

class Carregador(object):

    def __init__(self, path):

        # carraga o arquivo com as definições em xml
        f = open(path)

        # gera o objeto para iteração em xml do BeautifulSoup
        self.REDE = BeautifulSoup(f)

        self.ELEMENTOS = self.REDE.find_all('elementos')[0]
        self.TOPO = self.REDE.find_all('topologia')[0]


    def carregar_topologia(self):
        chaves = self._gerar_chaves()
        nos = self._gerar_nos_de_carga()
        setores = self._gerar_setores(nos)
        self._associar_chaves_aos_setores(chaves, setores)
        condutores = self._gerar_condutores()
        trechos = self._gerar_trechos(nos, chaves, condutores)
        alimentadores = self._gerar_alimentadores(setores, trechos, chaves)
        transformadores = self._gerar_transformadores()
        subestacoes = self._gerar_subestacaoes(alimentadores, transformadores)

        return {'chaves': chaves,
                'nos': nos,
                'setores': setores,
                'trechos': trechos,
                'alimentadores': alimentadores,
                'transformadores': transformadores,
                'subestacoes': subestacoes}


    def _gerar_chaves(self):
        # Busca e instanciamento dos objetos do tipo Chave
        print 'Gerando chaves...'
        chaves_xml = self.ELEMENTOS.find_all('chave')
        chaves = dict()
        for chave_tag in chaves_xml:
            if chave_tag['estado'] == 'fechado':
                chaves[chave_tag['nome']] = Chave(nome=chave_tag['nome'], estado=1)
            elif chave_tag['estado'] == 'aberto':
                chaves[chave_tag['nome']] = Chave(nome=chave_tag['nome'], estado=0)
            print 'Chave %s criada.' % chaves[chave_tag['nome']].nome

        return chaves


    def _gerar_nos_de_carga(self):
        # Busca e instanciamento dos objetos do tipo NoDeCarga
        print 'Gerando Nos de Carga...'
        nos_xml = self.ELEMENTOS.find_all('no')
        nos = dict()
        for no_tag in nos_xml:
            elemento_tag = self.TOPO.find_all('elemento', tipo='no', nome=no_tag['nome'])[0]
            #if elemento_tag is not None:
            #    elemento_tag.reverse()
            vizinhos = [no['nome'] for no in elemento_tag.vizinhos.findChildren('no')]
            vizinhos.reverse()
            chaves_do_no = [chave['nome']
                            for chave in elemento_tag.chaves.findChildren('chave')]

            potencia_ativa_tag = no_tag.find_all('potencia', tipo='ativa')[0]
            potencia_reativa_tag = no_tag.find_all('potencia', tipo='reativa')[0]
            if potencia_ativa_tag['multip'] == 'k':
                potencia_ativa = float(potencia_ativa_tag.text) * 1e3
            elif potencia_ativa_tag['multip'] == 'M':
                potencia_ativa = float(potencia_ativa_tag.text) * 1e6
            else:
                potencia_ativa = float(potencia_ativa_tag.text)

            if potencia_reativa_tag['multip'] == 'k':
                potencia_reativa = float(potencia_reativa_tag.text) * 1e3
            elif potencia_reativa_tag['multip'] == 'M':
                potencia_reativa = float(potencia_reativa_tag.text) * 1e6
            else:
                potencia_reativa = float(potencia_reativa_tag.text)

            print potencia_ativa
            print potencia_reativa
            print chaves_do_no

            nos[no_tag['nome']] = NoDeCarga(nome=no_tag['nome'],
                                            vizinhos=vizinhos,
                                            potencia=Fasor(real=potencia_ativa,
                                                           imag=potencia_reativa,
                                                           tipo=Fasor.Potencia),
                                            chaves=chaves_do_no)
            print 'NoDeCarga %s criado.' % nos[no_tag['nome']].nome
        return nos


    def _gerar_setores(self, nos):
        # Busca e instanciamento dos objetos do tipo Setor
        print 'Gerando Setores...'
        setores_xml = self.ELEMENTOS.find_all('setor')
        setores = dict()

        for setor_tag in setores_xml:
            elemento_tag = self.TOPO.find_all(
                'elemento', tipo='setor', nome=setor_tag['nome'])[0]
            vizinhos_do_setor = [setor['nome'] for setor in elemento_tag.findChildren('setor')]
            nomes_nos_do_setor = [no['nome'] for no in elemento_tag.findChildren('no')]
            nos_do_setor = [no for no in nos.values() if no.nome in nomes_nos_do_setor]
            setores[setor_tag['nome']] = Setor(nome=setor_tag['nome'],
                                               vizinhos=vizinhos_do_setor,
                                               nos_de_carga=nos_do_setor)
            print 'Setor %s criado.' % setores[setor_tag['nome']].nome
        return setores


    def _associar_chaves_aos_setores(self, chaves, setores):
        # Associação das chaves aos setores
        for chave in chaves.values():
            elemento_chave = self.TOPO.find_all('elemento', tipo='chave', nome=chave.nome)[0]
            chave.n1 = setores[elemento_chave.n1.setor['nome']]
            chave.n2 = setores[elemento_chave.n2.setor['nome']]


    def _gerar_condutores(self):
        # Busca e instanciamento dos objetos do tipo Condutor
        print 'Gerando Condutores...'
        condutores_xml = self.ELEMENTOS.find_all('condutor')
        condutores = dict()

        for condutor_tag in condutores_xml:
            condutores[condutor_tag['nome']] = Condutor(nome=condutor_tag['nome'],
                                                        rp=condutor_tag['rp'],
                                                        xp=condutor_tag['xp'],
                                                        rz=condutor_tag['rz'],
                                                        xz=condutor_tag['xz'],
                                                        ampacidade=condutor_tag['ampacidade'])
        return condutores


    def _gerar_trechos(self, nos, chaves, condutores):
        # Busca e instanciamento dos objetos do tipo Alimentador
        print 'Gerando Trechos...'
        trechos_xml = self.ELEMENTOS.find_all('trecho')
        trechos = dict()
        for trecho_tag in trechos_xml:

            elementos = self.TOPO.find_all('elemento', tipo = 'trecho', nome = trecho_tag['nome'])
            elemento_tag = elementos[0]
            if elemento_tag.n1.no is not None:
                n1 = nos[elemento_tag.n1.no['nome']]
            elif elemento_tag.n1.chave is not None:
                n1 = chaves[elemento_tag.n1.chave['nome']]

            if elemento_tag.n2.no is not None:
                n2 = nos[elemento_tag.n2.no['nome']]
            elif elemento_tag.n2.chave is not None:
                n2 = chaves[elemento_tag.n2.chave['nome']]

            comprimento_tag = trecho_tag.comprimento
            # comprimento = float(comprimento_tag.text)
            if comprimento_tag['multip'] == 'k':
                comprimento = float(comprimento_tag.text) * 1
            elif comprimento_tag['multip'] == 'M':
                comprimento = float(comprimento_tag.text) * 1
            else:
                comprimento = float(comprimento_tag.text)

            condutor = condutores[elemento_tag.condutores.condutor['nome']]

            trechos[trecho_tag['nome']] = Trecho(nome=trecho_tag['nome'],
                                                 n1=n1,
                                                 n2=n2,
                                                 condutor=condutor,
                                                 comprimento=comprimento)
        return trechos


    def _gerar_alimentadores(self, setores, trechos, chaves):
        # Busca e instanciamento dos objetos do tipo Alimentador
        print 'Gerando Alimentadores...'
        alimentadores_xml = self.ELEMENTOS.find_all('alimentador')
        alimentadores = dict()

        for alimen_tag in alimentadores_xml:
            elemento_tag = self.TOPO.find_all('elemento', tipo='alimentador', nome=alimen_tag['nome'])[0]
            nomes_dos_trechos = [trecho['nome'] for trecho in elemento_tag.trechos.findChildren('trecho')]
            nomes_dos_setores = [setor['nome'] for setor in elemento_tag.setores.findChildren('setor')]
            nomes_das_chaves = [chave['nome'] for chave in elemento_tag.chaves.findChildren('chave')]
            trechos_do_alimentador = [trecho for trecho in trechos.values() if trecho.nome in nomes_dos_trechos]
            setores_do_alimentador = [setor for setor in setores.values() if setor.nome in nomes_dos_setores]
            chaves_do_alimentador = [chave for chave in chaves.values() if chave.nome in nomes_das_chaves]
            alimentadores[alimen_tag['nome']] = Alimentador(nome=alimen_tag['nome'],
                                                            setores=setores_do_alimentador,
                                                            trechos=trechos_do_alimentador,
                                                            chaves=chaves_do_alimentador)

            print 'Ordenando alimentador...'
            print 'No Raiz: {raiz}'.format(raiz=elemento_tag.raiz.setor['nome'])

            alimentadores[alimen_tag['nome']].ordenar(raiz=elemento_tag.raiz.setor['nome'])

            alimentadores[alimen_tag['nome']].gerar_arvore_nos_de_carga()
            print 'Alimentador %s criado.' % alimentadores[alimen_tag['nome']].nome
        return alimentadores


    def _gerar_transformadores(self):
        # Busca e instanciamento dos objetos do tipo Transformador
        print 'Gerando Transformadores'
        transformadores_xml = self.ELEMENTOS.find_all('transformador')
        transformadores = dict()

        for trafo_tag in transformadores_xml:

            tensao_primario_tag = trafo_tag.find_all('enrolamento', tipo='primario')[0].tensao
            if tensao_primario_tag['multip'] == 'k':
                tensao_primario = float(tensao_primario_tag.text) * 1e3
            elif tensao_primario_tag['multip'] == 'M':
                tensao_primario = float(tensao_primario_tag.text) * 1e6
            else:
                tensao_primario = float(tensao_primario_tag.text)

            tensao_secundario_tag = trafo_tag.find_all('enrolamento', tipo='secundario')[0].tensao
            if tensao_secundario_tag['multip'] == 'k':
                tensao_secundario = float(tensao_secundario_tag.text) * 1e3
            elif tensao_secundario_tag['multip'] == 'M':
                tensao_secundario = float(tensao_secundario_tag.text) * 1e6
            else:
                tensao_secundario = float(tensao_secundario_tag.text)


            potencia_tag = trafo_tag.find_all('potencia')[0]
            if potencia_tag['multip'] == 'k':
                potencia = float(potencia_tag.text) * 1e3
            elif potencia_tag['multip'] == 'M':
                potencia = float(potencia_tag.text) * 1e6
            else:
                potencia = float(potencia_tag.text)

            impedancia_tag = trafo_tag.find_all('impedancia', tipo='seq_pos')[0]
            resistencia_tag = impedancia_tag.resistencia
            reatancia_tag = impedancia_tag.reatancia

            if resistencia_tag['multip'] == 'k':
                resistencia = float(resistencia_tag.text) * 1e3
            elif resistencia_tag['multip'] == 'M':
                resistencia = float(resistencia_tag.text) * 1e6
            else:
                resistencia = float(resistencia_tag.text)

            if reatancia_tag['multip'] == 'k':
                reatancia = float(reatancia_tag.text) * 1e3
            elif resistencia_tag['multip'] == 'M':
                reatancia = float(reatancia_tag.text) * 1e6
            else:
                reatancia = float(reatancia_tag.text)

            transformadores[trafo_tag['nome']] = Transformador(nome=trafo_tag['nome'],
                                                               tensao_primario=Fasor(mod=tensao_primario, ang=0.0,
                                                                                     tipo=Fasor.Tensao),
                                                               tensao_secundario=Fasor(mod=tensao_secundario, ang=0.0,
                                                                                       tipo=Fasor.Tensao),
                                                               potencia=Fasor(mod=potencia, ang=0.0, tipo=Fasor.Potencia),
                                                               impedancia=Fasor(real=resistencia, imag=reatancia,
                                                                                tipo=Fasor.Impedancia))
        return transformadores


    def _gerar_subestacaoes(self, alimentadores, transformadores):
        # Busca e instanciamento dos objetos do tipo Subestacao
        print 'Gerando Subestações...'
        subestacoes_xml = self.ELEMENTOS.find_all('subestacao')
        subestacoes = dict()

        for sub_tag in subestacoes_xml:
            elemento_tag = self.TOPO.find_all('elemento', tipo='subestacao', nome=sub_tag['nome'])[0]
            nomes_dos_alimentadores = [alimentador['nome'] for alimentador in
                                       elemento_tag.alimentadores.findChildren('alimentador')]

            alimentadores_da_subestacao = [alimentador for alimentador in alimentadores.values() if
                                           alimentador.nome in nomes_dos_alimentadores]

            nomes_dos_trafos = [trafo['nome'] for trafo in elemento_tag.transformadores.findChildren('transformador')]

            trafos_da_subestacao = [trafo for trafo in transformadores.values() if trafo.nome in nomes_dos_trafos]

            subestacoes[sub_tag['nome']] = Subestacao(nome=sub_tag['nome'],
                                                      alimentadores=alimentadores_da_subestacao,
                                                      transformadores=trafos_da_subestacao, 
                                                      impedancia_positiva=0.1033+0.8087j,
                                                      impedancia_zero=0+0.6365j)
            print 'Subestacao %s criada.' % subestacoes[sub_tag['nome']].nome
        return subestacoes

# if __name__ == '__main__':
#     top = carregar_topologia()
