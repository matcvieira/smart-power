# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from xml.dom import minidom


class Sector(object):
	def __init__(self, name=None):
		self.nodes = []
		self.neighbours = []
		self.name = name
		self.conductors = []

class ConnectionEvent(object):
	def __init__(self,n1=None,n2=None):
		self.occured = False
		self.pair = (n1,n2)

class Feeder(object):
	def __init__(self, sector=None, count = "", breaker0=None):
		self.root = sector
		self.name = sector.name + count
		self.sectors = []
		self.conductors = []
		self.breaker0 = breaker0
		self.breakers = []
		for sector in self.breaker0.sectors:
			self.sectors.append(sector)

	def find_conductor0(self):
		for conductor in self.conductors:
			if conductor.nodes[0] == self.breaker0 or conductor.nodes[1] == self.breaker0:
				self.conductor0 = conductor


class SpecialConductor(object):
	def __init__(self,n1=None,n2=None):
		self.nodes = [n1,n2]
		self.mrid = str(n1.find('mrid').text).strip() + str(n2.find('mrid').text).strip()
		self.sector = n1.sector


class ReadCIM(object):

	def __init__(self,file="/home/mateusvieira/Dropbox/GREI - Workspace/Test 001/rede_adaptada_CIM"):
		if file is None:
			return "No CIM File entered"
		else:
			self.cim_file = BeautifulSoup(open(file))
			# Leitura de todos os elementos do arquivo CIM
			# Obtenção de todos os religadores
			self.breaker_list = self.cim_file.findAll("breaker")
			#Obtenção de todos os nós de carga
			self.consumer_list = self.cim_file.findAll("energyconsumer")
			#Obtenção de todos os trechos
			self.conductor_list = self.cim_file.findAll("conductor")
			#Obtenção de todos os nós conectivos
			self.connode_list = self.cim_file.findAll("connectivitynode")
			#Obtenção de todas as barras
			self.busbar_list = self.cim_file.findAll("busbarsection")
			#Obtenção de todos os terminais
			self.terminal_list = self.cim_file.findAll("terminal")
			#Obtenção de todas as subestações
			self.substation_list = self.cim_file.findAll("substation")

			#Definir nomes dos setores
			self.name_sectors()

			self.define_busbar_neighbours()

			# Cria listas de nós para cada conductor
			for conductor in self.conductor_list:
				conductor.nodes = []
				conductor.n1 = None
				conductor.n2 = None

			# Cria listas para cada breaker receber teus nodes
			for breaker in self.breaker_list:
				breaker.nodes = []
				breaker.sectors = []
			# Definir vizinhos e chaves dos nós de carga
			print "Defining consumers neighbours and breakers..."
			for consumer in self.consumer_list:
				consumer.sector = None
				consumer.im_neighbours =[]
				self.define_node_neighbours(consumer)
				print ("Vizinhos de " + self.get_mrid(consumer) + ": " +
				str(self.get_mrid_list(consumer.neighbours)) + "    [" +
				str(self.consumer_list.index(consumer)) + "]")
				print ("Chaves de " + self.get_mrid(consumer) + ": " +
				str(self.get_mrid_list(consumer.switches)))

			print "Double checking consumers neighbours..."
			for consumer in self.consumer_list:
				consumer.im_neighbours = sorted(list(set(consumer.im_neighbours)))
				print "Consumer: " + str(consumer.find("mrid").text).strip()
				print "    Vizinhos:"
				for neighbour in consumer.neighbours:
					print "        " + str(neighbour.find("mrid").text).strip()
			raw_input("next step press enter")  

			print "Double checking breakers nodes..."
			for breaker in self.breaker_list:
				print ("Nós de " + self.get_mrid(breaker) + ": " +
					str(self.get_mrid_list(breaker.nodes)))
	
			print "Defining sectors..."
			self.sectors = self.define_sectors()

			print "Double checking consumers sectors..."
			for consumer in self.consumer_list:
				print "Consumer: " + str(consumer.find("mrid").text).strip()
				print "    Sector: " + consumer.sector.name

			print "Double checking sectors nodes..."
			for sector in self.sectors:
				print "Sector: " + sector.name
				for node in sector.nodes:
					print "   Node: " + self.get_mrid(node)

			print "Double checking busbar neighbours..."
			for busbar in self.busbar_list:
				print "Busbar: " + self.get_mrid(busbar)
				for neighbour in busbar.neighbours:
					print "    Neighbour: " + self.get_mrid(neighbour)

			print "Cleaning conductors nodes lists and creating specials..."
			self.define_special_conductors()
			self.clean_conductors_nodes()
			for conductor in self.special_conductors:
				print "Special Conductor: " + conductor.mrid
				for node in conductor.nodes:
					print "    Node: " + self.get_mrid(node)
					print "    Sector: " + conductor.sector.name

			print "Defining conductors sectors..."
			self.define_edges_sectors()
			
			for conductor in self.conductor_list:
				if isinstance(conductor,SpecialConductor):
					name = conductor.mrid
				else:
					name = self.get_mrid(conductor)
				print "Conductor: " + name
				print "Sector: " + conductor.sector.name
				for node in conductor.nodes:
					print "    Node: " + self.get_mrid(node)


			print "Checking breakers sectors..."
			self.define_breaker_sectors()
			for breaker in self.breaker_list:
				print "Breaker:" + self.get_mrid(breaker)
				for sector in breaker.sectors:
					print "    Sector:" + sector.name
			print "Defining sectors neighbours..."
			self.define_sectors_neighbours()

			print "Final check on sectors data..."
			for sector in self.sectors:
				print "Sector "+ sector.name
				print "    Nodes:"
				for node in sector.nodes:
					print "        " + str(node.find('mrid').text).strip()
				print "    Neighbours:"
				for neighbour in sector.neighbours:
					print "        " + neighbour.name
				print "    Conductors:"
				for conductor in sector.conductors:
					if isinstance(conductor,SpecialConductor):
						print conductor.mrid
					else:
						print "        " + self.get_mrid(conductor)

			print "Defining Feeders..."
			self.define_feeders()

			print "Organizing Breakers..."
			self.organize_breakers()

			print "Organizing Conductors..."
			self.organize_conductors()

			print "Writing xml..."
			self.write_xml()


	def define_edges_sectors(self):
		for conductor in self.conductor_list:
			if isinstance(conductor,SpecialConductor) == False:
				for node in conductor.nodes:
					if node.name == "energyconsumer":
						conductor.sector = node.sector
						conductor.sector.conductors.append(conductor)
			else:
				conductor.sector.conductors.append(conductor)

		for sector in self.sectors:
			sector.conductors = sorted(list(set(sector.conductors)))

	def define_breaker_sectors(self):
		for breaker in self.breaker_list:
			for node in breaker.nodes:
				breaker.sectors.append(node.sector)


	def name_sectors(self):
		sectors = []
		for consumer in self.consumer_list:
			consumer_name = str(consumer.find('mrid').text).strip()
			letter = consumer_name[0]
			sectors.append(letter)
		for bus in self.busbar_list:
			bus_name = str(bus.find('mrid').text).strip()
			sectors.append(bus_name)
		sectors = list(set(sectors))
		sectors = sorted(sectors)
		print sectors
		return sectors


	def define_node_neighbours(self,consumer=None):
		'''
		Função que define os vizinhos de um dado nó de carga
		'''
		# Cria lista que irá receber a lista de vizinhos
		consumer.neighbours = []
		consumer.switches = []

		# Obtém nome do nó de carga
		consumer_name = str(consumer.find('mrid').text).strip()
		print "Definindo Vizinhos para " + consumer_name + "..."

		# Varredura nos terminais deste nó de carga
		for terminal in consumer.findAll("terminal"):
			terminal_name = terminal.find('mrid')
			# Chama função que encontra o vizinho imediato (e.g um condutor) do nó de carga
			im_neighbour_info = self.find_im_neighbour(terminal_name)
			if im_neighbour_info is None:
				continue
			im_neighbour = im_neighbour_info[0]
			im_neighbour_terminal = im_neighbour_info[1]
			print "Vizinho Imediato encontrado: " + im_neighbour.name + " " + self.get_mrid(im_neighbour)
			conductor = None
			if im_neighbour.name == "conductor":
				conductor = im_neighbour
				neighbour_info = self.find_connected(im_neighbour,im_neighbour_terminal)
				neighbour = neighbour_info[0]
				neighbour_terminal = neighbour_info[1]
				consumer.im_neighbours.append(neighbour)
				conductor.nodes.append(neighbour)
				conductor.nodes.append(consumer)
				if neighbour.name == "breaker":
					# Define breaker como chave do nó de carga
					consumer.switches.append(neighbour)
					neighbour.nodes.append(consumer)
					connection_info = self.find_connected(neighbour,neighbour_terminal)
					connection = connection_info[0]
					connection_terminal = connection_info[1]
					if connection.name == "busbarsection":
						connection.neighbours.append(consumer)
						connection.breakers.append(neighbour)
						neighbour.nodes.append(connection)
						neighbour_info = connection_info
					else:
						neighbour_info = self.find_connected(connection,connection_terminal)
					neighbour = neighbour_info[0]
					neighbour_terminal = neighbour_info[1]
					print "Vizinho encontrado: " + neighbour.name + " " + self.get_mrid(neighbour)
					consumer.neighbours.append(neighbour)
					continue
				if neighbour.name == "energyconsumer" or neighbour.name == "busbarsection":
					print "Vizinho encontrado: " + neighbour.name + " " + self.get_mrid(neighbour)
					consumer.neighbours.append(neighbour)

	
	def define_feeders(self):
		sectors0 = []
		self.feeders = []
		for sector in self.sectors:
			for node in sector.nodes:
				if node.name == "busbarsection":
					sectors0.append(sector)

		for sector in sectors0:
			i = 1
			for neighbour in sector.neighbours:
				for breaker in self.breaker_list:
					if (breaker.sectors[0] == sector and breaker.sectors[1] == neighbour) or (breaker.sectors[0] == neighbour and breaker.sectors[1] == sector):
						breaker0 = breaker
				feeder = Feeder(sector,"_AL" + str(i),breaker0)
				self.feeders.append(feeder)
				i += 1

		closed_breakers = []
		for breaker in self.breaker_list:
			if self.get_value(breaker,"normalopen") == "0":
				closed_breakers.append(breaker)
				print self.get_mrid(breaker)

		breakers0 =[]
		for breaker in self.breaker_list:
			for node in breaker.nodes:
				if node.name == "busbarsection":
					breakers0.append(breaker)



		for feeder in self.feeders:
			go = True
			print "Defining parameters for feeder: " + feeder.name + "..."
			print "Breaker 0: " + self.get_mrid(feeder.breaker0)

			while go is True:
				print "start"

				add_sector = False
				for closed_breaker in closed_breakers:
					print "Closed Breaker: " + self.get_mrid(closed_breaker)
					if closed_breaker in breakers0:
						print "Breaker 0: do not add"
						continue
					for sector in closed_breaker.sectors:
						if sector in feeder.sectors:
							add_sector = True

					if add_sector is True:
						for sector in closed_breaker.sectors:
							if sector in feeder.sectors:
								continue
							else:
								feeder.sectors.append(sector)
								feeder.breakers.append(closed_breaker)
								closed_breakers.remove(closed_breaker)
								break
						else:
							continue
						break
				else:
					go = False

		for feeder in self.feeders:
			for sector in feeder.sectors:
				for conductor in sector.conductors:
					feeder.conductors.append(conductor)


		for feeder in self.feeders:
			print "Feeder: " + feeder.name
			for sector in feeder.sectors:
				print "    Sector: " + sector.name
			for conductor in feeder.conductors:
				if isinstance(conductor,SpecialConductor):
					print conductor.mrid
				else:
					print "    Conductor: " + self.get_mrid(conductor)
			for breaker in feeder.breakers:
				print "    Breaker: " + self.get_mrid(breaker)

	def organize_breakers(self):
		for feeder in self.feeders:
			sector0 = feeder.root
			breaker0 = feeder.breaker0
			breaker0.n1 = sector0
			if breaker0.sectors[0] == sector0:
				breaker0.n2 = breaker0.sectors[1]
			else:
				breaker0.n2 = breaker0.sectors[0]
			found_breakers = []
			while len(found_breakers) < len(feeder.breakers):
				for breaker in feeder.breakers:
					if breaker.sectors[0] in breaker0.sectors:
						breaker.n1 = breaker.sectors[0]
						breaker.n2 = breaker.sectors[1]
						breaker0 = breaker
						found_breakers.append(breaker)
					elif breaker.sectors[1] in breaker0.sectors:
						breaker.n1 = breaker.sectors[1]
						breaker.n2 = breaker.sectors[0]
						breaker0 = breaker
						found_breakers.append(breaker)

			print "Feeder: " + feeder.name
			print "    Root Breaker: " + self.get_mrid(feeder.breaker0)
			print "        n1: " + feeder.breaker0.n1.name
			print "        n2: " + feeder.breaker0.n2.name
			for breaker in feeder.breakers:
				print "    Breaker: " + self.get_mrid(breaker)
				print "        n1: " + breaker.n1.name
				print "        n2: " + breaker.n2.name

	def organize_conductors(self):
		for feeder in self.feeders:
			print feeder.name
			feeder.find_conductor0()
			if isinstance(feeder.conductor0,SpecialConductor):
				print feeder.conductor0.mrid
			else:
				print self.get_mrid(feeder.conductor0)
			conductor0 = feeder.conductor0
			conductor0.n1 = conductor0.nodes[0]
			conductor0.n2 = conductor0.nodes[1]
			found_conductors = []
			pending_conductors = []
			done = True
			while done is True:
				if isinstance(conductor0,SpecialConductor):
					print "Conductor 0: " + conductor0.mrid
				else:
					print "Conductor0: " + self.get_mrid(conductor0)
				for conductor in feeder.conductors:
					if isinstance(conductor,SpecialConductor) or conductor==conductor0:
						continue
					print "     compare to: "+ self.get_mrid(conductor)
					if conductor.nodes[0] in conductor0.nodes:
						if conductor.n1 is None:
							conductor.n1 = conductor.nodes[0]
						if conductor.n2 is None:
							conductor.n2 = conductor.nodes[1]
						if conductor not in found_conductors:
							pending_conductors.append(conductor)
						found_conductors.append(conductor)
						print "Found next conductor: " + self.get_mrid(conductor)
					elif conductor.nodes[1] in conductor0.nodes:
						if conductor.n1 is None:
							conductor.n1 = conductor.nodes[1]
						if conductor.n2 is None:
							conductor.n2 = conductor.nodes[0]
						if conductor not in found_conductors:
							pending_conductors.append(conductor)
						found_conductors.append(conductor)
						print "Found next conductor: " + self.get_mrid(conductor)
				conductor0 = pending_conductors.pop()
				for conductor in feeder.conductors:
					if isinstance(conductor,SpecialConductor):
						continue
					if conductor.n1 is None or conductor.n2 is None:
						break
				else:
					done = False


			print "Feeder: " + feeder.name
			print "    Root Conductor:  " + feeder.conductor0.mrid
			print "        n1: " + self.get_mrid(feeder.conductor0.n1)
			print "        n2: " + self.get_mrid(feeder.conductor0.n2)
			for conductor in feeder.conductors:
				if isinstance(conductor,SpecialConductor):
					continue
				print "    Conductor: " + self.get_mrid(conductor)
				print "        n1: " + self.get_mrid(conductor.n1)
				print "        n2: " + self.get_mrid(conductor.n2)





				




	def check_connection(self,n1=None,n2=None,lista=None):
		for connection in lista:
			if (n1,n2) == connection.pair:
				break
		else:
			return True
		return False




	
	def define_special_conductors(self):
		self.special_conductors = []
		for busbar in self.busbar_list:
			for breaker in busbar.breakers:
				cond = SpecialConductor(busbar, breaker)
				self.special_conductors.append(cond)

	def define_busbar_neighbours(self):
		for busbar in self.busbar_list:
			busbar.neighbours = []
			busbar.breakers = []

	def clean_conductors_nodes(self):
		to_remove = []
		for conductor in self.conductor_list:
			print self.get_mrid(conductor)
			if conductor.nodes == []:
				to_remove.append(conductor)
			else:
				conductor.nodes = sorted(list(set(conductor.nodes)))

		for conductor in to_remove:
			self.conductor_list.remove(conductor)
		for conductor in self.special_conductors:
			self.conductor_list.append(conductor)



	def define_sectors(self):
		'''
		Função que encontra setores 
		'''
		sectors = []
		for consumer in self.consumer_list:
			for neighbour in consumer.im_neighbours:
				if neighbour.name == "energyconsumer":
					if self.has_sector(neighbour):
						if self.has_sector(consumer):
							pass
						else:
							consumer.sector = neighbour.sector
							consumer.sector.nodes.append(neighbour)
					elif self.has_sector(consumer):
						pass
					else:
						sector = Sector(str(consumer.find('mrid').text).strip()[0])
						consumer.sector = sector
					neighbour.sector = consumer.sector
					neighbour.sector.nodes.append(neighbour)
			sectors.append(sector)
		sectors = sorted(list(set(sectors)))

		for busbar in self.busbar_list:
			sector = Sector(str(busbar.find('mrid').text).strip())
			sector.nodes.append(busbar)
			busbar.sector = sector
			sectors.append(sector)
		for sector in sectors:
			sector.nodes = sorted(list(set(sector.nodes)))

		return sorted(list(set(sectors)))

		# for consumer in self.consumer_list:
		#     if str(consumer.find('mrid').text).strip()[0] == "E":
		#         print str(consumer.find('mrid').text).strip()
		#         for neighbour in consumer.im_neighbours:
		#             print "         " + str(neighbour.find('mrid').text).strip()


	def define_sectors_neighbours(self):
		for sector in self.sectors:
			for node in sector.nodes:
				for neighbour in node.neighbours:
					if neighbour.name == "energyconsumer" or neighbour.name == "busbarsection":
						if neighbour.sector == sector:
							pass
						else:
							sector.neighbours.append(neighbour.sector)
		return


	def has_sector(self, consumer=None):
		if consumer.sector is None:
			return False
		else:
			return True
	def find_im_neighbour(self,terminal_name=None):
		'''
		Função que encontra vizinho imediato de um elemento, passado seu terminal.
		'''
		connode_found = None
		# Procura a qual nó conectivo o terminal faz parte
		for connode in self.connode_list:
			for terminal in connode.findAll("terminal"):
				if terminal.find('mrid') == terminal_name:
					connode_found = connode
					# print "Connectivity Node found!"
					break
			if connode_found is not None:
				break
		else:
			print "Terminal not found!"
			return None

		# Chama função que encontra o terminal ligado a este.
		parent_terminal = self.find_other_terminal(connode_found,terminal_name)
		# Chama a função que encontra parent deste terminal, ou seja, o vizinho imediato.
		parent = self.find_parent(parent_terminal)
		return parent


	def find_other_terminal(self,connode,terminal_name):
		'''
		Função que encontra o segundo terminal de um nó conectivo, passado o primeiro terminal.
		'''
		for connode_terminal in connode.findAll("terminal"):
			connode_terminal_name = connode_terminal.find('mrid')
			if connode_terminal_name == terminal_name:
				pass
			else:
				return connode_terminal

	def find_parent(self, parent_terminal=None):
		'''
		Função que encontra parent de terminal passado.
		'''
		for terminal in self.terminal_list:
			if terminal.parent.name == "connectivitynode":
				pass
			elif terminal.find('mrid')==parent_terminal.find('mrid'):
				return [terminal.parent,parent_terminal]

	def find_connected(self,conductor=None,conductor_terminal=None):
		for terminal in conductor.findAll("terminal"):
			terminal_name = terminal.find('mrid')
			conductor_terminal_name = conductor_terminal.find('mrid')
			if terminal_name == conductor_terminal_name:
				pass
			else:
				connected = self.find_im_neighbour(terminal_name)
				return connected

	def get_mrid(self,element=None):
		return str(element.find('mrid').text).strip()

	def get_value(self,element=None,value=None):
		return str(element.find(value).text).strip()

	def get_mrid_list(self,element_list=None):
		mrid_list = []
		for element in element_list:
			mrid_list.append(str(element.find('mrid').text).strip())
		return mrid_list

	# def build_feeders:


	def write_xml(self,file="/home/mateusvieira/Dropbox/GREI - Workspace/Test 001/rede_adaptada_RNP.xml"):
		rnp = BeautifulSoup()
		tag_rede = rnp.new_tag("rede")
		tag_elementos = rnp.new_tag("elementos")
		tag_topologia = rnp.new_tag("topologia")
		tag_rede.append(tag_elementos)
		tag_rede.append(tag_topologia)
		rnp.append(tag_rede)

		# INSERÇÃO DE ELEMENTOS

		for breaker in self.breaker_list:
			mrid = self.get_mrid(breaker)
			estado = self.get_value(breaker,"normalopen")
			if estado == "1":
				estado = "aberto"
			else:
				estado = "fechado"
			tag_chave = rnp.new_tag("chave")
			tag_chave["nome"] = mrid
			tag_chave["estado"] = estado
			tag_elementos.append(tag_chave)

		for consumer in self.consumer_list:
			tag_consumer = rnp.new_tag("no")
			mrid = self.get_mrid(consumer)
			potencia_ativa = self.get_value(consumer,"pfixed")
			potencia_reativa = self.get_value(consumer,"qfixed")

			tag_consumer["nome"] = mrid

			tag_pativa = rnp.new_tag("potencia")
			tag_pativa["tipo"] = "ativa"
			tag_pativa["multip"] = "k"
			tag_pativa["unid"] = "W"
			tag_pativa.append(potencia_ativa)

			tag_preativa = rnp.new_tag("potencia")
			tag_preativa["tipo"] = "reativa"
			tag_preativa["multip"] = "k"
			tag_preativa["unid"] = "VAr"
			tag_preativa.append(potencia_reativa)

			tag_consumer.append(tag_pativa)
			tag_consumer.append(tag_preativa)

			tag_elementos.append(tag_consumer)

		for trecho in self.conductor_list:
			tag_trecho = rnp.new_tag("trecho")
			if isinstance(trecho,SpecialConductor):
				mrid = trecho.mrid
				length = "0.01"
			else:
				mrid = self.get_mrid(trecho)
				length = self.get_value(trecho,"length")

			tag_trecho["nome"] = mrid

			tag_length = rnp.new_tag("comprimento")
			tag_length["multip"] = "k"
			tag_length["unid"] = "m"
			tag_length.append(length)

			tag_trecho.append(tag_length)

			tag_elementos.append(tag_trecho)

		tag_condutor = rnp.new_tag("condutor")
		tag_condutor["nome"] = "CAA 266R"
		tag_condutor["rp"] = "0.2391"
		tag_condutor["xp"] = "0.37895"
		tag_condutor["rz"] = "0.41693"
		tag_condutor["xz"] = "1.55591"
		tag_condutor["ampacidade"] = "301"
		tag_elementos.append(tag_condutor)

		for setor in self.sectors:
			tag_setor = rnp.new_tag("setor")
			tag_setor["nome"] = setor.name
			tag_elementos.append(tag_setor)

		# for alimentador in self.feeder_list:
		#     tag_feeder = rnp.new_tag("alimentador")
		#     tag_feeder["nome"] = alimentador
		#     tag_elementos.append(tag_feeder)

		for subestacao in self.substation_list:
			tag_subestacao = rnp.new_tag("subestacao")
			tag_subestacao["nome"] = self.get_mrid(subestacao)
			paparente = "1"
			rpostrafo = "1"
			qpostrafo = "1"
			rzerotrafo = "1"
			qzerotrafo = "1"
			rpos = "1"
			qpos = "1"
			rzero = "1"
			qzero ="1"
			tensaop = "69"
			tensaos = "13.8"


			tag_zpos = rnp.new_tag("impedancia")
			tag_zpos["tipo"] = "seq_pos"
			tag_r = rnp.new_tag("resistencia")
			tag_r["multip"] = ""
			tag_r["unid"] = "pu"
			tag_r.append(rpos)
			tag_q = rnp.new_tag("reatancia")
			tag_q["multip"] = ""
			tag_q["unid"] = "pu"
			tag_q.append(qpos)
			tag_zpos.append(tag_r)
			tag_zpos.append(tag_q)

			tag_zzero = rnp.new_tag("impedancia")
			tag_zzero["tipo"] = "seq_zero"
			tag_r = rnp.new_tag("resistencia")
			tag_r["multip"] = ""
			tag_r["unid"] = "pu"
			tag_r.append(rzero)
			tag_q = rnp.new_tag("reatancia")
			tag_q["multip"] = ""
			tag_q["unid"] = "pu"
			tag_q.append(qzero)
			tag_zzero.append(tag_r)
			tag_zzero.append(tag_q)

			tag_subestacao.append(tag_zpos)
			tag_subestacao.append(tag_zzero)

			tag_elementos.append(tag_subestacao)

			for count in range(1,3):
				tag_transformer = rnp.new_tag("transformador")
				tag_transformer["nome"] = self.get_mrid(subestacao).replace("E ","") + "_T" + str(count)
				tag_power = rnp.new_tag("potencia")
				tag_power["tipo"] = "aparente"
				tag_power["multip"] = "M"
				tag_power["unid"] = "VA"
				tag_power.append(paparente)

				tag_zpos = rnp.new_tag("impedancia")
				tag_zpos["tipo"] = "seq_pos"
				tag_r = rnp.new_tag("resistencia")
				tag_r["multip"] = ""
				tag_r["unid"] = "ohms"
				tag_r.append(rpostrafo)
				tag_q = rnp.new_tag("reatancia")
				tag_q["multip"] = ""
				tag_q["unid"] = "ohms"
				tag_q.append(qpostrafo)
				tag_zpos.append(tag_r)
				tag_zpos.append(tag_q)

				tag_zzero = rnp.new_tag("impedancia")
				tag_zzero["tipo"] = "seq_zero"
				tag_r = rnp.new_tag("resistencia")
				tag_r["multip"] = ""
				tag_r["unid"] = "ohms"
				tag_r.append(rzerotrafo)
				tag_q = rnp.new_tag("reatancia")
				tag_q["multip"] = ""
				tag_q["unid"] = "ohms"
				tag_q.append(qzerotrafo)
				tag_zzero.append(tag_r)
				tag_zzero.append(tag_q)

				tag_enrolamentop = rnp.new_tag("enrolamento")
				tag_enrolamentop["tipo"] = "primario"
				tag_tensao = rnp.new_tag("tensao")
				tag_tensao["multip"] = "k"
				tag_tensao["unid"] = "V"
				tag_tensao.append(tensaop)
				tag_enrolamentop.append(tag_tensao)

				tag_enrolamentos = rnp.new_tag("enrolamento")
				tag_enrolamentos["tipo"] = "secundario"
				tag_tensao = rnp.new_tag("tensao")
				tag_tensao["multip"] = "k"
				tag_tensao["unid"] = "V"
				tag_tensao.append(tensaos)
				tag_enrolamentos.append(tag_tensao)

				tag_transformer.append(tag_power)
				tag_transformer.append(tag_zpos)
				tag_transformer.append(tag_zzero)
				tag_transformer.append(tag_enrolamentop)
				tag_transformer.append(tag_enrolamentos)

				tag_elementos.append(tag_transformer)



		i=0
		# INSERÇÃO DE TOPOLOGIA

		# Topologia dos nós
		for consumer in self.consumer_list:
			i+=1
			tag_elemento = rnp.new_tag("elemento")
			tag_elemento["tipo"] = "no"
			tag_elemento["nome"] = self.get_mrid(consumer)

			tag_vizinhos = rnp.new_tag("vizinhos")
			tag_chaves = rnp.new_tag("chaves")

			for neighbour in consumer.neighbours:
				tag_consumer = rnp.new_tag("no")
				tag_consumer["nome"] = self.get_mrid(neighbour)
				tag_vizinhos.append(tag_consumer)

			for im_neighbour in consumer.im_neighbours:
				if im_neighbour.name == "breaker":
					tag_breaker = rnp.new_tag("chave")
					tag_breaker["nome"] = self.get_mrid(im_neighbour)
					tag_chaves.append(tag_breaker)

			tag_elemento.append(tag_vizinhos)
			tag_elemento.append(tag_chaves)
			tag_topologia.append(tag_elemento)

		# Topologia dos setores
		for setor in self.sectors:
			tag_elemento = rnp.new_tag("elemento")
			tag_elemento["tipo"] = "setor"
			tag_elemento["nome"] = setor.name
			tag_neighbours = rnp.new_tag("vizinhos")
			tag_nodes = rnp.new_tag("nos")

			for neighbour in setor.neighbours:
				tag_neighbour = rnp.new_tag("vizinho")
				tag_neighbour["nome"] = neighbour.name
				tag_neighbours.append(tag_neighbour)

			for node in setor.nodes:
				tag_node = rnp.new_tag("node")
				tag_node["nome"] = self.get_mrid(node)
				tag_nodes.append(tag_node)

			tag_elemento.append(tag_neighbours)
			tag_elemento.append(tag_nodes)
			tag_topologia.append(tag_elemento)


		# for breaker in self.breaker_list:
		#     tag_elemento = rnp.new_tag("elemento")
		#     tag_elemento["tipo"] = "chave"
		#     tag_elemento["nome"] = self.get_mrid(breaker)
			
		#     tag_n1 = rnp.new_tag("n1")
		#     tag_n2 = rnp.new_tag("n2")






		output_file = open(file,"w")
		output_file.write(rnp.prettify(formatter="xml"))

		






