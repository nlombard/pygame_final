#Nicholas Lombardo
#4/21/2016
#Twisted_Proxy_Server

from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from GameSpace import GameSpace
from Client import ClientConnFactory
from Client import ClientConnection
from Server import ServerConnFactory
from Server import ServerConnection
import zlib

class Comm(object):
	def __init__(self,host,port):
		self.comm = self
		self.client_conn = False
		#self.SERVER_HOST = '127.0.0.1' #other game to connect to
		self.SERVER_HOST = host
		self.SERVER_PORT = port
	def write(self,data):
		if self.client_conn == True:
			#sd = zlib.compress(data)
			self.comm.client.transport.write(data)

if __name__ == '__main__':
	#SERVER_HOST = '10.26.191.133' #other game to connect to
	SERVER_HOST = '127.0.0.1' #other game to connect to
	SERVER_PORT = 32001

	lc_speed = 1/40	
	status = input("Welcome to TimeFresh and the Quest for Sushi!\nServer (0) or Client (1): ")

	if status == 0:
		comm = Comm(SERVER_HOST,SERVER_PORT)
		comm.status = "server"
		gs = GameSpace(reactor,comm,status)
		gs.main() #init game space
		lc = LoopingCall(gs.gameloop)
		reactor.listenTCP(comm.SERVER_PORT, ServerConnFactory(comm,gs)) #begin connection to proxy server
		lc.start(lc_speed)
		gs.update()
	elif status == 1:
		#SERVER_HOST = input("Enter Friend's IP: ")
		comm = Comm(SERVER_HOST,SERVER_PORT)
		comm.status = "client"
		gs = GameSpace(reactor,comm,status)	
		gs.main() #init game space
		lc = LoopingCall(gs.gameloop)
		reactor.connectTCP(comm.SERVER_HOST, comm.SERVER_PORT, ClientConnFactory(comm,gs)) #begin connection to proxy server
		lc.start(lc_speed)
		gs.update()
		#print "If a window does not open soon, please try reconnecting or make sure the server is running."

	reactor.run() #start reactor