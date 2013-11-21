#!/usr/bin/python                                                                                                                             

from ChatGUI import *
from socket import *
import re, thread, sys, signal, os
import time

class ChatClient(QtCore.QObject):
	userName = ""
	#serverPort = 0
	
	# constructor                                                                                                                             
	def __init__(self, serverPort):
		self.app = QtGui.QApplication(sys.argv)
		super(ChatClient, self).__init__()
		self.serverPort = serverPort
		self.GUI = ChatGUI()
		self.GUI.connectMessageInput(self.send_message)
		self.clientThread = thread.start_new_thread(self.run, ())
		self.connect(self, QtCore.SIGNAL("updateUsers"), self.GUI.setUserList)
		self.connect(self, QtCore.SIGNAL("addMessage"), self.GUI.addMessage)
		sys.exit(self.app.exec_())

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

	def send_message(self):
		message = self.GUI.chatInput.text().toAscii()
		if message:
			message = "PUT " + message
			self.GUI.chatInput.clear()
			self.serverSocket.send(message)
		self.GUI.chatInput.setFocus()		

	def get_data(self):
		while(1):
			time.sleep(.25)
			self.get_users()
			self.get_msgs()

	def get_users(self):
		message = "GETUSERS"
		self.serverSocket.send(message)
		try:
			chats = self.serverSocket.recv(4196)
			chatsArray = chats.split(" ",1)
			#print chatsArray
			if chatsArray[0] == "USERS":
				self.emit(QtCore.SIGNAL("updateUsers"), chatsArray[1])
				#self.GUI.setUserList(chatsArray[1])
				#signal.signal(signal.SIGALRM, self.GUI.updateUserList)
				#signal.alarm(1)
				#print("chatsArray[0] == USERS")
			#else: 
				#print chatsArray
				#print "error in get_users"
		except Exception, e:
			pass

	def get_msgs(self):
		message = "GETMSGS"
		self.serverSocket.send(message)
		try:
			chats = self.serverSocket.recv(4196)
			chatsArray = chats.split(" ",1)
			#print chatsArray
			if chatsArray[0] == "MSGS":
				#self.GUI.addMessage(chatsArray[1])
				self.emit(QtCore.SIGNAL("addMessage"), chatsArray[1])
			else:
				print "error in get_msgs"
		except Exception, e:
			pass

	def check_status(self,status):
		if status == "OK":
			print "ok to chat"
		else:
			print status
			self.app.closeAllWindows()

	def run(self):
		self.process_command(sys.argv[1])
		self.serverSocket = socket(AF_INET,SOCK_STREAM)
		self.serverSocket.settimeout(.25)
		self.serverSocket.connect(('student.cs.appstate.edu',self.serverPort))
		self.serverSocket.send("NAME " + self.userName)
		status = self.serverSocket.recv(256)
		self.check_status(status)
		self.get_data()
		while(1):
			a = 0

def main():
	client = ChatClient(15008)

if __name__ == '__main__':
	main()
