# -*- encoding: utf-8 -*-
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from xml.dom import minidom


class Sector(object):
	def __init__(self, name=None):
		self.nodes = []
		self.neighbours = []
		self.name = name

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

			#Definir nomes dos alimentadores
			self.name_feeders()

			#Definir nomes dos setores
			self.name_sectors()

			self.define_busbar_neighbours()

			# Cria listas para cada breaker receber teus nodes
			for breaker in self.breaker_list:
				breaker.nodes = []
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
				print "Consumer: " + str(consumer.find("mrid").text).strip()
				print "    Vizinhos:"
				for neighbour in consumer.im_neighbours:
					print "        " + str(neighbour.find("mrid").text).strip()  

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

			print "Writing xml..."
			self.write_xml()



	def name_feeders(self):
		'''
		Função que define os alimentadores principais
		'''
		print "Definindo lista de alimentadores..."
		self.feeder_list = []
		for busbar in self.busbar_list:
			for i in range(len(busbar.findAll("terminal"))-1):
				feeder_name = str(busbar.find('mrid').text).strip() + "_" + str(i)
				self.feeder_list.append(feeder_name)
				print "Alimentador " + feeder_name + " adicionado com sucesso!"

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
				return
			im_neighbour = im_neighbour_info[0]
			im_neighbour_terminal = im_neighbour_info[1]
			print "Vizinho Imediato encontrado: " + im_neighbour.name + " " + self.get_mrid(im_neighbour)

			if im_neighbour.name == "conductor":
				neighbour_info = self.find_connected(im_neighbour,im_neighbour_terminal)
				neighbour = neighbour_info[0]
				neighbour_terminal = neighbour_info[1]
				consumer.im_neighbours.append(neighbour)
				if neighbour.name == "breaker":
					# Define breaker como chave do nó de carga
					consumer.switches.append(neighbour)
					neighbour.nodes.append(consumer)
					connection_info = self.find_connected(neighbour,neighbour_terminal)
					connection = connection_info[0]
					connection_terminal = connection_info[1]
					if connection.name == "busbarsection":
						connection.neighbours.append(consumer)
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

	def define_busbar_neighbours(self):
		for busbar in self.busbar_list:
			busbar.neighbours = []


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

	def get_mrid_list(self,element_list=None):
		mrid_list = []
		for element in element_list:
			mrid_list.append(str(element.find('mrid').text).strip())
		return mrid_list

	def write_xml(self,file="/home/mateusvieira/Dropbox/GREI - Workspace/Test 001/rede_adaptada_RNP"):
		rnp = BeautifulSoup()
		tag_rede = rnp.new_tag("rede")
		tag_elementos = rnp.new_tag("elementos")
		tag_topologia = rnp.new_tag("topologia")
		tag_rede.append(tag_elementos)
		tag_rede.append(tag_topologia)
		rnp.append(tag_rede)

		for breaker in self.breaker_list:
			mrid = str(breaker.find("mrid").text).strip()
			estado = str(breaker.find("normalopen").text).strip()
			if estado == "1":
				estado = "aberto"
			else:
				estado = "fechado"
			tag_chave = rnp.new_tag("chave")
			tag_chave["nome"] = mrid
			tag_chave["estado"] = estado
			tag_elementos.append(tag_chave)
			
        tag_condutor = xml_rnp.new_tag("condutor")
        tag_condutor["nome"] = "CAA 266R"
        tag_condutor["rp"] = "0.2391"
        tag_condutor["xp"] = "0.37895"
        tag_condutor["rz"] = "0.41693"
        tag_condutor["xz"] = "1.55591"
        tag_condutor["ampacidade"] = "301"
        tag_elementos.append(tag_condutor)


		output_file = open(file,"w")
		output_file.write(rnp.prettify(formatter="xml"))

		






