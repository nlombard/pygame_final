from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
import cPickle as pickle
import zlib

#client
class ClientConnFactory(ClientFactory): #creates the connections with the client
	def __init__(self,comm,gs):
		self.comm = comm
		self.gs = gs
	def buildProtocol(self,addr):
		return ClientConnection(self.comm,addr,self.gs) #returns a clientConnection object

class ClientConnection(Protocol):  #a single tcp connection from client to server
	def __init__(self,comm,addr,gs):
		self.addr = addr
		self.comm = comm
		self.comm.client = self
		self.gs = gs
	def connectionMade(self): #called from the event queue when a connection is made
		print "CLIENT: connection made", self.addr
		self.comm.client_conn = True
		self.gs.create_player() #create second player
		for enemy in self.gs.enemy_array:
			if enemy.id % 2 == 1: #every even enemy
				enemy.player = self.gs.player2
		self.gs.update()
	def dataReceived(self,data):
		#data = zlib.decompress(data)
		# #data = pickle.loads(pd)
		#print "CLIENT received data:", data
		self.data_parse(data)

	def connectionLost(self, reason):  #when connection lost close everything
		print "CLIENT: lost connection to", self.addr
		self.comm.client_conn = False

	def data_parse(self,glob):
		for data in glob:
			if data == "h":
				self.gs.hearts -= 1
			elif data == "f" or data == "u" or data == "d" or data == "r" or data == "l" or data == "q" or data == "e":
				self.gs.player2.simple_move(data)
			else:
				for enemy in self.gs.enemy_array:
					if str(enemy.id) == data:
						enemy.simple_fire()
			self.gs.update()