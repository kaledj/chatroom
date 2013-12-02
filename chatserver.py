#!/usr/bin/python                                                                                                                        
"""
ChatServer: class that runs the chatserver

author: David Kale, Sina Tashakkori, Tim Jassmann
version: 1
"""

from socket import *
import re
import thread
import select

debug = False

class ChatServer:
	serverPort = 0
	backlog = 5
	clientSockets = []
	clientInfo = []
	# Constructor
	#
	def __init__(self, serverPort):
		self.serverPort = serverPort

	# run - creates serversocket and listens on that socket for requests.
	#
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
	
	# nameExists - returns true if the name exists. Otherwise returns false.
	# 
	# Parameters: 
	# name - the name to check
	#
	# Returns: true if name exists.
	#
	def nameExists(self, name):
		for s in self.clientInfo:
			if s[1] == name:
				return True
		return False
	
	# getSocketInfo - returns socket info tuple.
	#
	# Parameters:
	# connectionSocket - the socket to get info about
	#
	# Returns: The tuple containing info on the socket.
	#
	def getSocketInfo(self, connectionSocket):
		for s in self.clientInfo:
			if s[0] == connectionSocket:
				return s

	# socketInfoExists - returns true if info on the socket exists.
	#
	# Parameters:
	# connectionSocket - the socket to look for info on.
	#
	# Returns: True if info on the socket exists.
	# 
	def socketInfoExists(self, connectionSocket):
		for s in self.clientInfo:
			if s[0] == connectionSocket:
				return True
		return False

	# handle_connection - handles a request from a connection.
	# Requests:
	# NAME - sets the name of the socket
	# GETMSGS - sends messages for specific client
	# GETUSERS - sends the user list
	# PUT - adds the message to each user's message list
	# 
	# Parameters:
	# connectionSocket - the socket to handle a request from
	def handle_connection(self, connectionSocket):
		try:
			request = connectionSocket.recv(1024)
			splitRequest = request.split(' ', 1)
			if splitRequest[0] == "NAME":
				if len(splitRequest) == 2:
					if(self.nameExists(splitRequest[1])):
						connectionSocket.send("Error: Name is in use")
						self.clientSockets.remove(connectionSocket)
					else:
						self.clientInfo.append([connectionSocket,splitRequest[1],""])
						connectionSocket.send("OK")
				else:
					connectionSocket.send("ERROR Invalid name")
			elif splitRequest[0] == "GETMSGS":
				info = self.getSocketInfo(connectionSocket)
				message = "MSGS " + info[2]
				connectionSocket.send(message)
				info[2] = ""
				if debug: print message
			elif splitRequest[0] == "GETUSERS":
				data = "USERS "
				for i in self.clientInfo:
					data += i[1]+"\n"
				connectionSocket.send(data)
				if debug: print data
			elif splitRequest[0] == "PUT":
				if len(splitRequest) == 2:
					name = self.getSocketInfo(connectionSocket)[1]
					for s in self.clientInfo:
						if(s[2]):
							s[2] += "\n"
						s[2] += "<"+name+">"+splitRequest[1]
			else:
				if connectionSocket in self.clientSockets:
					self.clientSockets.remove(connectionSocket)
					self.clientInfo.remove(self.getSocketInfo(connectionSocket))
		except Exception:
			pass

#creates new server on port 15008
server = ChatServer(15008)
#runs the server
server.run()
