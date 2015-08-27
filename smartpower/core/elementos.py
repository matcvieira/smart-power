# coding=utf-8




class Religador(object):
     def __init__(self, nome=None, rated_current=None, in_transit_time=None, breaking_capacity=None, reclose_sequences=None, estado=1):
        assert estado == 1 or estado == 0, 'O parâmetro estado deve ser um inteiro de valor 1 ou 0'
        self.normalOpen = estado
        self.ratedCurrent = rated_current
        self.inTransitTime = in_transit_time
        self.breakingCapacity = breaking_capacity
        self.recloseSequences = reclose_sequences
        self.nome = nome


class EnergyConsumer(object):
    def __init__(self, nome, pfixed = 0, qfixed = 0):
        self.id = id(self)
        self.nome = nome
        self.potencia_ativa = pfixed
        self.potencia_reativa = qfixed


class Substation(object):
    def __init__(self, nome, tensao_primario, tensao_secundario, potencia, impedancia):
        self.nome = nome
        self.tensao_primario = tensao_primario
        self.tensao_secundario = tensao_secundario
        self.potencia = potencia
        self.impedancia = impedancia
        self.alimentadores = []
        

class BusBarSection(object):
    def __init__(self,nome=None, phases = None):
        self.nome = nome
        self.phases = phases


class Condutor(object):
    def __init__(self, length, r, r0, x, x0, currentLimit):
        self.id = id(self)
        self.comprimento = length
        self.resistencia = r
        self.resistencia_zero = r0
        self.reatancia = x
        self.reatancia_zero = x0
        self.ampacidade = currentLimit

class NoConect(object):
    
    def __init__(self, terminal_list):
        super(NoConect, self).__init__()
        self.terminal_list = terminal_list
        self.backup_list = None

    def define_no(self):
        for terminal in self.terminal_list:
            terminal.no = self

class Terminal(object):
    def __init__(self, parent, connected = False):
        self.mRID = id(self)
        self.no = None
        self.connected = connected
        self.parent = parent

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def delete_from_list(self):
        if self.no != None:
            self.no.backup_list = self.no.terminal_list
            self.no.terminal_list.remove(self)
            print "remova!"
            if len(self.no.terminal_list) < 2:
                self.parent.scene().lista_no_conectivo.remove(self.no)

        
