from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
import cPickle as pickle
import zlib

class ServerConnFactory(Factory): #creates the connections with the clients
	def __init__(self,comm,gs):
		self.comm = comm
		self.gs = gs
		#self.serverconn = ServerConnection(Comm)

	#handler for the build protocol
	def buildProtocol(self,addr):
		return ServerConnection(self.comm,addr,self.gs)

class ServerConnection(Protocol): 
	
	def __init__(self,comm,addr,gs):
		self.addr = addr
		self.comm = comm
		self.comm.client = self
		self.gs = gs
	#handler for connection made
	def connectionMade(self): #called from the event queue when a connection is made
		print "SERVER: new connection recv from", self.addr
		self.comm.client_conn = True
		self.gs.create_player()
		#self.comm.write(str(self.gs.player.rect.center))
		self.gs.update()
		#self.gs.enemy_laser_array = []
		#self.gs.fire_count = 0
	#a handler for data received on this connection, this connection is to the client
	def dataReceived(self,data):
		#data = zlib.decompress(data)
		#data = pickle.loads(pd)
		#print "SERVER: data received", data
		self.data_parse(data)
		
	#a handler for when a connection is lost to the client
	def connectionLost(self, reason):
		print "SERVER: lost connection to", self.addr
		self.comm.client_conn = False


	def data_parse(self,glob):
		for data in glob:
			if data == "h":
				self.gs.hearts -= 1
			elif data == "f" or data == "u" or data == "d" or data == "r" or data == "l" or data == "q" or data == "e":
				self.gs.player2.simple_move(data)
			else:
				pass
				#for enemy in self.gs.enemy_array:
				#	if str(enemy.id) == data:
				#		print "enemy fire!"
						#enemy.simple_fire()
				#		break
			self.gs.update()
