#!/usr/bin/python                                                                                                                             

"""
chatclient.py: Defines a python class that implements a client for a chatroom. 

author: David Kale, Sina Tashakkori, Tim Jassmann
version: 2
"""

from ChatGUI import *
from socket import *
import re, thread, sys, signal, os
import time

class ChatClient(QtCore.QObject):

	userName = ""
	login = False

	# Constructor                                                                                                                             
	#
	def __init__(self, serverPort):
		self.app = QtGui.QApplication(sys.argv)
		super(ChatClient, self).__init__()
		self.serverPort = serverPort
		self.GUI = ChatGUI()
		self.GUI.connectMessageInput(self.send_message)
		# Connects relevant signals to GUI slots
		self.connectSignals()
		self.clientThread = thread.start_new_thread(self.run, ())
		self.app.exec_()

	def connectSignals(self):
		# Signals to GUI
		self.connect(self, QtCore.SIGNAL("updateUsers"), self.GUI.setUserList)
		self.connect(self, QtCore.SIGNAL("addMessage"), self.GUI.addMessage)
		self.connect(self, QtCore.SIGNAL("exit"), self.GUI.exit)
		self.connect(self, QtCore.SIGNAL("promptUsername"), self.GUI.showLoginDialog)
		# Signals from GUI
		self.connect(self.GUI, QtCore.SIGNAL("usernameGiven"), self.setUsername)
		self.connect(self.GUI, QtCore.SIGNAL("usernameChanged"), self.changeUsername)
		self.connect(self.GUI, QtCore.SIGNAL("languageChanged"), self.changeLanguage)

	# process_command - Takes expected command line arguments to initialize username.
	#
	def process_command(self,command):
		if not command:
			print "Error, username not provided. Program terminated"
			sys.exit()
		else:
			self.userName = command

	def promptUsername(self):
		self.emit(QtCore.SIGNAL("promptUsername"),)

	def setUsername(self, username):
		if username is not self.userName:
			self.userName = str(username)

	def changeUsername(self, username):
		if username.toAscii() != self.userName:
			self.serverSocket.send("NAME " + username)
			status = self.serverSocket.recv(128)
			if status != "ERROR Name is in use":
				self.userName = username.toAscii()

	def changeLanguage(self, lang):
		self.serverSocket.send("LANG " + lang)

	# send_message - Obtains the text from chat input and sends them to server. 
	#				 PUT is prepended to indicate the method.
	#
	def send_message(self):
		message = self.GUI.chatInput.text().toAscii()
		if message:
			message = "PUT " + message
			self.GUI.chatInput.clear()
			self.serverSocket.send(message)
		self.GUI.chatInput.setFocus()		

	# get_data - Polls the server for the most recent users list and the most
	#			 recent chat log. The specific functionality of each is delegated
	#			 to an appropriate function call.
	#
	def get_data(self):
		while(1):
			time.sleep(.25)
			self.get_users()
			self.check_response()
			self.get_msgs()
			self.check_response()

	# get_users - Polls the server for the most recent list of users. This
	#			  list is sent to the GUI.
	#
	def get_users(self):
		message = "GETUSERS"
		try:
			self.serverSocket.send(message)
		except Exception, e:
			print "Error connecting to server"
			self.emit(QtCore.SIGNAL("exit"),)
			sys.exit(0)

	# get_msgs - Polls the server for the most recent chat log. When complete, 
	#            the GUI is notified via signal. 
	#
	def get_msgs(self):
		message = "GETMSGS"
		try:
			self.serverSocket.send(message)
		except Exception, e:
			print "Error connecting to server"
			self.emit(QtCore.SIGNAL("exit"),)
			sys.exit(0)

	def check_response(self):
		try:
			chats = self.serverSocket.recv(4196)
			response = chats.split(" ", 1)
			if response[0] == "USERS":
				self.emit(QtCore.SIGNAL("updateUsers"), response[1])
			elif response[0] == "MSGS":
				self.emit(QtCore.SIGNAL("addMessage"), response[1])
			elif response[0] == "ERROR":
				pass
		except Exception, e:
			print e
			pass


	# check_status - Small helper method that checks a given server status.
	#		
	def check_status(self,status):
		if status == "OK":
			print "ok to chat"
		else:
			print status
			self.app.closeAllWindows()

	# run - Processes the command line arguments and checks for validity. Then, 
	#		establishes a TCP connection with the chatroom server. Main event
	#		based execution loop is entered, where a message may have been typed
	#		and sent by the GUI, and meanwhile the client simply polls the 
	#		server periodically for the most recent chat data. 
	#
	def run(self):
		self.emit(QtCore.SIGNAL("promptUsername"),)
		while True:
			if self.userName: break
		self.serverSocket = socket(AF_INET,SOCK_STREAM)
		try:
			self.serverSocket.connect(('student.cs.appstate.edu',self.serverPort))
			self.serverSocket.send("NAME " + self.userName)
			status = self.serverSocket.recv(256)
			self.check_status(status)
			self.serverSocket.send("LANG en")
		except:
			print "Error contacting server"
			self.emit(QtCore.SIGNAL("exit"),)
			sys.exit(0)
		self.get_data()

def main():
	client = ChatClient(15008)

if __name__ == '__main__':
	main()
