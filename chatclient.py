#!/usr/bin/python                                                                                                                             

from ChatGUI import *
from socket import *
import re
import thread
import sys

class ChatClient:

	userName = ""
	serverPort = 0
	
	# constructor                                                                                                                             
	def __init__(self, serverPort):
		self.serverPort = serverPort
		self.GUI = ChatGUI()

	# handle_connection                                                                                                                       
	def send_username(self, serverPort):
		request = connectionSocket.recv(1024)
		regex = re.compile(request)

	def process_command(self,command):
		if not command:
			print "Error, username not provided. Program terminated"
			sys.exit()
		else:
			self.userName = command

	def send_message(self,message,serverSocket):
		message = "PUT " + message
		serverSocket.send(message)

	def send_get(self,serverSocket):
		while(1):
			message = "GET"
			serverSocket.send(message)

			try:
				for i in range(2):
					chats = serverSocket.recv(4196)
					chatsArray = chats.split(" ",1)
					if chatsArray[0] == "USERS":
						self.GUI.setuserlist(chatsArray[1])

					elif chatsArray[0] == "MSGS":
						self.GUI.addMessage(chatsArray[1])
						print("David is really gay")

			except Exception, e:
				pass
	
	def check_status(self,status):
		if status == "OK":
			print "ok to chat"

		else:
			print status

	def run(self):
		self.process_command("Test")
		#self.process_command(sys.argv[1])
		serverSocket = socket(AF_INET,SOCK_STREAM)
		serverSocket.settimeout(.25)
		serverSocket.connect(('student.cs.appstate.edu',self.serverPort))
		serverSocket.send("NAME " + self.userName)
		status = serverSocket.recv(256)
		self.check_status(status)
		self.send_message("Sina loves the D",serverSocket)
		status = serverSocket.recv(256)
		self.check_status(status)
		self.send_get(serverSocket)
		thread.start_new_thread(self.send_get,(serverSocket,))
		while(1):
			a = 0

def main():
	app = QtGui.QApplication(sys.argv)            
	#thread.start_new_thread(sys.exit, (app.exec_, ))
	client = ChatClient(15008)
	thread.start_new_thread(client.run, ())
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()