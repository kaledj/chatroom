#!/usr/bin/python                                                                                                                        

from socket import *
import re
import thread
import select

class ChatServer:
	serverPort = 0
	backlog = 5
	clientSockets = []
	clientInfo = []
	# constructor                                                                                                                                                                 
	def __init__(self, serverPort):
		self.serverPort = serverPort

	# run                                                                                                                                                                         
	def run(self):
		serverSocket = socket(AF_INET,SOCK_STREAM)
		serverSocket.bind(('',self.serverPort))
		serverSocket.listen(self.backlog)
		inputs = [serverSocket]
		print ("Server ready for chat clients")
		while(1):
			inputready, outputready, exceptready = select.select(inputs, [], [])
			for s in inputready:
				if s == serverSocket:
					connectionSocket, addr  = serverSocket.accept()
					inputs.append(connectionSocket)
					self.clientSockets.append(connectionSocket)
				elif s in self.clientSockets:
					thread.start_new_thread(self.handle_connection,(s,))

	def nameExists(self, name):
		for s in self.clientInfo:
			if s[1] == name:
				return True
		return False

	def getSocketInfo(self, connectionSocket):
		for s in self.clientInfo:
			if s[0] == connectionSocket:
				return s

	def socketInfoExists(self, connectionSocket):
		for s in self.clientInfo:
			if s[0] == connectionSocket:
				return True
		return False

	# handle_connection                                                                                                                                                           
	def handle_connection(self, connectionSocket):
		try:
			request = connectionSocket.recv(1024)
			splitRequest = request.split(' ', 1)
			if splitRequest[0] == "NAME":
				#print request
				if len(splitRequest) == 2:
					if(self.nameExists(splitRequest[1])):
						connectionSocket.send("ERROR Name is in use")
						self.clientSockets.remove(connectionSocket)
					else:
						self.clientInfo.append([connectionSocket,splitRequest[1],""])
						connectionSocket.send("OK")
				else:
					connectionSocket.send("ERROR Invalid name")
			elif splitRequest[0] == "GETMSGS":
				#print request
				info = self.getSocketInfo(connectionSocket)
				message = "MSGS " + info[2]
				connectionSocket.send(message)
				info[2] = ""
				print message
			elif splitRequest[0] == "GETUSERS":
				#print request
				data = "USERS "
				for i in self.clientInfo:
					data += i[1]+"\n"
				connectionSocket.send(data)
				print data
			elif splitRequest[0] == "PUT":
				#print request
				if len(splitRequest) == 2:
					name = self.getSocketInfo(connectionSocket)[1]
					for s in self.clientInfo:
						if(s[2]):
							s[2] += "\n"
						s[2] += "<"+name+">"+splitRequest[1]
					#connectionSocket.send("OK")
			elif splitRequest[0] == "USERS":
				#print request
				data = "MSGS \nUsers:"
				for i in self.clientInfo:
					data += i[1]+"\n"
				connectionSocket.send(data)
			else:
				if connectionSocket in self.clientSockets:
					self.clientSockets.remove(connectionSocket)
					self.clientInfo.remove(self.getSocketInfo(connectionSocket))
		except Exception:
			pass
server = ChatServer(15008)
server.run()
